from google.adk.agents import Agent
from google.adk.tools import FunctionTool

from ..config import MODEL
from ..tools.threat_tools import ip_lookup, port_lookup
from ..state.state import Records, RecordsAndThreats

threat_search_agent = Agent(
    name="ThreatSearchAgent",
    model=MODEL,
    description="추출된 접속 기록의 IP와 포트를 조회하여 위협 정보를 수집합니다.",
    instruction="""당신은 위협 인텔리전스 분석가입니다.
    입력으로 주어진 'records' 리스트를 순회하면서, 각 레코드의 'src_ip', 'dst_ip'와 'dst_port'에 대해 위협 조회를 수행해야 합니다.
    
    1. 모든 레코드에 나타난 모든 IP 주소(src_ip, dst_ip)를 중복 없이 수집하십시오.
    2. 각 고유 IP에 대해 'ip_lookup' 도구를 한 번씩만 호출하여 위협 정보를 얻으십시오.
    3. 모든 레코드에 나타난 모든 포트 번호(dst_port)를 중복 없이 수집하십시오.
    4. 각 고유 포트에 대해 'port_lookup' 도구를 한 번씩만 호출하여 위협 정보를 얻으십시오.
    5. 조회된 모든 IP 및 포트 위협 정보를 취합하여 하나의 'threats' 리스트로 만드십시오.
    6. 최종적으로 'threats' 리스트를 상태에 업데이트하십시오.
    """,
    tools=[
        FunctionTool(func=ip_lookup),
        FunctionTool(func=port_lookup)
    ],
    input_schema=Records,
    output_schema=RecordsAndThreats,
    include_contents='none',
)
