import json
import logging
import os
import time
import urllib.error
import urllib.request
from functools import lru_cache
from typing import Any, Dict, Optional

from dotenv import load_dotenv

load_dotenv()


def _fetch_virustotal(ip: str) -> Optional[Dict[str, Any]]:
    vt_api_key_env = "VT_API_KEY"
    vt_timeout = 10
    vt_max_retries = 3
    initial_backoff = 8  # Start with 8 seconds for the first retry

    api_key = os.getenv(vt_api_key_env)
    if not api_key:
        logging.warning("VirusTotal API key not found. Skipping IP lookup.")
        return None

    url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip}"
    request = urllib.request.Request(url, headers={"x-apikey": api_key})

    for attempt in range(vt_max_retries):
        try:
            with urllib.request.urlopen(request, timeout=vt_timeout) as response:
                return json.load(response)
        except urllib.error.HTTPError as e:
            if e.code == 429:  # Rate limit exceeded
                wait_time = initial_backoff * (2**attempt)
                logging.warning(
                    "VirusTotal rate limit hit. Retrying in %d seconds... (Attempt %d/%d)",
                    wait_time,
                    attempt + 1,
                    vt_max_retries,
                )
                time.sleep(wait_time)
            else:
                logging.error("VirusTotal API request failed with HTTP status %d: %s", e.code, e.reason)
                return None  # Non-recoverable HTTP error
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as e:
            logging.error("Error during VirusTotal request for IP %s: %s", ip, e)
            return None  # Non-recoverable error

    logging.error("Failed to fetch from VirusTotal for IP %s after %d attempts.", ip, vt_max_retries)
    return None


def _normalize_virustotal(ip: str, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    data = payload.get("data") if isinstance(payload, dict) else None
    attributes = data.get("attributes", {}) if isinstance(data, dict) else {}
    if not attributes:
        return None

    reputation = attributes.get("reputation")
    stats = attributes.get("last_analysis_stats", {}) or {}
    malicious = int(stats.get("malicious", 0) or 0)
    suspicious = int(stats.get("suspicious", 0) or 0)

    threat_level = "unknown"
    if reputation is not None:
        if reputation <= -30:
            threat_level = "high"
        elif reputation < 0:
            threat_level = "medium"

    if threat_level == "unknown":
        if malicious >= 1 or suspicious >= 2:
            threat_level = "low"

    is_malicious = (reputation is not None and reputation < 0) or malicious > 0

    categories = []
    # Extract categories from analysis results
    last_analysis_results = attributes.get("last_analysis_results", {})
    if isinstance(last_analysis_results, dict):
        for engine_result in last_analysis_results.values():
            if not isinstance(engine_result, dict):
                continue
            category = engine_result.get("category")
            result = engine_result.get("result")
            if (category in {"malicious", "suspicious"}) and result not in {
                "clean",
                "unrated",
                "malicious",
                "suspicious",
            }:
                categories.append(result)

    # Extract categories from tags
    vt_tags = attributes.get("tags") or []
    if isinstance(vt_tags, list):
        categories.extend(tag for tag in vt_tags if isinstance(tag, str))

    deduped_categories = list(dict.fromkeys(categories))

    return {
        "ip": ip,
        "reputation": reputation,
        "is_malicious": is_malicious,
        "threat_level": threat_level,
        "categories": deduped_categories,
        "sources": ["VirusTotal"],
        "detail_url": f"https://www.virustotal.com/gui/ip-address/{ip}",
    }


def ip_lookup(ip: str) -> Dict[str, Any]:
    """
    단일 IP 주소에 대해 악성 여부와 위협 수준을 조회합니다.
    VirusTotal API를 우선 호출하고, 실패 시 기본값을 반환합니다.
    """
    vt_payload = _fetch_virustotal(ip)
    vt_result = _normalize_virustotal(ip, vt_payload) if vt_payload else None
    if vt_result:
        return vt_result

    return {
        "ip": ip,
        "reputation": None,
        "is_malicious": False,
        "threat_level": "unknown",
        "categories": [],
        "sources": [],
        "detail_url": None,
    }


@lru_cache(maxsize=1)
def _port_service_index() -> Dict[int, str]:
    index: Dict[int, str] = {}
    try:
        with open("/etc/services", "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                # 주석 제거 후 처리
                line = line.split("#", 1)[0].strip()
                if not line:
                    continue
                parts = line.split()
                if len(parts) < 2 or "/" not in parts[1]:
                    continue
                port_part, _proto = parts[1].split("/", 1)
                if not port_part.isdigit():
                    continue
                port_num = int(port_part)
                # 이미 등록된 포트는 덮어쓰지 않고 최초 값 유지
                index.setdefault(port_num, parts[0])
    except OSError:
        pass
    return index


def _classify_port(port: int, service_name: Optional[str]) -> Dict[str, Any]:
    service = (service_name or "").lower()

    if port in {3389, 5900, 5985, 5986, 23} or "rdp" in service or "vnc" in service:
        return {"threat_level": "high", "categories": ["remote access", "exploit target" if port == 3389 else "bruteforce target"]}
    if port == 22 or "ssh" in service:
        return {"threat_level": "medium", "categories": ["remote access", "bruteforce target"]}
    if port in {445, 139, 135} or "smb" in service or "netbios" in service:
        return {"threat_level": "high", "categories": ["lateral movement", "ransomware target"]}
    if port in {21, 990} or "ftp" in service:
        return {"threat_level": "medium", "categories": ["file transfer", "bruteforce target"]}
    if port in {80, 443, 8080, 8443, 8000} or "http" in service or "https" in service:
        return {"threat_level": "low", "categories": ["web"]}
    if port == 53 or "dns" in service:
        return {"threat_level": "low", "categories": ["DNS"]}
    if port in {1433, 1521, 3306, 5432, 6379, 27017} or any(db in service for db in ["sql", "mongo", "redis", "db"]):
        return {"threat_level": "medium", "categories": ["database"]}

    return {
        "threat_level": "low" if service else "unknown",
        "categories": [service] if service else [],
    }


def port_lookup(port: int) -> Dict[str, Any]:
    """
    단일 포트 번호가 알려진 고위험 서비스 또는 공격 벡터에 해당하는지 조회합니다.
    """
    service_name = _port_service_index().get(port)
    classification = _classify_port(port, service_name)
    sources = ["etc/services"] if service_name else []

    return {
        "port": port,
        "is_malicious": None,
        "threat_level": classification["threat_level"],
        "categories": classification["categories"],
        "sources": sources,
        "detail_url": None,
    }
