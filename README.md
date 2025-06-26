### 🔥 Latest Features
- **🚀 Auto-Startup**: Application starts automatically on system boot with persistent background processes
- **💪 Production Ready**: Complete process management with crash recovery and graceful shutdown
- **🛡️ Enhanced Rate Limiting**: Intelligent retry logic with exponential backoff for Gemini API
- **📊 Status Monitoring**: Real-time process monitoring and comprehensive logging
- **🔧 Easy Management**: Simple scripts for start/stop/status operations
- **Latest Gemini Models**: `models/gemini-2.5-pro-preview-0325` (Top Priority), Gemini 2.0 Flash, Experimental 1206, 1121, and more. See `LATEST_MODELS.md` for full list and priorities.
- **Rate Limit Fallback**: Automatically switches to the next available model if the preferred one is rate-limited. Users are notified of fallbacks.
- **Enhanced Precision**: Configurable temperature and advanced parameters
- **OCR Support**: Process both text-based and scanned PDFs
- **Model Selection UI**: Choose the best model for your use case
- **Real-time Performance**: Lightning-fast responses with latest models

---

## ✨ Features

- 📄 Upload and parse PDFs
- 🧠 Embed document chunks with HuggingFace embeddings
- 💂️ Store embeddings in ChromaDB
- 💬 Query documents using Gemini via Google AI Studio
- 🌍 Microservice architecture (Streamlit client + FastAPI server)

---

## 🎓 How RAG Works

Retrieval-Augmented Generation (RAG) enhances LLMs by injecting external knowledge. Instead of relying solely on pre-trained data, the model retrieves relevant information from a vector database (like ChromaDB) and uses it to generate accurate, context-aware responses.

---

## 🚀 Getting Started (Production Ready)

### ⚡ Quick Start - 2 Minutes Setup
```bash
# 1. Clone the repository
git clone https://github.com/yourusername/AIPDFChatbot.git
cd AIPDFChatbot

# 2. Set your Gemini API Key (get it from https://makersuite.google.com/app/apikey)
echo "GEMINI_API_KEY=your_actual_gemini_api_key_here" > server/.env

# 3. One-time setup for auto-startup
./setup-autostart.sh
```

**🎉 That's it!** Your AI PDF Chatbot is now:
- ✅ **Running** at http://localhost:8501
- ✅ **Auto-starts** when your Mac boots up
- ✅ **Self-recovers** if it crashes
- ✅ **Runs 24/7** in the background
- ✅ **Zero maintenance** required

### 🛠️ Management Commands
```bash
./status.sh               # 📊 Check if services are running
./start.sh                # 🚀 Start manually (if needed)
./stop.sh                 # 🛑 Stop all services
./disable-autostart.sh    # ❌ Disable auto-startup
./validate-release.sh     # ✅ Validate installation
```

### 🌐 Access Your Application
- **Main Interface**: http://localhost:8501
- **API Endpoint**: http://localhost:8000  
- **API Documentation**: http://localhost:8000/docs

---

## 🛠️ Manual Setup (Alternative)

### 1. Clone the Repository

```bash
git clone https://github.com/snsupratim/ragbot.git
cd ragbot
```

### 2. Setup the Backend (FastAPI)

```bash
cd server
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt # Installs all dependencies including google-api-core for rate limit handling

# Set your Gemini API Key (IMPORTANT: Name changed from GROQ_API_KEY)
echo "GEMINI_API_KEY=your_key_here" > .env

# Run the FastAPI server
uvicorn main:app --reload
```

### 3. Setup the Frontend (Streamlit)

```bash
cd client
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
streamlit run app.py
```

### 4. Run the Application

```bash
cd server
python3 -m venv venv
source venv/bin/activate
uvicorn main:app --reload
```

```bash
cd client
python3 -m venv venv
source venv/bin/activate
streamlit run app.py
```
Open your browser and navigate to [http://localhost:8501]

---

## 🔧 Troubleshooting

### Common Issues

#### 🔑 API Key Issues
```bash
# Check if API key is set
cat server/.env
# Should show: GEMINI_API_KEY=your_key_here

# If missing, set it:
echo "GEMINI_API_KEY=your_actual_key" > server/.env
```

#### 🚫 Port Already in Use
```bash
# Stop all services first
./stop.sh

# Check what's using the ports
lsof -i :8000  # FastAPI server
lsof -i :8501  # Streamlit client

# Force kill if needed
sudo kill -9 <PID>

# Then start again
./start.sh
```

#### ❌ Application Not Starting
```bash
# Check status with detailed information
./status.sh

# Check logs for errors
tail -f logs/server.log
tail -f logs/client.log

# Validate installation
./validate-release.sh

# Reset everything if needed
./stop.sh
./disable-autostart.sh
rm -rf logs/*
./setup-autostart.sh
```

#### 🔄 Rate Limit Errors (429)
The application now automatically handles rate limits with:
- ✅ **Exponential backoff** retry logic
- ✅ **Model fallback** to alternative AI models
- ✅ **User-friendly error messages**

If you still encounter issues:
- Wait a few minutes and try again
- Check your API quota in Google AI Studio
- The system will automatically retry with different models

#### 🖥️ UI Issues
```bash
# Clear browser cache and reload
# Or try incognito/private browsing mode

# Restart the client only
./stop.sh
./start.sh
```

### 📋 Health Check Commands

```bash
# Quick status check
./status.sh

# Validate complete installation
./validate-release.sh

# View real-time logs
tail -f logs/server.log    # Backend logs
tail -f logs/client.log    # Frontend logs

# Monitor continuously
watch -n 5 ./status.sh
```

### 🔄 Reset Everything
If you encounter persistent issues:

```bash
# Complete reset procedure
./stop.sh                    # Stop all services
./disable-autostart.sh       # Disable auto-startup
rm -rf logs/*               # Clear logs
rm server/.env              # Remove API key (you'll need to re-add)
./validate-release.sh       # Validate clean state
```

Then start fresh:
```bash
echo "GEMINI_API_KEY=your_key" > server/.env
./setup-autostart.sh
```

---

## 📊 Performance Tips

### 🚀 Optimal Usage
- **PDF Size**: Keep PDFs under 50MB for best performance
- **Multiple Files**: Upload 5-10 PDFs at a time for optimal processing
- **Model Selection**: Use faster models for quick queries, precise models for complex questions
- **Clear Chat**: Restart the app if you experience slowdowns after extended use

### 💡 Best Practices
- **Regular Updates**: Keep your Gemini API key active and monitor usage
- **Log Monitoring**: Occasionally check logs for any warnings
- **Resource Management**: The app uses ~500MB-1GB RAM depending on document size

---

## 🆘 Need Help?

### 📞 Quick Diagnostics
1. **Run**: `./status.sh` for immediate status
2. **Check**: `logs/` directory for detailed error information  
3. **Validate**: `./validate-release.sh` for complete system check
4. **Reset**: Use the reset procedure above if issues persist

### 📚 Documentation
- **Quick Setup**: See `QUICK_START.md`
- **Production Guide**: See `PRODUCTION_GUIDE.md` 
- **Release Notes**: See `RELEASE_NOTES.md`

**The system is designed to be self-healing and user-friendly. Most issues resolve automatically!** 🎉