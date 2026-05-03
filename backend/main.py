from fastapi import FastAPI, Depends, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import json
import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import local modules
from database import engine, get_db, Base
from models import Topic, Question, Choice
from schemas import TopicBase, QuestionBase, ChoiceBase, QuizRequest
from websocket_manager import manager

# Create tables on startup
Base.metadata.create_all(bind=engine)

# Lifespan context manager for startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown logic (if needed)

# Initialize FastAPI app
app = FastAPI(
    title="Quizly Backend",
    description="Backend API for the Quizly quiz generator",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS to allow frontend requests
origins = [
    "http://localhost:3000",
    "http://localhost:5173",  # Vite default
    "http://localhost:5174",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
    "https://localhost",
    "https://127.0.0.1",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== ENDPOINTS ====================

@app.get("/", tags=["root"])
async def root():
    """Root endpoint to verify API is running"""
    return {"message": "Quizly Backend API", "version": "1.0.0", "status": "running"}

# ==================== TOPICS ====================

@app.get("/api/topics", response_model=List[TopicBase], tags=["Topics"])
async def get_topics(db: Session = Depends(get_db)):
    """Get all available quiz topics"""
    topics = db.query(Topic).all()
    return topics

@app.get("/api/topics/{topic_id}", response_model=TopicBase, tags=["Topics"])
async def get_topic(topic_id: int, db: Session = Depends(get_db)):
    """Get a specific topic by ID"""
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    return topic

@app.post("/api/topics", response_model=TopicBase, tags=["Topics"])
async def create_topic(name: str, db: Session = Depends(get_db)):
    """Create a new topic"""
    existing = db.query(Topic).filter(Topic.name == name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Topic already exists")
    
    topic = Topic(name=name)
    db.add(topic)
    db.commit()
    db.refresh(topic)
    return topic

# ==================== QUESTIONS ====================

@app.get("/api/topics/{topic_id}/questions", response_model=List[QuestionBase], tags=["Questions"])
async def get_topic_questions(
    topic_id: int,
    limit: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Get questions for a specific topic with optional limit"""
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    
    query = db.query(Question).filter(Question.topic_id == topic_id)
    
    if limit:
        query = query.limit(limit)
    
    questions = query.all()
    return questions

@app.get("/api/questions/{question_id}", response_model=QuestionBase, tags=["Questions"])
async def get_question(question_id: int, db: Session = Depends(get_db)):
    """Get a specific question by ID"""
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question

@app.post("/api/topics/{topic_id}/questions", response_model=QuestionBase, tags=["Questions"])
async def create_question(
    topic_id: int,
    text: str,
    difficulty: int = 1,
    db: Session = Depends(get_db)
):
    """Create a new question for a topic"""
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    
    question = Question(
        topic_id=topic_id,
        text=text,
        difficulty=difficulty
    )
    db.add(question)
    db.commit()
    db.refresh(question)
    return question

# ==================== CHOICES ====================

@app.post("/api/questions/{question_id}/choices", response_model=ChoiceBase, tags=["Choices"])
async def create_choice(
    question_id: int,
    text: str,
    is_correct: bool = False,
    db: Session = Depends(get_db)
):
    """Create a choice for a question"""
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    choice = Choice(
        question_id=question_id,
        text=text,
        is_correct=is_correct
    )
    db.add(choice)
    db.commit()
    db.refresh(choice)
    return choice

# ==================== QUIZ ENDPOINTS ====================

@app.get("/api/quiz/random", response_model=List[QuestionBase], tags=["Quiz"])
async def get_random_quiz(
    topic_id: int,
    num_questions: int = 5,
    db: Session = Depends(get_db)
):
    """Get random questions from a topic for a quiz"""
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    
    # Fetch questions (order by random in the app, not SQL for simplicity)
    questions = db.query(Question)\
        .filter(Question.topic_id == topic_id)\
        .limit(num_questions)\
        .all()
    
    if not questions:
        raise HTTPException(status_code=404, detail="No questions found for this topic")
    
    return questions[:num_questions]

# ==================== WEBSOCKET ====================

@app.websocket("/ws/challenge/{session_id}/{player_name}")
async def challenge_websocket(
    websocket: WebSocket,
    session_id: str,
    player_name: str,
    db: Session = Depends(get_db)
):
    """WebSocket endpoint for multiplayer quiz challenge"""
    await manager.connect(websocket, session_id, player_name)
    
    try:
        while True:
            # Wait for a player to submit an answer
            data = await websocket.receive_text()
            payload = json.loads(data)
            
            # Expected payload: {"action": "submit_answer", "question_id": 12, "choice_id": 45}
            if payload.get("action") == "submit_answer":
                question_id = payload.get("question_id")
                choice_id = payload.get("choice_id")
                
                # Check database to see if the choice is correct
                choice = db.query(Choice).filter(
                    Choice.id == choice_id,
                    Choice.question_id == question_id
                ).first()
                
                is_correct = choice.is_correct if choice else False
                
                if is_correct:
                    # Award points (e.g., 10 points per correct answer)
                    manager.update_score(session_id, player_name, 10)
                
                # Broadcast the updated state to both players
                await manager.broadcast(session_id, {
                    "type": "score_update",
                    "player": player_name,
                    "is_correct": is_correct,
                    "current_scores": manager.scores.get(session_id, {})
                })
                
    except WebSocketDisconnect:
        manager.disconnect(websocket, session_id, player_name)
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(websocket, session_id, player_name)

# ==================== HEALTH CHECK ====================

@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Quizly Backend"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
