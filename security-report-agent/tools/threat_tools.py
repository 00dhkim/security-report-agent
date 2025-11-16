from typing import Dict, Any

def ip_lookup(ip: str) -> Dict[str, Any]:
    """
    단일 IP 주소에 대해 악성 여부와 위협 수준을 조회합니다.
    (이것은 외부 위협 인텔리전스 API 호출을 시뮬레이션하는 모의 함수입니다.)
    """
    # TODO: 실제 외부 위협 인텔리전스 API 연동 구현이 필요합니다.
    # 현재는 고정된 모의 DB를 사용하고 있습니다.
    # 'requests' 또는 'httpx' 라이브러리를 사용하여 VirusTotal, AbuseIPDB, OTX AlienVault 등
    # 외부 API를 호출하고, 그 결과를 ThreatInfo 스키마에 맞게 파싱하여 반환해야 합니다.
    # API 키는 환경 변수에서 관리하는 것이 좋습니다.
    print(f" MOCK: ip_lookup(ip='{ip}')")
    # 실제 구현에서는 VirusTotal, AbuseIPDB 등의 API를 호출해야 합니다.
    mock_db = {
        "8.8.8.8": {
            "ip": "8.8.8.8",
            "is_malicious": False,
            "threat_level": "unknown",
            "categories": ["DNS"],
            "sources": ["InternalDB"],
            "detail_url": None,
        },
        "203.0.113.1": {
            "ip": "203.0.113.1",
            "is_malicious": True,
            "threat_level": "high",
            "categories": ["botnet", "scanner"],
            "sources": ["VT", "AbuseIPDB"],
            "detail_url": "https://www.virustotal.com/gui/ip-address/203.0.113.1",
        },
        "1.2.3.4": {
            "ip": "1.2.3.4",
            "is_malicious": True,
            "threat_level": "medium",
            "categories": ["bruteforce"],
            "sources": ["AbuseIPDB"],
            "detail_url": None,
        },
        "111.222.111.222": {
            "ip": "111.222.111.222",
            "is_malicious": True,
            "threat_level": "high",
            "categories": ["botnet", "bruteforce", "scanner"],
            "sources": ["VT", "AbuseIPDB", "InternalDB"],
            "detail_url": "https://www.virustotal.com/gui/ip-address/111.222.111.222",
        }
    }
    return mock_db.get(ip, {
        "ip": ip,
        "is_malicious": False,
        "threat_level": "unknown",
        "categories": [],
        "sources": [],
        "detail_url": None,
    })

def port_lookup(port: int) -> Dict[str, Any]:
    """
    단일 포트 번호가 알려진 고위험 서비스 또는 공격 벡터에 해당하는지 조회합니다.
    """
    # TODO: 실제 포트 정보 조회 로직 구현이 필요합니다.
    # 현재는 널리 알려진 일부 포트에 대한 고정된 모의 DB를 사용하고 있습니다.
    # 더 포괄적인 포트 정보(예: IANA 목록, Nmap 서비스 정보 등)를 기반으로
    # 데이터베이스를 구축하거나, 관련 정보를 제공하는 내부 시스템과 연동해야 합니다.
    print(f" MOCK: port_lookup(port={port})")
    mock_db = {
        22: {
            "port": 22,
            "is_malicious": None,
            "threat_level": "medium",
            "categories": ["remote access", "bruteforce target"],
        },
        3389: {
            "port": 3389,
            "is_malicious": None,
            "threat_level": "high",
            "categories": ["remote access", "exploit target"],
        },
        53: {"port": 53, "threat_level": "low", "categories": ["DNS"]},
        80: {"port": 80, "threat_level": "low", "categories": ["web"]},
        443: {"port": 443, "threat_level": "low", "categories": ["web"]},
    }
    return mock_db.get(port, {
        "port": port,
        "threat_level": "unknown",
        "categories": [],
    })
