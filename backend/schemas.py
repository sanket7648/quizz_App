from pydantic import BaseModel
from typing import List

class ChoiceBase(BaseModel):
    id: int
    text: str
    is_correct: bool

    class Config:
        from_attributes = True

class QuestionBase(BaseModel):
    id: int
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