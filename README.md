# Quizly - Quiz Generator Application

A full-stack quiz application with a React/TypeScript frontend and FastAPI backend. Features dynamic quiz categories, real-time scoring, and WebSocket support for multiplayer challenges.

## 📁 Project Structure

```
quizGenerator/
├── backend/              # FastAPI server
│   ├── main.py          # Main application with all endpoints
│   ├── models.py        # SQLAlchemy models
│   ├── schemas.py       # Pydantic schemas for validation
│   ├── database.py      # Database configuration
│   ├── websocket_manager.py  # WebSocket connection management
│   ├── seed_db.py       # Database seeding script
│   ├── requirements.txt  # Python dependencies
│   └── .env             # Environment variables
│
├── brainburst-quizzes/  # React/TypeScript frontend
│   ├── src/
│   │   ├── routes/      # TanStack Router pages
│   │   ├── components/  # React components
│   │   ├── hooks/       # Custom React hooks (useQuizData.ts)
│   │   ├── lib/         # Utilities (api.ts, quizData.ts)
│   │   └── ui/          # UI component library
│   ├── package.json
│   ├── vite.config.ts
│   └── .env             # Environment variables
│
└── README.md            # This file
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** for backend
- **Node.js 16+** and **Bun** for frontend
- A terminal/command prompt
- **PostgreSQL** hosted on Neon.tech (already configured)

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify database connection:**
   ```bash
   python verify_db.py
   ```
   
   You should see:
   ```
   ✅ PostgreSQL Connection Successful!
   ✓ Found 5 topics
   ```

5. **Start the backend server:**
   ```bash
   python main.py
   ```
   
   The server will run at `http://localhost:8000`

   **Check the API documentation at:** `http://localhost:8000/docs` (Swagger UI)

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd brainburst-quizzes
   ```

2. **Install dependencies using Bun:**
   ```bash
   bun install
   ```
   
   Or with npm:
   ```bash
   npm install
   ```

3. **Verify `.env` file:**
   ```
   VITE_API_URL=http://localhost:8000
   ```

4. **Start the development server:**
   ```bash
   bun run dev
   # Or with npm:
   npm run dev
   ```
   
   The app will be available at `http://localhost:5173` (or similar)

## 🔌 API Endpoints

### Topics
- `GET /api/topics` - Get all quiz topics
- `GET /api/topics/{id}` - Get specific topic
- `POST /api/topics` - Create new topic

### Questions
- `GET /api/topics/{topic_id}/questions` - Get questions for a topic
- `GET /api/questions/{id}` - Get specific question
- `POST /api/topics/{topic_id}/questions` - Create new question

### Quiz
- `GET /api/quiz/random` - Get random quiz questions for a topic
- `POST /api/quiz/generate` - **[NEW]** Generate quiz questions using AI for any custom topic

### WebSocket
- `WS /ws/challenge/{session_id}/{player_name}` - Multiplayer challenge

### Utilities
- `GET /` - API status
- `GET /health` - Health check

## 📊 Database Schema

### Database Type
**PostgreSQL** hosted on **Neon.tech** (AWS ap-southeast-1)

### Models

**Topic**
- `id`: Integer (Primary Key)
- `name`: String (Unique, Indexed)

**Question**
- `id`: Integer (Primary Key)
- `topic_id`: Integer (Foreign Key → Topic)
- `text`: String
- `difficulty`: Integer (1-3)

**Choice**
- `id`: Integer (Primary Key)
- `question_id`: Integer (Foreign Key → Question)
- `text`: String
- `is_correct`: Boolean

### Sample Data
- 5 quiz categories (Science, History, Technology, Geography, Sports)
- 40 total questions (8 per category)
- 160 answer choices (4 per question)

## 🔧 Configuration

### Backend (.env)
```env
DATABASE_URL=postgresql://...your-neon-url...  # PostgreSQL on Neon.tech
GEMINI_API_KEY=...your-gemini-api-key...       # Google Gemini API key for AI question generation
HOST=0.0.0.0
PORT=8000
```

### Frontend (.env)
```env
VITE_API_URL=http://localhost:8000  # Backend API URL
```

**Note:** Your PostgreSQL connection string is already configured in `.env`. 

### AI Features Setup

To enable AI-powered quiz generation, you need to:

1. **Get a Google Gemini API Key:**
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Add it to your backend `.env` file as `GEMINI_API_KEY`

2. **The app uses Gemini Pro** model for generating questions. You can modify the model in `ai_service.py`

3. **Cost:** Gemini has a free tier with generous rate limits - perfect for testing and small apps!

## 📝 Features

✅ **Dynamic Quiz Categories** - Fetch quiz topics from the backend
✅ **Random Questions** - Get random questions per quiz
✅ **AI-Powered Quiz Generation** - **[NEW]** Generate custom quizzes on any topic using Google Gemini
✅ **Custom Topic Input** - **[NEW]** Users can enter any topic and get AI-generated questions using Gemini
✅ **Difficulty Selection** - **[NEW]** Choose between Easy, Medium, and Hard questions
✅ **Score Tracking** - Real-time score calculation
✅ **Responsive Design** - Works on desktop and mobile
✅ **Fallback Data** - Uses hardcoded data if API is unavailable
✅ **WebSocket Support** - Ready for multiplayer challenges (partially implemented)
✅ **API Documentation** - Swagger UI at `/docs`

## 🛠️ Development

### Backend Commands

```bash
# Start server
python main.py

# Seed database
python seed_db.py

# View API docs
# Open http://localhost:8000/docs in browser
```

### Frontend Commands

```bash
# Development server
bun run dev

# Build for production
bun run build

# Preview production build
bun run preview

# Lint code
bun run lint
```

## 🔄 How Integration Works

### Pre-defined Categories (Database-based)
1. **Frontend loads** → Calls `GET /api/topics`
2. **Backend returns** topics list
3. **User selects category** → Frontend calls `GET /api/topics/{id}/questions?limit=5`
4. **Backend returns** random questions with choices
5. **User answers** → Quiz calculates score locally
6. **Results shown** → User can restart or pick another topic

### AI-Powered Generation (Custom Topics)
1. **User enters custom topic** → Frontend shows custom topic form
2. **User selects difficulty & number of questions** → Clicks "Generate Quiz"
3. **Frontend calls** `POST /api/quiz/generate` with topic details
4. **Backend calls Google Gemini API** to generate questions
5. **Gemini returns** JSON with questions and answer choices
6. **Backend validates** and returns formatted questions
7. **Frontend displays** generated quiz with answer tracking
8. **User answers** → Quiz calculates score
9. **Results shown** → User can regenerate or pick another topic

## 🧪 Testing the Integration

1. Start backend: `python main.py`
2. Start frontend: `bun run dev`
3. Open `http://localhost:5173`
4. Click on a category (e.g., "Science")
5. Answer questions and see results
6. Check backend logs for API calls

## 📱 Mobile Compatibility

The app is fully responsive and works on:
- Desktop browsers
- Tablets
- Mobile phones

## 🚨 Troubleshooting

### "API Connection Failed"
- Ensure backend is running on `http://localhost:8000`
- Check `.env` file in frontend for correct `VITE_API_URL`
- Check CORS is enabled in `main.py`

### "Database not found"
- Run `python seed_db.py` from backend directory
- Ensure you have write permissions in the directory

### "Port 8000 already in use"
- Kill existing process: `lsof -i :8000` (macOS/Linux) or `netstat -ano | findstr :8000` (Windows)
- Or change PORT in `.env`

## 🔐 Security Notes

- CORS is configured for localhost development
- Update `origins` list in `main.py` for production
- Use environment variables for sensitive data
- Add authentication for production

## 🚀 Production Deployment

1. **Update environment variables** for production
2. **Use PostgreSQL** instead of SQLite
3. **Add proper error handling** and logging
4. **Enable HTTPS** for WebSocket (WSS)
5. **Set proper CORS origins** for your domain
6. **Deploy** using Docker, AWS, Vercel, etc.

## 📚 Technology Stack

### Backend
- **Framework**: FastAPI
- **Database**: SQLAlchemy + SQLite (dev) / PostgreSQL (prod)
- **Validation**: Pydantic
- **Server**: Uvicorn

### Frontend
- **Framework**: React 18+
- **Routing**: TanStack Router
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **Package Manager**: Bun/npm

## 📄 License

[Your License Here]

## 👥 Contributing

Contributions welcome! Please follow the code style and test thoroughly.

## 📧 Support

For issues or questions, please create an issue in the repository.

---

**Happy Quizzing!** 🎉
