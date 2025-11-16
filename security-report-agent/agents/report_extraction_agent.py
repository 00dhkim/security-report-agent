from google.adk.agents import Agent
from google.adk.tools import FunctionTool

from ..config import MODEL
from ..tools.extraction_tools import doc_report_to_csv, csv_to_records

report_extraction_agent = Agent(
    name="ReportExtractionAgent",
    model=MODEL,
    description="월간 보안 관제 보고서 doc 파일을 파싱하여 CSV와 정형화된 레코드 리스트로 변환합니다.",
    instruction="""당신은 보고서 추출 전문가입니다.
    1. 'doc_report_to_csv' 도구를 사용하여 주어진 'report_path'로부터 CSV 텍스트를 추출하십시오.
    2. 추출된 CSV 텍스트를 'csv_to_records' 도구에 전달하여 레코드 리스트를 생성하십시오.
    3. 최종적으로 추출된 레코드 리스트를 각각 'records' 키로 출력하십시오.
    """,
    tools=[
        FunctionTool(func=doc_report_to_csv),
        FunctionTool(func=csv_to_records)
    ],
    # 이 에이전트의 출력이 다음 에이전트의 입력으로 사용될 수 있도록 상태 키를 매핑합니다.
    output_key="records",  # 현재 세션의 state 객체에 'records' 키로 저장됩니다. 근데 이모티콘 막 있고 몇 문단에 거친 LLM의 출력 그 자체를 state 객체의 reords로 저장해버림. 이를 방지하려면 schema로 저장하는게 맞을듯.
    include_contents='none',
)
