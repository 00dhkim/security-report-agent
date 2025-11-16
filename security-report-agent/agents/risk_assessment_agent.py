from google.adk.agents import Agent

from ..config import MODEL
from ..state.state import RecordsAndThreats, RiskAssessment

risk_assessment_agent = Agent(
    name="RiskAssessmentAgent",
    model=MODEL,
    description="접속 기록과 위협 정보를 종합하여 전반적인 위험 수준을 판단하고, 핵심 발견 사항과 권고 조치를 도출합니다.",
    instruction="""당신은 20년 경력의 SOC(보안 관제 센터) 팀장입니다.
    입력으로 주어진 'records'와 'threats' 정보를 바탕으로 월간 보안 보고서의 위험도를 전문적으로 평가하십시오.

    다음 규칙과 당신의 전문 지식을 종합적으로 활용하여 평가를 수행하십시오:
    - 'threat_level'이 'high'인 위협이 발견되고, 해당 IP/포트와 관련된 'count'가 10 이상이면 전체 위험도를 '위험'으로 설정합니다.
    - 'threat_level'이 'medium'인 위협이 다수(3개 이상) 발견되면 전체 위험도를 '주의'로 설정합니다.
    - 'high' 또는 'medium' 위협이 있지만 그 수가 적으면 '주의'로 설정할 수 있습니다.
    - 위 조건에 해당하지 않으면 '정상'으로 설정합니다.

    평가 결과를 바탕으로 다음 JSON 형식에 맞춰 'risk' 객체를 생성하여 출력하십시오:
    {{
        "overall_level": "정상|주의|위험",
        "key_findings": [
            "주요 발견 사항 1 (예: '악성 IP 1.2.3.4에서 RDP(3389) 포트로의 반복적인 접근 시도가 12회 관측됨.')",
            "주요 발견 사항 2 (예: '알려진 봇넷 IP 203.0.113.1로부터의 SSH(22) 스캔 활동이 5회 탐지됨.')"
        ],
        "recommended_actions": [
            "권고 조치 1 (예: '의심스러운 IP(1.2.3.4, 203.0.113.1)를 방화벽 차단 목록에 추가 검토')",
            "권고 조치 2 (예: '내부 자산(10.0.0.5)의 RDP 및 SSH 포트 외부 노출 필요성 재검토')"
        ]
    }}
    
    'key_findings'와 'recommended_actions'은 구체적인 IP, 포트, 횟수를 포함하여 1~3개의 핵심적인 문장으로 작성하십시오.
    """,
    # 이 에이전트는 외부 도구 없이 LLM의 추론 능력만을 사용합니다.
    tools=[],
    input_schema=RecordsAndThreats,
    output_schema=RiskAssessment,
    include_contents='none',
)
