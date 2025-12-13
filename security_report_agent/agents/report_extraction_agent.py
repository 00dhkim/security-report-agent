from google.adk.agents import Agent
from google.adk.tools import FunctionTool

from ..config import MODEL
from ..tools.extraction_tools import doc_report_parser, csv_to_records
from ..state.state import Records

report_extraction_agent = Agent(
    name="ReportExtractionAgent",
    model=MODEL,
    description="월간 보안 관제 보고서 doc/docx 파일(경로 또는 업로드)을 파싱하여 CSV와 정형화된 레코드 리스트로 변환합니다.",
    instruction="""당신은 보고서 추출 전문가입니다.
    1. 'doc_report_parser' 도구를 사용하여 텍스트를 추출하십시오. 사용자가 파일을 업로드한 경우 'report_path' 인자를 생략하여 업로드된 파일을 처리하십시오. 경로가 주어진 경우에만 'report_path'를 사용하십시오.
    2. 추출된 텍스트를 레코드 스키마에 맞게 적절히 변환하여 'records' 키로 출력하십시오.


## 참고 사항
- 추출된 텍스트에서 데이터를 빠짐없이 정확하게 변환해야합니다.
- 추출된 텍스트에서 일부 자료가 누락되거나, 형식이 다른 경우에도 유연하게 대처해야합니다.


## Example:
    [Extracted Text]
    ```No,Src IP,Dest IP,Port,Count
1,192.168.1.17,219.250.36.130,( domain )
53 / UDP,326973
1,192.168.1.17,185.125.190.58,( ntp )
123 / UDP,1363

...

No,Dest IP,Src IP,Port,Count
1,219.250.36.130,192.168.1.17,( domain )
53 / UDP,326973
1,219.250.36.130,192.168.1.20,( ntp )
123 / UDP,93188
```

    [Output]
    ```json
    {
        "records": [
            {
                "src_ip": "192.168.1.17",
                "dst_ip": "219.250.36.130",
                "dst_port": 53,
                "count": 326973
            },
            {
                "src_ip": "192.168.1.17",
                "dst_ip": "185.125.190.58",
                "dst_port": 123,
                "count": 1363
            },
            {
                "dst_ip": "219.250.36.130",
                "src_ip": "192.168.1.17",
                "dst_port": 53,
                "count": 326973
            },
            {
                "dst_ip": "219.250.36.130",
                "src_ip": "192.168.1.20",
                "dst_port": 123,
                "count": 93188
            }
        ]
    }
    ```
    """,
    tools=[
        FunctionTool(func=doc_report_parser),
        # FunctionTool(func=csv_to_records)
    ],
    # 이 에이전트의 출력이 다음 에이전트의 입력으로 사용될 수 있도록 상태 키를 매핑합니다.
    output_schema=Records,  # 현재 세션의 state 객체에 'records' 키로 저장됩니다. 근데 이모티콘 막 있고 몇 문단에 거친 LLM의 출력 그 자체를 state 객체의 reords로 저장해버림. 이를 방지하려면 schema로 저장하는게 맞을듯.
    include_contents='none',  # 에이전트의 history를 다음 에이전트에 전달하지 않음. stateless 작업에 유리.
)
