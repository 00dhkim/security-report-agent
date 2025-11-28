import csv
import io
from typing import List, Dict, Any

def doc_report_to_csv(report_path: str) -> Dict[str, str]:
    """
    월간 보안 관제 doc 보고서 파일을 파싱하여 src_ip, dst_ip, dst_port, count 컬럼을 가진 CSV 텍스트로 변환합니다.
    (이것은 실제 .doc 파일 파서를 시뮬레이션하는 모의 함수입니다.)
    """
    # TODO: 실제 .doc 파일 파싱 로직 구현이 필요합니다.
    # 현재는 고정된 모의 CSV 데이터를 반환하고 있습니다.
    # 'python-docx' 라이브러리를 사용하여 'report_path'의 파일을 열고,
    # 테이블 또는 텍스트에서 정해진 포맷에 따라 데이터를 추출하는 코드를 작성해야 합니다.
    print(f" MOCK: doc_report_to_csv(report_path='{report_path}')")
    # 여기서는 항상 고정된 CSV 문자열을 반환합니다.
    mock_csv_data = (
        "src_ip,dst_ip,dst_port,count\n"
        "192.168.1.10,8.8.8.8,53,150\n"
        "10.0.0.5,203.0.113.1,22,5\n"
        "192.168.1.12,198.51.100.2,443,2000\n"
        "1.2.3.4,10.0.0.5,3389,12\n"
        "203.0.113.1,192.168.1.10,80,80\n"
        "111.222.111.222,10.0.0.5,22,2\n"
    )
    return {"csv_text": mock_csv_data}

def csv_to_records(csv_text: str) -> Dict[str, List[Dict[str, Any]]]:
    """
    src_ip, dst_ip, dst_port, count 컬럼을 가진 CSV를 파싱하여 ReportRecord 리스트로 변환합니다.
    """
    print(f" csv_to_records(csv_text=...)")
    records = []
    # 문자열을 파일처럼 다루기 위해 io.StringIO 사용
    csv_file = io.StringIO(csv_text)
    reader = csv.DictReader(csv_file)
    for row in reader:
        records.append({
            "src_ip": row.get("src_ip"),
            "dst_ip": row.get("dst_ip"),
            "dst_port": int(row["dst_port"]) if row.get("dst_port") else None,
            "count": int(row["count"]) if row.get("count") else None,
        })
    return {"records": records}
