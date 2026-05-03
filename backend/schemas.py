from pydantic import BaseModel
from typing import List, Optional

class ChoiceBase(BaseModel):
    id: Optional[int] = None
    text: str
    is_correct: bool

    class Config:
        from_attributes = True

class QuestionBase(BaseModel):
    id: Optional[int] = None
    text: str
    difficulty: int
    choices: List[ChoiceBase] = []

    class Config:
        from_attributes = True

class TopicBase(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class QuizRequest(BaseModel):
    topic_id: int
    num_questions: int = 5

class GenerateQuizRequest(BaseModel):
    topic: str
    num_questions: int = 5
    difficulty: int = 2

class GeneratedQuiz(BaseModel):
    topic: str
    questions: List[QuestionBase]
    generated_at: str