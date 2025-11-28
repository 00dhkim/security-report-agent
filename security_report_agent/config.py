# 중앙에서 모델 설정을 관리합니다.
# MODEL_NAME = "gemini-2.5-flash"

from google.adk.models.lite_llm import LiteLlm
from google.adk.models.google_llm import Gemini
# MODEL = LiteLlm(model="friendliai/Qwen/Qwen3-235B-A22B-Instruct-2507")
MODEL = Gemini(model="gemini-2.5-flash")
