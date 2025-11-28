from google.adk.agents.sequential_agent import SequentialAgent

# 개별 에이전트 임포트
from .agents.report_extraction_agent import report_extraction_agent
from .agents.threat_search_agent import threat_search_agent
from .agents.risk_assessment_agent import risk_assessment_agent
from .agents.summary_agent import summary_agent

# 전체 워크플로우를 조율하는 루트 에이전트 정의
root_agent = SequentialAgent(
    name="SecurityReportPipelineAgent",
    description="보안 보고서 분석 파이프라인을 순차적으로 실행하여 최종 요약문을 생성합니다.",
    # 하위 에이전트가 리스트 순서대로 실행됩니다.
    sub_agents=[
        report_extraction_agent,
        threat_search_agent,
        risk_assessment_agent,
        summary_agent
    ],
    # 최종적으로 사용자에게 보여줄 출력값을 지정합니다.
    # summary_agent의 출력인 final_summary_ko를 최종 결과로 반환합니다.
    # output_key="final_summary_ko"
)
