# main.py

from fastapi import FastAPI
from pydantic import BaseModel
from educhain import Educhain

app = FastAPI()
from educhain import Educhain, LLMConfig
from langchain_google_genai import ChatGoogleGenerativeAI

from educhain import Educhain, LLMConfig
from langchain_core.language_models.chat_models import BaseChatModel

from educhain import Educhain, LLMConfig
from langchain_core.language_models.fake import FakeListLLM

from educhain import Educhain, LLMConfig
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage
from educhain import Educhain, LLMConfig
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.outputs import ChatGeneration, ChatResult
from langchain_core.messages import AIMessage
import json
# ✅ Fully implemented Dummy LLM with required abstract methods
class DummyLLM(BaseChatModel):
    def _llm_type(self) -> str:
        return "dummy-llm"

    def _generate(self, messages, stop=None, run_manager=None, **kwargs) -> ChatResult:
        # Return a valid mock response in expected format
        dummy_response = {
            "questions": [
                {
                    "question": "What does a 'for' loop do in Python?",
                    "options": ["Iterates", "Sleeps", "Jumps", "Crashes"],
                    "answer": "Iterates"
                },
                {
                    "question": "Which keyword starts a loop?",
                    "options": ["if", "def", "for", "class"],
                    "answer": "for"
                }
            ]
        }

        return ChatResult(
            generations=[ChatGeneration(
                message=AIMessage(content=json.dumps(dummy_response))
            )]
        )

# Inject into EduChain
dummy_model = DummyLLM()
config = LLMConfig(custom_model=dummy_model)
client = Educhain(config)
# ---------- MCQ Tool ----------
class MCQRequest(BaseModel):
    topic: str
    num: int = 5

@app.post("/generate_mcqs")
def generate_mcqs(request: MCQRequest):
    mcqs = client.qna_engine.generate_questions(
        topic=request.topic,
        num=request.num,
        question_type="Multiple Choice"
    )
    return mcqs.model_dump()



# ---------- Lesson Plan Tool ----------
class LessonRequest(BaseModel):
    topic: str
    duration: str = "45 minutes"
    grade_level: str = "High School"

@app.post("/generate_lesson_plan")
def generate_lesson(request: LessonRequest):
    lesson = client.content_engine.generate_lesson_plan(
        topic=request.topic,
        duration=request.duration,
        grade_level=request.grade_level
    )
    return lesson.model_dump()
