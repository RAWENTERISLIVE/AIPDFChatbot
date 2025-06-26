#!/bin/bash

# AI PDF Chatbot Auto-Startup Disable Script
# This script disables automatic startup for macOS

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🛑 Disabling AI PDF Chatbot Auto-Startup${NC}"

PLIST_FILE="com.aipdchatbot.startup.plist"
LAUNCHAGENTS_DIR="$HOME/Library/LaunchAgents"

# Check if LaunchAgent exists
if [ -f "$LAUNCHAGENTS_DIR/$PLIST_FILE" ]; then
    echo -e "${YELLOW}📋 Unloading LaunchAgent...${NC}"
    
    # Unload the LaunchAgent
    if launchctl unload "$LAUNCHAGENTS_DIR/$PLIST_FILE" 2>/dev/null; then
        echo -e "${GREEN}✅ LaunchAgent unloaded successfully${NC}"
    else
        echo -e "${YELLOW}⚠️ LaunchAgent was not loaded${NC}"
    fi
    
    # Remove the plist file
    rm -f "$LAUNCHAGENTS_DIR/$PLIST_FILE"
    echo -e "${GREEN}✅ LaunchAgent removed successfully${NC}"
    
    echo -e "${GREEN}🎉 Auto-startup disabled successfully!${NC}"
    echo -e "${YELLOW}💡 The application will no longer start automatically${NC}"
    echo -e "${BLUE}To start manually, run: ./start.sh${NC}"
else
    echo -e "${YELLOW}⚠️ Auto-startup was not enabled${NC}"
fi
