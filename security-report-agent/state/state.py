from pydantic import BaseModel
from typing import List, Optional

class ReportRecord(BaseModel):
    src_ip: Optional[str] = None
    dst_ip: Optional[str] = None
    dst_port: Optional[int] = None
    count: Optional[int] = None

class ThreatInfo(BaseModel):
    # IP/포트 단위 위협 정보
    ip: Optional[str] = None
    port: Optional[int] = None
    is_malicious: Optional[bool] = None
    threat_level: Optional[str] = None  # "low", "medium", "high", "unknown"
    categories: List[str] = []       # "botnet", "scanner", "bruteforce" 등
    sources: List[str] = []          # VT, AbuseIPDB, InternalDB 등
    detail_url: Optional[str] = None

class RiskAssessment(BaseModel):
    overall_level: str              # "정상", "주의", "위험"
    key_findings: List[str]         # 중요한 포인트 문장 리스트
    recommended_actions: List[str]  # 권고 조치

#TODO: 지금 참조되지 않고 있다
class MonthlySocState(BaseModel):
    # 입력
    report_path: Optional[str] = None          # doc 파일 경로 또는 ID
    report_csv_text: Optional[str] = None      # CSV 형태의 원문 (문자열)
    records: List[ReportRecord] = []        # 파싱된 레코드 목록

    # 위협 검색 결과
    threats: List[ThreatInfo] = []          # IP/포트별 위협 정보

    # 리스크 판단
    risk: Optional[RiskAssessment] = None      # 보안 전문가 관점 리스크 요약

    # 최종 결과
    final_summary_ko: Optional[str] = None     # 한 문단 한국어 요약
