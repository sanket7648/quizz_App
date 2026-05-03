"""
OpenAI GPT Quiz - Syntax, Proxies, & Async Fixed
"""

import json
import os
from typing import List, Dict, Any
from openai import AsyncOpenAI  # <-- Changed to AsyncOpenAI

_client = None

def get_client():
    global _client
    if _client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY missing")
        # Initialize the Async client
        _client = AsyncOpenAI(api_key=api_key)
    return _client

async def generate_questions(topic: str, num_questions=5, difficulty=2):
    client = get_client()
    
    example_json = '{"questions": [{"text": "?", "choices": [{"text": "A", "is_correct": false}, {"text": "B", "is_correct": true}], "difficulty": 2}]}'
    prompt = f"Generate {num_questions} MCQs on '{topic}' (difficulty {difficulty}). Return JSON like: {example_json}"
    
    try:
        # Await now works properly with the AsyncOpenAI client
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            response_format={ "type": "json_object" } # Forces strict JSON mode
        )
        content = response.choices[0].message.content.strip()
        
        # Find JSON
        start = content.find('{')
        end = content.rfind('}') + 1
        data = json.loads(content[start:end])
        
        questions = data.get("questions", [])
        validated = []
        for q in questions:
            validated.append({
                "text": q.get("text", ""),
                "choices": q.get("choices", []),
                "difficulty": q.get("difficulty", difficulty)
            })
        return validated[:num_questions]
    except Exception as e:
        raise Exception(f"OpenAI: {e}")

async def generate_questions_sync(topic, num_questions=5, difficulty=2):
    return await generate_questions(topic, num_questions, difficulty)