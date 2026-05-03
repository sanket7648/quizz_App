# Quizly Backend API

FastAPI backend for the Quizly quiz generator application, connected to **PostgreSQL** on Neon.tech.

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Verify Database Connection

```bash
python verify_db.py
```

Expected output:
```
✅ PostgreSQL Connection Successful!
✓ Found 5 topics
```

### 3. Run Server

```bash
python main.py
```

Server starts at `http://localhost:8000`

## Database

**Type**: PostgreSQL (Neon.tech)
**Region**: ap-southeast-1 (AWS Asia Pacific)
**Status**: ✅ Pre-seeded with 40 quiz questions

### Data Included
- Science: 8 questions
- History: 8 questions
- Technology: 8 questions
- Geography: 8 questions
- Sports: 8 questions

## API Documentation

Once running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## API Endpoints

### Topics
```
GET /api/topics
GET /api/topics/{id}
POST /api/topics
```

### Questions  
```
GET /api/topics/{topic_id}/questions
GET /api/questions/{id}
POST /api/topics/{topic_id}/questions
```

### Choices
```
POST /api/questions/{question_id}/choices
```

### Quiz
```
GET /api/quiz/random?topic_id=1&num_questions=5
```

### WebSocket
```
WS /ws/challenge/{session_id}/{player_name}
```

### Health
```
GET /health
GET /
```

## Database

Uses SQLite for development (`quiz.db`).

### Models
- **Topic**: Quiz categories
- **Question**: Quiz questions with difficulty levels
- **Choice**: Multiple choice answers with correctness flag

## Environment Variables

Your `.env` file is pre-configured with Neon.tech PostgreSQL:

```env
DATABASE_URL=postgresql://neondb_owner:...@ep-empty-fire-ao6gl0zi-pooler.c-2.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
HOST=0.0.0.0
PORT=8000
```

**No changes needed!** The database is already connected and seeded.

## Project Structure

```
backend/
├── main.py              # FastAPI app & endpoints
├── models.py            # SQLAlchemy models
├── schemas.py           # Pydantic request/response models
├── database.py          # Database configuration
├── websocket_manager.py # WebSocket connection handling
├── seed_db.py          # Database initialization script
├── requirements.txt     # Python dependencies
└── .env                # Environment variables
```

## Development

### Verify Connection
```bash
python verify_db.py
```

### Add More Quiz Data

Edit `seed_db.py` to add more categories and questions, then run:
```bash
python seed_db.py
```

**Note:** This will clear existing data and re-populate the database.

### Modify Models

Update `models.py` for new database fields.

### Update API

Add new endpoints in `main.py`.

## Production Notes

Your app is already set up for production:
- ✅ PostgreSQL database (more scalable than SQLite)
- ✅ SSL/TLS encrypted connections
- ✅ Connection pooling configured
- ✅ Ready for deployment

## Troubleshooting

**PostgreSQL connection failed?**
```bash
python verify_db.py
```
Check .env file has correct DATABASE_URL

**Need to reset database?**
```bash
python seed_db.py
```

**Import errors?**
```bash
pip install -r requirements.txt --force-reinstall
```

**Connection still failing?**
1. Verify internet connection
2. Check .env DATABASE_URL is complete
3. Confirm credentials in .env match Neon.tech
4. Check sslmode=require in connection string
