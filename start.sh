#!/bin/bash
# Quick Start Script for Quizly Application
# Run both backend and frontend servers

echo "🚀 Starting Quizly Application..."
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if running on Windows
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" ]]; then
    IS_WINDOWS=true
else
    IS_WINDOWS=false
fi

# Start Backend
echo -e "${BLUE}📦 Starting Backend Server...${NC}"
cd backend

if [ "$IS_WINDOWS" = true ]; then
    # Windows
    if [ ! -d "venv" ]; then
        echo "Creating virtual environment..."
        python -m venv venv
    fi
    
    # Activate venv
    source venv/Scripts/activate
    
    # Install dependencies if not already installed
    pip install -q -r requirements.txt
    
    # Seed database
    python seed_db.py
    
    # Start server
    echo -e "${GREEN}✓ Backend starting at http://localhost:8000${NC}"
    start cmd /k "python main.py"
else
    # macOS/Linux
    if [ ! -d "venv" ]; then
        echo "Creating virtual environment..."
        python3 -m venv venv
    fi
    
    source venv/bin/activate
    pip install -q -r requirements.txt
    python seed_db.py
    
    echo -e "${GREEN}✓ Backend starting at http://localhost:8000${NC}"
    python main.py &
fi

cd ..

# Wait a bit for backend to start
sleep 2

# Start Frontend
echo -e "${BLUE}⚛️  Starting Frontend Server...${NC}"
cd brainburst-quizzes

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    if command -v bun &> /dev/null; then
        bun install -q
    else
        npm install -q
    fi
fi

echo -e "${GREEN}✓ Frontend starting at http://localhost:5173${NC}"
echo ""
echo -e "${GREEN}✅ Both servers are starting!${NC}"
echo ""
echo "📝 Next steps:"
echo "  1. Open http://localhost:5173 in your browser"
echo "  2. Open http://localhost:8000/docs for API documentation"
echo "  3. Start taking quizzes!"
echo ""
echo "🛑 To stop the servers, press Ctrl+C in both terminal windows"

if [ "$IS_WINDOWS" = false ]; then
    if command -v bun &> /dev/null; then
        bun run dev
    else
        npm run dev
    fi
else
    if command -v bun &> /dev/null; then
        start cmd /k "bun run dev"
    else
        start cmd /k "npm run dev"
    fi
fi
