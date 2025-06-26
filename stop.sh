#!/bin/bash

# AI PDF Chatbot Stop Script
# This script stops both the FastAPI server and Streamlit client

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🛑 Stopping AI PDF Chatbot...${NC}"

# Get the directory of this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Function to stop process by PID file
stop_process() {
    local service_name=$1
    local pid_file=$2
    
    if [ -f "$pid_file" ]; then
        PID=$(cat "$pid_file")
        if ps -p $PID > /dev/null 2>&1; then
            echo -e "${YELLOW}Stopping $service_name (PID: $PID)...${NC}"
            kill $PID
            sleep 3
            
            # Force kill if still running
            if ps -p $PID > /dev/null 2>&1; then
                echo -e "${YELLOW}Force stopping $service_name...${NC}"
                kill -9 $PID
            fi
            
            echo -e "${GREEN}✅ $service_name stopped${NC}"
        else
            echo -e "${YELLOW}$service_name was not running${NC}"
        fi
        rm -f "$pid_file"
    else
        echo -e "${YELLOW}No PID file found for $service_name${NC}"
    fi
}

# Stop processes using PID files
stop_process "Server" "logs/server.pid"
stop_process "Client" "logs/client.pid"

# Also kill any remaining processes on the ports
echo -e "${YELLOW}Checking for remaining processes...${NC}"

# Kill processes on port 8000 (FastAPI)
SERVER_PIDS=$(lsof -ti:8000)
if [ ! -z "$SERVER_PIDS" ]; then
    echo -e "${YELLOW}Stopping remaining server processes...${NC}"
    echo $SERVER_PIDS | xargs kill -9 2>/dev/null
fi

# Kill processes on port 8501 (Streamlit)
CLIENT_PIDS=$(lsof -ti:8501)
if [ ! -z "$CLIENT_PIDS" ]; then
    echo -e "${YELLOW}Stopping remaining client processes...${NC}"
    echo $CLIENT_PIDS | xargs kill -9 2>/dev/null
fi

echo -e "${GREEN}🎉 AI PDF Chatbot stopped successfully!${NC}"
