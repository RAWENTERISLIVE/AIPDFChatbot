#!/bin/bash

# AI PDF Chatbot Startup Script
# This script starts both the FastAPI server and Streamlit client

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Starting AI PDF Chatbot...${NC}"

# Get the directory of this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Function to check if port is in use
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null ; then
        return 0
    else
        return 1
    fi
}

# Function to start server
start_server() {
    echo -e "${YELLOW}📡 Starting FastAPI Server...${NC}"
    cd "$SCRIPT_DIR/server"
    
    # Activate virtual environment or create if it doesn't exist
    if [ ! -d "venv" ]; then
        echo -e "${YELLOW}Creating server virtual environment...${NC}"
        python3 -m venv venv
    fi
    
    source venv/bin/activate
    
    # Install requirements if needed
    pip3 install -r requirements.txt >/dev/null 2>&1
    
    # Check if API key is set
    if [ ! -f ".env" ] || ! grep -q "GEMINI_API_KEY" .env; then
        echo -e "${RED}❌ Error: GEMINI_API_KEY not found in .env file${NC}"
        echo -e "${YELLOW}Please create a .env file with your Gemini API key:${NC}"
        echo -e "${BLUE}echo 'GEMINI_API_KEY=your_key_here' > server/.env${NC}"
        exit 1
    fi
    
    # Start server in background
    nohup python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 > ../logs/server.log 2>&1 &
    SERVER_PID=$!
    echo $SERVER_PID > ../logs/server.pid
    
    # Wait for server to start
    echo -e "${YELLOW}Waiting for server to start...${NC}"
    for i in {1..30}; do
        if check_port 8000; then
            echo -e "${GREEN}✅ Server started successfully on port 8000${NC}"
            break
        fi
        sleep 1
        if [ $i -eq 30 ]; then
            echo -e "${RED}❌ Server failed to start${NC}"
            exit 1
        fi
    done
    
    cd "$SCRIPT_DIR"
}

# Function to start client
start_client() {
    echo -e "${YELLOW}🖥️ Starting Streamlit Client...${NC}"
    cd "$SCRIPT_DIR/client"
    
    # Activate virtual environment or create if it doesn't exist
    if [ ! -d "venv" ]; then
        echo -e "${YELLOW}Creating client virtual environment...${NC}"
        python3 -m venv venv
    fi
    
    source venv/bin/activate
    
    # Install requirements if needed
    pip3 install -r requirements.txt >/dev/null 2>&1
    
    # Start client in background
    nohup streamlit run app.py --server.port 8501 --server.address 0.0.0.0 > ../logs/client.log 2>&1 &
    CLIENT_PID=$!
    echo $CLIENT_PID > ../logs/client.pid
    
    # Wait for client to start
    echo -e "${YELLOW}Waiting for client to start...${NC}"
    for i in {1..30}; do
        if check_port 8501; then
            echo -e "${GREEN}✅ Client started successfully on port 8501${NC}"
            break
        fi
        sleep 1
        if [ $i -eq 30 ]; then
            echo -e "${RED}❌ Client failed to start${NC}"
            exit 1
        fi
    done
    
    cd "$SCRIPT_DIR"
}

# Create logs directory
mkdir -p logs

# Check if already running
if check_port 8000 && check_port 8501; then
    echo -e "${GREEN}✅ AI PDF Chatbot is already running!${NC}"
    echo -e "${BLUE}🌐 Frontend: http://localhost:8501${NC}"
    echo -e "${BLUE}🔧 Backend: http://localhost:8000${NC}"
    echo -e "${BLUE}📚 API Docs: http://localhost:8000/docs${NC}"
    exit 0
fi

# Kill existing processes if running
if [ -f "logs/server.pid" ]; then
    SERVER_PID=$(cat logs/server.pid)
    if ps -p $SERVER_PID > /dev/null 2>&1; then
        echo -e "${YELLOW}Stopping existing server...${NC}"
        kill $SERVER_PID
        sleep 2
    fi
fi

if [ -f "logs/client.pid" ]; then
    CLIENT_PID=$(cat logs/client.pid)
    if ps -p $CLIENT_PID > /dev/null 2>&1; then
        echo -e "${YELLOW}Stopping existing client...${NC}"
        kill $CLIENT_PID
        sleep 2
    fi
fi

# Start services
start_server
start_client

echo -e "${GREEN}🎉 AI PDF Chatbot started successfully!${NC}"
echo -e "${BLUE}🌐 Frontend: http://localhost:8501${NC}"
echo -e "${BLUE}🔧 Backend: http://localhost:8000${NC}"
echo -e "${BLUE}📚 API Docs: http://localhost:8000/docs${NC}"
echo -e "${YELLOW}📋 Logs: Check logs/server.log and logs/client.log${NC}"
echo -e "${YELLOW}🛑 To stop: Run ./stop.sh${NC}"
