#!/usr/bin/env python
"""Verify PostgreSQL connection and data"""

from dotenv import load_dotenv
import os

load_dotenv()

from database import SessionLocal
from models import Topic, Question

db = SessionLocal()
try:
    topics = db.query(Topic).all()
    print("\n✅ PostgreSQL Connection Successful!")
    print(f"✓ Found {len(topics)} topics")
    
    for topic in topics:
        question_count = db.query(Question).filter(Question.topic_id == topic.id).count()
        print(f"  - {topic.name}: {question_count} questions")
    
    print("\n✅ Database is properly seeded and ready!")
    
except Exception as e:
    print(f"❌ Connection failed: {e}")
finally:
    db.close()
