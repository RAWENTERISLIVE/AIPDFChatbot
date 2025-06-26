#!/bin/bash

# AI PDF Chatbot Status Script
# This script checks the status of both services

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}📊 AI PDF Chatbot Status${NC}"
echo "================================"

# Function to check if port is in use
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null ; then
        return 0
    else
        return 1
    fi
}

# Check server status
if check_port 8000; then
    echo -e "${GREEN}✅ FastAPI Server: Running (Port 8000)${NC}"
    echo -e "   📡 API Endpoint: http://localhost:8000"
    echo -e "   📚 API Docs: http://localhost:8000/docs"
else
    echo -e "${RED}❌ FastAPI Server: Not Running${NC}"
fi

# Check client status
if check_port 8501; then
    echo -e "${GREEN}✅ Streamlit Client: Running (Port 8501)${NC}"
    echo -e "   🌐 Web Interface: http://localhost:8501"
else
    echo -e "${RED}❌ Streamlit Client: Not Running${NC}"
fi

echo ""

# Check PID files
if [ -f "logs/server.pid" ]; then
    SERVER_PID=$(cat logs/server.pid)
    if ps -p $SERVER_PID > /dev/null 2>&1; then
        echo -e "${GREEN}Server PID: $SERVER_PID (Active)${NC}"
    else
        echo -e "${YELLOW}Server PID: $SERVER_PID (Stale)${NC}"
    fi
else
    echo -e "${YELLOW}No server PID file found${NC}"
fi

if [ -f "logs/client.pid" ]; then
    CLIENT_PID=$(cat logs/client.pid)
    if ps -p $CLIENT_PID > /dev/null 2>&1; then
        echo -e "${GREEN}Client PID: $CLIENT_PID (Active)${NC}"
    else
        echo -e "${YELLOW}Client PID: $CLIENT_PID (Stale)${NC}"
    fi
else
    echo -e "${YELLOW}No client PID file found${NC}"
fi

echo ""

# Overall status
if check_port 8000 && check_port 8501; then
    echo -e "${GREEN}🎉 AI PDF Chatbot is fully operational!${NC}"
    echo -e "${BLUE}💡 Access the application at: http://localhost:8501${NC}"
elif check_port 8000 || check_port 8501; then
    echo -e "${YELLOW}⚠️ AI PDF Chatbot is partially running${NC}"
    echo -e "${YELLOW}💡 Run ./start.sh to start all services${NC}"
else
    echo -e "${RED}💥 AI PDF Chatbot is not running${NC}"
    echo -e "${BLUE}💡 Run ./start.sh to start the application${NC}"
fi
