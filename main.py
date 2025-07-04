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

# ✅ Create a fake LLM that always returns dummy text
fake_llm = FakeListLLM(responses=["Dummy response from fake LLM"])

# Configure EduChain to use the fake model
config = LLMConfig(custom_model=fake_llm)
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
