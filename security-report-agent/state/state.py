from pydantic import BaseModel
from typing import List, Optional

class ReportRecord(BaseModel):
    src_ip: Optional[str] = None
    dst_ip: Optional[str] = None
    dst_port: Optional[int] = None
    count: Optional[int] = None

class Records(BaseModel):
    records: List[ReportRecord] = []

class ThreatInfo(BaseModel):
    # IP/포트 단위 위협 정보
    ip: Optional[str] = None
    port: Optional[int] = None
    is_malicious: Optional[bool] = None
    threat_level: Optional[str] = None  # "low", "medium", "high", "unknown"
    categories: List[str] = []       # "botnet", "scanner", "bruteforce" 등
    sources: List[str] = []          # VT, AbuseIPDB, InternalDB 등
    detail_url: Optional[str] = None

class RecordsAndThreats(BaseModel):
    records: List[ReportRecord] = []
    threats: List[ThreatInfo] = []

class RiskAssessment(BaseModel):
    overall_level: str              # "정상", "주의", "위험"
    key_findings: List[str]         # 중요한 포인트 문장 리스트
    recommended_actions: List[str]  # 권고 조치
