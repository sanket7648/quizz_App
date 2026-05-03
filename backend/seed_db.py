"""
Seed the database with quiz data from quizData.ts
This script populates the database with topics, questions, and choices.
"""

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

from database import SessionLocal, engine, Base
from models import Topic, Question, Choice

# Quiz data mirrored from frontend's quizData.ts
QUIZ_DATA = {
    "science": {
        "name": "Science",
        "icon": "🧬",
        "questions": [
            {
                "text": "What planet is known as the Red Planet?",
                "options": ["Venus", "Mars", "Jupiter", "Saturn"],
                "answer": 1
            },
            {
                "text": "What is the chemical symbol for gold?",
                "options": ["Go", "Gd", "Au", "Ag"],
                "answer": 2
            },
            {
                "text": "Which gas do plants absorb from the atmosphere?",
                "options": ["Oxygen", "Hydrogen", "Nitrogen", "Carbon dioxide"],
                "answer": 3
            },
            {
                "text": "What is the speed of light (approx)?",
                "options": ["3×10^8 m/s", "3×10^6 m/s", "3×10^5 km/s", "Both A and C"],
                "answer": 3
            },
            {
                "text": "Human body has how many bones?",
                "options": ["196", "206", "216", "226"],
                "answer": 1
            },
            {
                "text": "Which is the largest organ in the human body?",
                "options": ["Liver", "Brain", "Skin", "Lungs"],
                "answer": 2
            },
            {
                "text": "Water boils at?",
                "options": ["90°C", "100°C", "110°C", "120°C"],
                "answer": 1
            },
            {
                "text": "DNA stands for?",
                "options": ["Deoxyribonucleic Acid", "Diribonucleic Acid", "Dinucleic Acid", "None"],
                "answer": 0
            },
        ]
    },
    "history": {
        "name": "History",
        "icon": "🏛️",
        "questions": [
            {
                "text": "Who was the first President of the USA?",
                "options": ["Lincoln", "Washington", "Jefferson", "Adams"],
                "answer": 1
            },
            {
                "text": "World War II ended in?",
                "options": ["1942", "1945", "1948", "1950"],
                "answer": 1
            },
            {
                "text": "The Great Wall is in?",
                "options": ["India", "Japan", "China", "Korea"],
                "answer": 2
            },
            {
                "text": "Who discovered America?",
                "options": ["Magellan", "Cook", "Columbus", "Vespucci"],
                "answer": 2
            },
            {
                "text": "The French Revolution began in?",
                "options": ["1789", "1799", "1776", "1804"],
                "answer": 0
            },
            {
                "text": "Taj Mahal was built by?",
                "options": ["Akbar", "Babur", "Shah Jahan", "Aurangzeb"],
                "answer": 2
            },
            {
                "text": "Who painted the Mona Lisa?",
                "options": ["Van Gogh", "Picasso", "Da Vinci", "Michelangelo"],
                "answer": 2
            },
            {
                "text": "The Berlin Wall fell in?",
                "options": ["1987", "1989", "1991", "1993"],
                "answer": 1
            },
        ]
    },
    "tech": {
        "name": "Technology",
        "icon": "💻",
        "questions": [
            {
                "text": "HTML stands for?",
                "options": ["HyperText Markup Language", "HighText Machine Language", "HyperTabular ML", "None"],
                "answer": 0
            },
            {
                "text": "Founder of Microsoft?",
                "options": ["Steve Jobs", "Bill Gates", "Elon Musk", "Mark Z."],
                "answer": 1
            },
            {
                "text": "Which is a JS framework?",
                "options": ["Django", "Laravel", "React", "Flask"],
                "answer": 2
            },
            {
                "text": "CPU stands for?",
                "options": ["Central Process Unit", "Central Processing Unit", "Computer Personal Unit", "Control Process Unit"],
                "answer": 1
            },
            {
                "text": "Who founded Tesla?",
                "options": ["Elon Musk", "Martin Eberhard", "Steve Jobs", "Jeff Bezos"],
                "answer": 0
            },
            {
                "text": "Which company makes the iPhone?",
                "options": ["Samsung", "Google", "Apple", "Sony"],
                "answer": 2
            },
            {
                "text": "AI stands for?",
                "options": ["Auto Intelligence", "Artificial Intelligence", "Applied Info", "Active Internet"],
                "answer": 1
            },
            {
                "text": "GitHub was acquired by?",
                "options": ["Google", "Microsoft", "Meta", "Amazon"],
                "answer": 1
            },
        ]
    },
    "geography": {
        "name": "Geography",
        "icon": "🌍",
        "questions": [
            {
                "text": "Capital of Australia?",
                "options": ["Sydney", "Melbourne", "Canberra", "Perth"],
                "answer": 2
            },
            {
                "text": "Largest ocean?",
                "options": ["Atlantic", "Indian", "Arctic", "Pacific"],
                "answer": 3
            },
            {
                "text": "Mount Everest is in?",
                "options": ["India", "Nepal", "China", "Bhutan"],
                "answer": 1
            },
            {
                "text": "Sahara is a?",
                "options": ["Sea", "Desert", "Forest", "Mountain"],
                "answer": 1
            },
            {
                "text": "Longest river?",
                "options": ["Amazon", "Nile", "Yangtze", "Mississippi"],
                "answer": 1
            },
            {
                "text": "Capital of Japan?",
                "options": ["Osaka", "Kyoto", "Tokyo", "Nagoya"],
                "answer": 2
            },
            {
                "text": "Smallest country?",
                "options": ["Monaco", "Vatican City", "Malta", "Nauru"],
                "answer": 1
            },
            {
                "text": "Which continent has the most countries?",
                "options": ["Asia", "Europe", "Africa", "S. America"],
                "answer": 2
            },
        ]
    },
    "sports": {
        "name": "Sports",
        "icon": "⚽",
        "questions": [
            {
                "text": "How many players in a football team?",
                "options": ["9", "10", "11", "12"],
                "answer": 2
            },
            {
                "text": "Olympics held every?",
                "options": ["2 yrs", "3 yrs", "4 yrs", "5 yrs"],
                "answer": 2
            },
            {
                "text": "Cricket originated in?",
                "options": ["India", "England", "Australia", "S. Africa"],
                "answer": 1
            },
            {
                "text": "Usain Bolt is from?",
                "options": ["USA", "Jamaica", "Kenya", "Trinidad"],
                "answer": 1
            },
            {
                "text": "Tennis grand slam played on grass?",
                "options": ["US Open", "French", "Wimbledon", "Australian"],
                "answer": 2
            },
            {
                "text": "Most NBA championships (player)?",
                "options": ["Jordan", "LeBron", "Russell", "Kobe"],
                "answer": 2
            },
            {
                "text": "FIFA World Cup 2022 winner?",
                "options": ["France", "Brazil", "Argentina", "Germany"],
                "answer": 2
            },
            {
                "text": "How long is a marathon (km)?",
                "options": ["40", "42.195", "45", "50"],
                "answer": 1
            },
        ]
    },

    "movies": {
        "name": "Movies",
        "icon": "🍿",
        "questions": [
            {
                "text": "Who directed Inception?",
                "options": ["Spielberg", "Nolan", "Cameron", "Tarantino"],
                "answer": 1
            },
            {
                "text": "Titanic released in?",
                "options": ["1995", "1997", "1999", "2001"],
                "answer": 1
            },
            {
                "text": "Iron Man actor?",
                "options": ["Chris Evans", "Robert Downey Jr.", "Mark Ruffalo", "Chris Hemsworth"],
                "answer": 1
            },
            {
                "text": "Highest grossing film (2024)?",
                "options": ["Avatar", "Avengers Endgame", "Titanic", "Star Wars 7"],
                "answer": 0
            },
            {
                "text": "Joker (2019) lead?",
                "options": ["Heath Ledger", "Joaquin Phoenix", "Jared Leto", "Jack Nicholson"],
                "answer": 1
            },
            {
                "text": "Studio behind Toy Story?",
                "options": ["Disney", "Pixar", "DreamWorks", "Sony"],
                "answer": 1
            },
            {
                "text": "Matrix protagonist?",
                "options": ["Neo", "Trinity", "Morpheus", "Smith"],
                "answer": 0
            },
            {
                "text": "Parasite is from?",
                "options": ["Japan", "China", "S. Korea", "Vietnam"],
                "answer": 2
            },
        ]
    }
}

def seed_database():
    """Populate the database with quiz data"""
    # Create all tables
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    try:
        # Clear existing data
        db.query(Choice).delete()
        db.query(Question).delete()
        db.query(Topic).delete()
        db.commit()
        
        # Seed each topic with its questions and choices
        for category_key, category_data in QUIZ_DATA.items():
            print(f"Seeding {category_data['name']}...")
            
            # Create topic
            topic = Topic(name=category_data["name"])
            db.add(topic)
            db.flush()  # Flush to get the ID
            
            # Create questions and choices for this topic
            for q_idx, q_data in enumerate(category_data["questions"]):
                question = Question(
                    topic_id=topic.id,
                    text=q_data["text"],
                    difficulty=1
                )
                db.add(question)
                db.flush()
                
                # Create choices for this question
                for choice_idx, choice_text in enumerate(q_data["options"]):
                    is_correct = choice_idx == q_data["answer"]
                    choice = Choice(
                        question_id=question.id,
                        text=choice_text,
                        is_correct=is_correct
                    )
                    db.add(choice)
            
            db.commit()
            print(f"✓ {category_data['name']} seeded successfully")
        
        print("\n✅ Database seeded successfully!")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding database: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
