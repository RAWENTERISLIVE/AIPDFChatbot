# 🚀 Latest Gemini Models Integration & Rate Limit Handling

## Overview
RagBot now supports the latest cutting-edge Gemini models with enhanced precision and performance for RAG (Retrieval-Augmented Generation) applications. It also features a robust rate limit handling mechanism with model fallback.

## 🤖 Available Models (Prioritized)

The system will attempt to use models in the following order if the initially requested model (or the top priority model if none is specified) encounters a rate limit:

### 1. **Gemini 2.5 Pro Preview (New)** 🏆 Top Priority
- **Model ID**: `models/gemini-2.5-pro-preview-03-25`
- **Priority**: 1
- **Release**: March 2025 (Preview)
- **Description**: Next-generation model with highest quota and latest features.
- **Best For**: Complex problem-solving, creative content generation, in-depth analysis, cutting-edge applications.
- **Performance**: State-of-the-art, offering significant improvements over previous versions.

### 2. **Gemini 2.0 Flash (Experimental)** ⚡ Fastest
- **Model ID**: `models/gemini-2.0-flash-exp`
- **Priority**: 2
- **Release**: December 2024
- **Description**: Latest multimodal model with enhanced reasoning and flash speed.
- **Best For**: General use, reasoning, coding, multimodal tasks.
- **Performance**: Fastest response times with maintained quality.

### 3. **Gemini 1.5 Pro (Latest)** 🛡️ Most Stable
- **Model ID**: `gemini-1.5-pro-latest`
- **Priority**: 3
- **Release**: December 2024
- **Description**: Latest stable version of Gemini 1.5 Pro with improved capabilities.
- **Best For**: General use, reliable responses, production.
- **Performance**: Most stable and reliable.

### 4. **Gemini 1.5 Flash (Latest)** ⚡ Speed Optimized
- **Model ID**: `gemini-1.5-flash-latest`
- **Priority**: 4
- **Release**: December 2024
- **Description**: Latest stable version of Gemini 1.5 Flash with enhanced speed.
- **Best For**: Speed, efficiency, quick tasks.
- **Performance**: Optimized for speed.

### 5. **Gemini 1.5 Pro** 🛡️ Stable
- **Model ID**: `models/gemini-1.5-pro`
- **Priority**: 5
- **Release**: May 2024
- **Description**: Stable high-performance model with proven reliability.
- **Best For**: General use, reliable responses, production.
- **Performance**: Stable and reliable.

### 6. **Gemini 1.5 Flash** ⚡ Fast
- **Model ID**: `models/gemini-1.5-flash`
- **Priority**: 6
- **Release**: May 2024
- **Description**: Fast and efficient model optimized for quick responses.
- **Best For**: Speed, efficiency, quick tasks.
- **Performance**: Optimized for speed.

## 🚦 Rate Limit Handling & Model Fallback

- **Automatic Fallback**: If the selected Gemini model (or the highest priority model if none is specified) hits a rate limit (HTTP 429 error), the system will automatically attempt to use the next available model in the priority list.
- **Retry Mechanism**: A short delay is introduced before retrying with the next model to allow transient issues to resolve.
- **User Notification**:
    - If a fallback occurs, the user will be notified which model was ultimately used.
    - If all models become unavailable due to persistent rate limits or other issues, the user will receive a message indicating that the service is temporarily unavailable.

## 🎛️ Enhanced Configuration

### Temperature Control
- **Range**: 0.0 - 1.0 (adjustable in UI)
- **Default**: 0.1 (high precision)
- **Lower values**: More precise and deterministic
- **Higher values**: More creative and varied

### Advanced Parameters
- **Top-P**: 0.8 (nucleus sampling for quality)
- **Top-K**: 40 (diversity control)
- **Max Tokens**: 8192 per model
- **Enhanced Retrieval**: k=5 documents per query

## 🔧 API Enhancements

### New Endpoints

#### `/models` - Get Available Models
```bash
GET http://localhost:8000/models
```
Returns all available models with their capabilities, performance characteristics, and metadata.

#### `/ask/` - Enhanced Query with Model Selection
```bash
POST http://localhost:8000/ask/
Content-Type: application/x-www-form-urlencoded

question=Your question here
model_name=gemini-exp-1206
temperature=0.1
```

Parameters:
- `question` (required): The question to ask
- `model_name` (optional): Model to use (defaults to `gemini-exp-1206`)
- `temperature` (optional): Response creativity (defaults to 0.1)

## 🎨 UI Enhancements

### Model Selection Sidebar
- **Visual Model Cards**: Each model shows performance badge and description
- **Real-time Selection**: Switch models without restarting
- **Temperature Slider**: Adjust creativity/precision in real-time
- **Model Metadata**: View release date, best use cases, and performance characteristics

### Enhanced Chat Experience
- **Model Indicator**: Shows which model is processing your query
- **Performance Badges**: Visual indicators for model strengths
- **Loading States**: Clear feedback during processing

## 🚀 Performance Optimizations

### Enhanced PDF Processing
- **OCR Support**: Automatic fallback for scanned documents
- **Text Extraction**: Improved extraction from various PDF formats
- **Error Handling**: Robust processing with detailed error reporting

### Improved Retrieval
- **Better Context**: Increased document retrieval (k=5)
- **Enhanced Precision**: Custom prompt templates for accuracy
- **Source Attribution**: Clear source document references

## 🔄 Migration from Groq

### Completed Changes
1. **API Migration**: Full switch from Groq to Gemini AI Studio
2. **Model Upgrade**: Latest experimental models integrated
3. **Enhanced Embeddings**: Using `models/embedding-001`
4. **Improved Processing**: OCR support for all document types
5. **Better UI**: Model selection and temperature control

### Configuration
Ensure your `.env` file contains:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

## 📊 Model Comparison

| Model | Speed | Precision | Stability | Best For |
|-------|-------|-----------|-----------|----------|
| Gemini 2.5 Pro Preview | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Complex tasks, creative content |
| Gemini 2.0 Flash Exp | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | Fast general tasks |
| Gemini Exp 1206 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Critical analysis |
| Gemini Exp 1121 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | Research tasks |
| Gemini 1.5 Pro | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Production use |
| Gemini 1.5 Flash | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | Quick queries |

## 🛠️ Development Notes

### Code Structure
- **`modules/llm.py`**: Enhanced with latest models and precision settings
- **`main.py`**: Updated with model selection endpoints
- **`components/chatUI.py`**: Enhanced UI with model selection
- **`utils/api.py`**: Updated API client with model support

### Dependencies
All required packages installed:
- `langchain-google-genai`: Gemini integration
- `langchain-chroma`: Vector store
- `pytesseract`: OCR support
- `pdf2image`: PDF processing

## 🚀 Getting Started

1. **Start Server**:
   ```bash
   cd server
   python3 -m uvicorn main:app --host 0.0.0.0 --port 8000
   ```

2. **Start Client**:
   ```bash
   cd client
   streamlit run app.py
   ```

3. **Select Model**: Use the sidebar to choose your preferred model
4. **Upload PDFs**: Add your documents
5. **Ask Questions**: Chat with enhanced precision using latest models

The system is now fully optimized with the latest Gemini models for superior RAG performance!
