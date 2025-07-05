# Check out- README.md for external citations and references.
# main.py

from fastapi import FastAPI
from pydantic import BaseModel
from educhain import Educhain

# Initialize FastAPI app
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

# Dummy LLM to mock lesson plan generation for testing
class DummyLLM(BaseChatModel):
    def _llm_type(self) -> str:
        """Return the type of the LLM."""
        return "dummy-llm"

    def _generate(self, messages, stop=None, run_manager=None, **kwargs) -> ChatResult:
        """
        Generate a hardcoded lesson plan response in the format expected by EduChain.
        """
        prompt = messages[-1].content.lower()

        if "loop" in prompt or "mcq" in prompt or "multiple choice" in prompt:
            # Return dummy MCQs
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
                    },
                    {
                        "question": "Which loop checks condition before executing?",
                        "options": ["for", "while", "do-while", "foreach"],
                        "answer": "while"
                    },
                    {
                        "question": "What is the output of: `for i in range(3): print(i)`?",
                        "options": ["0 1 2", "1 2 3", "0 1 2 3", "None"],
                        "answer": "0 1 2"
                    },
                    {
                        "question": "What keyword breaks a loop?",
                        "options": ["exit", "return", "stop", "break"],
                        "answer": "break"
                    }
                ]
            }
        else:
            # Return lesson plan (as already implemented)
            dummy_response = {
                "title": "Introduction to Algebra",
                "subject": "Algebra",
                "learning_objectives": [
                    "Understand the concept of variables",
                    "Apply operations to algebraic expressions",
                    "Solve basic linear equations"
                ],
                "lesson_introduction": "This lesson introduces fundamental concepts of algebra including variables and equations.",
                "main_topics": [
                    {
                        "title": "What is a variable?",
                        "subtopics": [
                            {
                                "title": "Definition of Variables",
                                "key_concepts": [
                                    {"type": "definition", "content": "A variable is a symbol used to represent a number."}
                                ],
                                "discussion_questions": [
                                    {"question": "Why do we use variables in math?"}
                                ],
                                "hands_on_activities": [
                                    {"title": "Variable Hunt", "description": "Find variables in real-life situations."}
                                ],
                                "reflective_questions": [
                                    {"question": "How would math be different without variables?"}
                                ],
                                "assessment_ideas": [
                                    {"type": "quiz", "description": "Short quiz on identifying variables."}
                                ]
                            }
                        ]
                    }
                ],
                "learning_adaptations": "Provide manipulatives for kinesthetic learners.",
                "real_world_applications": "Variables are used in science, engineering, and finance.",
                "ethical_considerations": "None."
            }

        # Return the response as a JSON string in AIMessage
        return ChatResult(
            generations=[ChatGeneration(
                message=AIMessage(content=json.dumps(dummy_response))
            )]
        )

# Inject DummyLLM into EduChain for testing
# This allows us to mock LLM responses for development and testing
# without calling a real LLM API.
dummy_model = DummyLLM()
config = LLMConfig(custom_model=dummy_model)
client = Educhain(config)

# Request model for MCQ generation
class MCQRequest(BaseModel):
    topic: str
    num: int = 5

@app.post("/generate_mcqs")
def generate_mcqs(request: MCQRequest):
    """
    Generate multiple-choice questions for a given topic using EduChain.
    """
    mcqs = client.qna_engine.generate_questions(
        topic=request.topic,
        num=request.num,
        question_type="Multiple Choice"
    )
    return mcqs.model_dump()

# Request model for lesson plan generation
class LessonRequest(BaseModel):
    topic: str
    duration: str = "45 minutes"
    grade_level: str = "High School"

@app.post("/generate_lesson_plan")
def generate_lesson(request: LessonRequest):
    """
    Generate a lesson plan for a given topic using EduChain.
    """
    # Add a keyword to guide DummyLLM for lesson plan mode
    request.topic = request.topic + " <<<lesson_mode>>>"
    lesson = client.content_engine.generate_lesson_plan(
        topic=request.topic,
        duration=request.duration,
        grade_level=request.grade_level
    )
    return lesson.model_dump()
