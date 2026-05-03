# Integration Guide: Backend & Frontend

This document explains how the backend API integrates with the frontend application.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        React Frontend                            │
│                   (brainburst-quizzes)                          │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Components:                                             │  │
│  │  - Index (Home Page)                                     │  │
│  │  - Quiz Component                                        │  │
│  │  - CategoryCard                                          │  │
│  └──────────────────────────────────────────────────────────┘  │
│                            ▲                                     │
│                            │ (HTTP Requests)                     │
│                            │ (WebSocket - Optional)              │
│                            ▼                                     │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  API Client (lib/api.ts)                                 │  │
│  │  - getTopics()                                           │  │
│  │  - getRandomQuiz()                                       │  │
│  │  - convertToQuizFormat()                                 │  │
│  └──────────────────────────────────────────────────────────┘  │
│                            ▲                                     │
│                            │                                     │
│                            ▼                                     │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Custom Hooks (hooks/useQuizData.ts)                     │  │
│  │  - useCategories()                                       │  │
│  │  - useQuiz()                                             │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                            ▲
                            │ HTTP/JSON
                            │ CORS-enabled
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FastAPI Backend                             │
│                       (backend)                                  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Endpoints:                                              │  │
│  │  - GET  /api/topics                                      │  │
│  │  - GET  /api/topics/{id}/questions                       │  │
│  │  - GET  /api/quiz/random                                 │  │
│  │  - WS   /ws/challenge/{session_id}/{player_name}         │  │
│  │  - GET  /health                                          │  │
│  └──────────────────────────────────────────────────────────┘  │
│                            ▼                                     │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Database Layer:                                         │  │
│  │  - SQLAlchemy ORM                                        │  │
│  │  - Models: Topic, Question, Choice                       │  │
│  │  - SQLite (dev) / PostgreSQL (prod)                      │  │
│  └──────────────────────────────────────────────────────────┘  │
│                            ▼                                     │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Database:                                               │  │
│  │  - quiz.db (SQLite)                                      │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. Loading Categories

**User Action:** Page loads

**Flow:**
```
Frontend loads
    ↓
useCategories() hook called
    ↓
Calls: GET /api/topics
    ↓
Backend queries Topic table
    ↓
Returns: [{ id: 1, name: "Science" }, ...]
    ↓
Frontend merges with fallback data (icons, descriptions)
    ↓
Displays category cards
```

### 2. Starting a Quiz

**User Action:** Click on category

**Flow:**
```
User clicks "Science" category
    ↓
Quiz component mounts with categoryId="science"
    ↓
useQuiz("science", 5) hook called
    ↓
Calls: GET /api/topics/1/questions?limit=5
    ↓
Backend:
  - Finds Topic with id=1
  - Returns 5 Question objects with Choices
    ↓
convertToQuizFormat() transforms API response:
  - choices[] → options[]
  - Finds correct answer index
    ↓
Quiz displays questions and tracks answers locally
    ↓
Score calculated on frontend
    ↓
Results displayed
```

### 3. API Response Conversion

**API Response (from backend):**
```json
{
  "id": 1,
  "text": "What planet is known as the Red Planet?",
  "difficulty": 1,
  "topic_id": 1,
  "choices": [
    { "id": 1, "text": "Venus", "is_correct": false },
    { "id": 2, "text": "Mars", "is_correct": true },
    { "id": 3, "text": "Jupiter", "is_correct": false },
    { "id": 4, "text": "Saturn", "is_correct": false }
  ]
}
```

**Frontend Conversion:**
```javascript
convertToQuizFormat(apiQuestion) {
  return {
    id: 1,
    text: "What planet is known as the Red Planet?",
    difficulty: 1,
    topic_id: 1,
    choices: [...],
    // Added for compatibility with Quiz component:
    question: "What planet is known as the Red Planet?",
    options: ["Venus", "Mars", "Jupiter", "Saturn"],
    answer: 1  // Index of correct answer
  }
}
```

## Key Files

### Backend Files

| File | Purpose |
|------|---------|
| `main.py` | FastAPI application, all endpoints |
| `models.py` | SQLAlchemy models (Topic, Question, Choice) |
| `schemas.py` | Pydantic request/response models |
| `database.py` | Database connection & session management |
| `websocket_manager.py` | WebSocket connection handling |
| `seed_db.py` | Database initialization with quiz data |

### Frontend Files

| File | Purpose |
|------|---------|
| `src/lib/api.ts` | API client functions |
| `src/hooks/useQuizData.ts` | Custom hooks for data fetching |
| `src/routes/index.tsx` | Home page (category selection) |
| `src/components/Quiz.tsx` | Quiz component (uses API) |
| `src/lib/quizData.ts` | Fallback quiz data (used if API unavailable) |

## API Endpoints

### Get All Topics
```
GET /api/topics

Response:
[
  { "id": 1, "name": "Science" },
  { "id": 2, "name": "History" },
  ...
]
```

### Get Questions for Topic
```
GET /api/topics/{topic_id}/questions?limit=5

Response:
[
  {
    "id": 1,
    "text": "What planet is known as the Red Planet?",
    "difficulty": 1,
    "topic_id": 1,
    "choices": [...]
  },
  ...
]
```

### Get Random Quiz
```
GET /api/quiz/random?topic_id=1&num_questions=5

Response:
Same as above - random selection of 5 questions
```

### Health Check
```
GET /health

Response:
{ "status": "healthy", "service": "Quizly Backend" }
```

## Environment Configuration

### Backend (.env)
```env
DATABASE_URL=sqlite:///./quiz.db
HOST=0.0.0.0
PORT=8000
```

### Frontend (.env)
```env
VITE_API_URL=http://localhost:8000
```

## CORS Configuration

Backend allows requests from:
```python
origins = [
    "http://localhost:3000",
    "http://localhost:5173",  # Vite dev server
    "http://localhost:5174",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
    "https://localhost",
    "https://127.0.0.1",
]
```

For production, update this list with your actual domains.

## Error Handling

### Frontend Error Handling

```typescript
// API errors are caught and logged
try {
  const topics = await getTopics();
} catch (error) {
  console.warn("Failed to fetch from API");
  // Falls back to hardcoded data
  setCategories(fallbackCategories);
}
```

### Backend Error Handling

```python
# Returns proper HTTP status codes
if not topic:
    raise HTTPException(status_code=404, detail="Topic not found")

# Validation errors are automatically handled by Pydantic
```

## Fallback Mechanism

The frontend has a graceful fallback system:

1. **First attempt:** Fetch from API
2. **If API fails:** Use hardcoded data from `quizData.ts`
3. **User experience:** Seamless - looks the same either way

This allows the app to work even if the backend is temporarily unavailable.

## Testing the Integration

### Manual Testing

1. **Start backend:**
   ```bash
   cd backend
   python main.py
   ```

2. **Start frontend:**
   ```bash
   cd brainburst-quizzes
   npm run dev
   ```

3. **Test in browser:**
   - Open http://localhost:5173
   - Check browser Network tab (DevTools)
   - Should see API calls to http://localhost:8000

4. **Check API docs:**
   - Open http://localhost:8000/docs
   - Try endpoints interactively

### Common Issues

**"API Connection Failed"**
- Is backend running on port 8000?
- Check `.env` VITE_API_URL value
- Check browser console for CORS errors

**"Database not found"**
- Run `python seed_db.py`
- Check `quiz.db` exists in backend directory

**"Port already in use"**
- Kill process on that port
- Or change port in `.env` and VITE_API_URL

## Future Enhancements

1. **WebSocket Multiplayer:** Implement real-time multiplayer challenges
2. **User Authentication:** Add login/signup with score tracking
3. **Analytics:** Track quiz attempts and success rates
4. **Custom Quizzes:** Allow users to create custom quizzes
5. **Mobile App:** React Native version
6. **Caching:** Add Redis for improved performance
7. **Database:** Switch to PostgreSQL for production

## Performance Optimization

- **Frontend:** API responses are cached with React Query
- **Backend:** Database queries are indexed
- **Both:** CORS preflight requests are minimal

## Security Considerations

- Add authentication for creating/modifying quiz data
- Validate input on both frontend and backend
- Use HTTPS in production
- Implement rate limiting on API
- Sanitize quiz content
- Update dependencies regularly

---

**Questions or Issues?** Check the main [README.md](../README.md) or create an issue in the repository.
