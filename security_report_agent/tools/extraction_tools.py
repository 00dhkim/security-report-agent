import csv
import io
import subprocess
import os
from docx import Document
from typing import List, Dict, Any

def _convert_doc_to_docx(doc_path):
    output_dir = os.path.dirname(doc_path)
    subprocess.run(["libreoffice", "--headless", "--convert-to", "docx", doc_path, "--outdir", output_dir])
    return doc_path.replace(".doc", ".docx")

def _parse_docx_tables(path):
    doc = Document(path)
    all_text = []

    # 본문 텍스트
    for para in doc.paragraphs:
        all_text.append(para.text)

    # 테이블 텍스트
    for table in doc.tables:
        for row in table.rows:
            row_text = [cell.text.strip().replace(",", "") for cell in row.cells]
            all_text.append(",".join(row_text))
        all_text.append("")  # 테이블 간 구분을 위해 빈 줄 추가

    return "\n".join(all_text)

def doc_report_parser(report_path: str) -> Dict[str, str]:
    """
    월간 보안 관제 doc 보고서 파일을 파싱하여 일반 본문과 No,Src IP,Dest IP,Port,Count 컬럼 등을 포함한 문자열을 반환합니다.
    """
    
    docx_path = _convert_doc_to_docx(report_path)
    parsed_text = _parse_docx_tables(docx_path)
    os.remove(docx_path) # remove the converted docx file

    print(f"doc extraction result:\n{parsed_text[:50]}...")

    return {"csv_text": parsed_text}

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
