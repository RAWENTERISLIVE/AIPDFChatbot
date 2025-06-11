# 🧠 Modular### 🔥 Latest Features
- **Latest Gemini Models**: `models/gemini-2.5-pro-preview-03-25` (Top Priority), Gemini 2.0 Flash, Latest 1.5 Pro/Flash, and more. See `LATEST_MODELS.md` for full list and priorities.
- **Rate Limit Fallback**: Automatically switches to the next available model if the preferred one is rate-limited. Users are notified of fallbacks.
- **Enhanced Precision**: Configurable temperature and advanced parameters. PDF Chatbot with FastAPI, ChromaDB & Streamlit

## 🚀 **NOW WITH LATEST GEMINI MODELS & RATE LIMIT FALLBACK!**
### ⚡ Featuring Gemini 2.5 Pro Preview, Gemini 2.0 Flash, Experimental 1206, and Enhanced Precision
### 🚦 Robust handling of API rate limits with automatic model fallback.

## 🎥 Watch the Tutorial

[![Watch the video](assets/ragbot2.0.png)](https://youtu.be/TxtK6NUUklQ)

This project is a cutting-edge **Retrieval-Augmented Generation (RAG)** application that allows users to upload PDF documents and chat with an AI assistant powered by the **latest Gemini models**. It features a microservice architecture with a decoupled **FastAPI backend** and **Streamlit frontend**, using **ChromaDB** as the vector store and **Google's latest Gemini models** for superior performance and precision.

### 🔥 Latest Features
- **Latest Gemini Models**: `models/gemini-2.5-pro-preview-0325` (Top Priority), Gemini 2.0 Flash, Experimental 1206, 1121, and more. See `LATEST_MODELS.md` for full list and priorities.
- **Rate Limit Fallback**: Automatically switches to the next available model if the preferred one is rate-limited. Users are notified of fallbacks.
- **Enhanced Precision**: Configurable temperature and advanced parameters
- **OCR Support**: Process both text-based and scanned PDFs
- **Model Selection UI**: Choose the best model for your use case
- **Real-time Performance**: Lightning-fast responses with latest models

---

## 📂 Project Structure

```
ragbot2.0/
├── client/         # Streamlit Frontend
│   |──components/
|   |  |──chatUI.py
|   |  |──history_download.py
|   |  |──upload.py
|   |──utils/
|   |  |──api.py
|   |──app.py
|   |──config.py
├── server/         # FastAPI Backend
│   ├── chroma_store/ ....after run
|   |──modules/
│      ├── load_vectorestore.py
│      ├── llm.py
│      ├── pdf_handler.py
│      ├── query_handlers.py
|   |──uploaded_pdfs/ ....after run
│   ├── logger.py
│   └── main.py
└── README.md
```

---

## ✨ Features

- 📄 Upload and parse PDFs
- 🧠 Embed document chunks with HuggingFace embeddings
- 💂️ Store embeddings in ChromaDB
- 💬 Query documents using LLaMA3 via Groq
- 🌍 Microservice architecture (Streamlit client + FastAPI server)

---

## 🎓 How RAG Works

Retrieval-Augmented Generation (RAG) enhances LLMs by injecting external knowledge. Instead of relying solely on pre-trained data, the model retrieves relevant information from a vector database (like ChromaDB) and uses it to generate accurate, context-aware responses.

---

## 📊 Application Diagram

📄 [Download the Full Architecture PDF](assets/ragbot2.0.pdf)

---

## 🚀 Getting Started Locally

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