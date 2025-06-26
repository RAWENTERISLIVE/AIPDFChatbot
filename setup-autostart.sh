#!/bin/bash

# AI PDF Chatbot Auto-Startup Setup Script
# This script sets up automatic startup for macOS

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔧 Setting up AI PDF Chatbot Auto-Startup${NC}"

# Get the directory of this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Update the plist file with correct path
PLIST_FILE="com.aipdchatbot.startup.plist"
LAUNCHAGENTS_DIR="$HOME/Library/LaunchAgents"

# Create LaunchAgents directory if it doesn't exist
mkdir -p "$LAUNCHAGENTS_DIR"

# Update plist file with current directory path
sed "s|/Users/raghav/Developer/AIPDFChatbot|$SCRIPT_DIR|g" "$PLIST_FILE" > "$LAUNCHAGENTS_DIR/$PLIST_FILE"

echo -e "${YELLOW}📋 Installing LaunchAgent...${NC}"

# Load the LaunchAgent
if launchctl load "$LAUNCHAGENTS_DIR/$PLIST_FILE" 2>/dev/null; then
    echo -e "${GREEN}✅ LaunchAgent installed successfully${NC}"
else
    echo -e "${YELLOW}⚠️ LaunchAgent was already loaded, reloading...${NC}"
    launchctl unload "$LAUNCHAGENTS_DIR/$PLIST_FILE" 2>/dev/null
    launchctl load "$LAUNCHAGENTS_DIR/$PLIST_FILE"
    echo -e "${GREEN}✅ LaunchAgent reloaded successfully${NC}"
fi

echo -e "${GREEN}🎉 Auto-startup setup complete!${NC}"
echo ""
echo -e "${BLUE}The AI PDF Chatbot will now:${NC}"
echo -e "• 🚀 Start automatically when you log in"
echo -e "• 🔄 Restart automatically if it crashes"
echo -e "• 📱 Run in the background persistently"
echo ""
echo -e "${YELLOW}💡 Useful commands:${NC}"
echo -e "• Check status: ${BLUE}./status.sh${NC}"
echo -e "• Stop manually: ${BLUE}./stop.sh${NC}"
echo -e "• Start manually: ${BLUE}./start.sh${NC}"
echo -e "• Disable auto-startup: ${BLUE}./disable-autostart.sh${NC}"
echo ""
echo -e "${GREEN}🌐 Your app will be available at: http://localhost:8501${NC}"
