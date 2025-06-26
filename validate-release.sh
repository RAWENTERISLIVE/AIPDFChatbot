#!/bin/bash

# AI PDF Chatbot - Release Validation Script
# This script validates that all components are ready for production release

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔍 AI PDF Chatbot - Release Validation${NC}"
echo "==========================================="

# Track validation results
PASSED=0
FAILED=0

# Function to check if a file exists
check_file() {
    local file=$1
    local description=$2
    
    if [ -f "$file" ]; then
        echo -e "${GREEN}✅ $description${NC}"
        ((PASSED++))
    else
        echo -e "${RED}❌ $description - Missing: $file${NC}"
        ((FAILED++))
    fi
}

# Function to check if a script is executable
check_executable() {
    local file=$1
    local description=$2
    
    if [ -x "$file" ]; then
        echo -e "${GREEN}✅ $description${NC}"
        ((PASSED++))
    else
        echo -e "${RED}❌ $description - Not executable: $file${NC}"
        ((FAILED++))
    fi
}

# Function to check directory structure
check_directory() {
    local dir=$1
    local description=$2
    
    if [ -d "$dir" ]; then
        echo -e "${GREEN}✅ $description${NC}"
        ((PASSED++))
    else
        echo -e "${RED}❌ $description - Missing: $dir${NC}"
        ((FAILED++))
    fi
}

echo -e "${YELLOW}📋 Checking Core Files...${NC}"

# Check management scripts
check_file "start.sh" "Start script"
check_file "stop.sh" "Stop script"
check_file "status.sh" "Status script"
check_file "setup-autostart.sh" "Auto-startup setup script"
check_file "disable-autostart.sh" "Auto-startup disable script"

echo ""
echo -e "${YELLOW}🔧 Checking Script Permissions...${NC}"

# Check script executability
check_executable "start.sh" "Start script executable"
check_executable "stop.sh" "Stop script executable"
check_executable "status.sh" "Status script executable"
check_executable "setup-autostart.sh" "Setup script executable"
check_executable "disable-autostart.sh" "Disable script executable"

echo ""
echo -e "${YELLOW}📦 Checking System Files...${NC}"

# Check system integration files
check_file "com.aipdchatbot.startup.plist" "LaunchAgent plist file"

echo ""
echo -e "${YELLOW}📚 Checking Documentation...${NC}"

# Check documentation files
check_file "README.md" "Main README"
check_file "PRODUCTION_GUIDE.md" "Production deployment guide"
check_file "QUICK_START.md" "Quick start guide"
check_file "RELEASE_NOTES.md" "Release notes"
check_file "PRODUCTION_COMPLETION.md" "Production completion summary"

echo ""
echo -e "${YELLOW}🏗️ Checking Project Structure...${NC}"

# Check directory structure
check_directory "server" "Server directory"
check_directory "client" "Client directory"
check_file "server/main.py" "Server main file"
check_file "client/app.py" "Client main file"
check_file "server/requirements.txt" "Server requirements"
check_file "client/requirements.txt" "Client requirements"

echo ""
echo -e "${YELLOW}🔧 Checking Enhanced Modules...${NC}"

# Check enhanced modules
check_file "server/modules/load_vectorstore.py" "Enhanced vectorstore loader"
check_file "server/modules/llm.py" "Enhanced LLM module"
check_file "client/components/upload.py" "Enhanced upload component"

echo ""
echo -e "${YELLOW}📋 Checking Configuration Files...${NC}"

# Check configuration
check_file "server/.env.example" "Environment file example"

# Check if logs directory will be created
if [ ! -d "logs" ]; then
    echo -e "${YELLOW}⚠️ Logs directory will be created on first run${NC}"
else
    echo -e "${GREEN}✅ Logs directory exists${NC}"
    ((PASSED++))
fi

echo ""
echo "==========================================="

# Summary
echo -e "${BLUE}📊 Validation Summary:${NC}"
echo -e "${GREEN}✅ Passed: $PASSED${NC}"
echo -e "${RED}❌ Failed: $FAILED${NC}"

if [ $FAILED -eq 0 ]; then
    echo ""
    echo -e "${GREEN}🎉 All validation checks passed!${NC}"
    echo -e "${GREEN}🚀 AI PDF Chatbot is ready for production release!${NC}"
    echo ""
    echo -e "${BLUE}Next steps:${NC}"
    echo -e "1. Set your API key: ${YELLOW}echo 'GEMINI_API_KEY=your_key' > server/.env${NC}"
    echo -e "2. Setup auto-startup: ${YELLOW}./setup-autostart.sh${NC}"
    echo -e "3. Access application: ${YELLOW}http://localhost:8501${NC}"
    exit 0
else
    echo ""
    echo -e "${RED}❌ Validation failed! Please fix the missing components.${NC}"
    exit 1
fi
