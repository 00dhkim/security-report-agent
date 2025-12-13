from google.adk.agents.sequential_agent import SequentialAgent
from google.adk.apps.app import App
from google.adk.plugins.save_files_as_artifacts_plugin import SaveFilesAsArtifactsPlugin

# 개별 에이전트 임포트
from .agents.report_extraction_agent import report_extraction_agent
from .agents.threat_search_agent import threat_search_agent
from .agents.risk_assessment_agent import risk_assessment_agent
from .agents.summary_agent import summary_agent

class SecurityPipelineAgent(SequentialAgent):
    """
    ADK Runner의 App name mismatch 문제를 해결하기 위한 래퍼 클래스입니다.
    이 클래스를 정의함으로써 에이전트의 정의 위치가 이 파일(프로젝트 내부)로 인식됩니다.
    """
    pass

# 전체 워크플로우를 조율하는 루트 에이전트 정의
root_agent = SecurityPipelineAgent(
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

# App 정의: 에이전트와 플러그인을 포함하는 애플리케이션 객체
# SaveFilesAsArtifactsPlugin: 업로드된 파일을 아티팩트로 저장하여 에이전트가 도구로 접근할 수 있게 함
# name="security_report_agent": agent.py가 위치한 디렉토리 이름과 일치시켜야 함
app = App(
    name="security_report_agent",
    root_agent=root_agent,
    plugins=[SaveFilesAsArtifactsPlugin()]
)
