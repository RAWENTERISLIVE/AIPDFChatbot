import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from typing import Optional

load_dotenv()

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# Latest Gemini models with their capabilities
AVAILABLE_MODELS = {
    "gemini-2.0-flash-exp": {
        "name": "Gemini 2.0 Flash (Experimental)",
        "description": "Latest multimodal model with enhanced reasoning and flash speed",
        "temperature_range": (0.0, 2.0),
        "max_tokens": 8192,
        "best_for": ["general", "reasoning", "coding", "multimodal"],
        "performance": "⚡ Fastest",
        "release": "2024-12"
    },
    "gemini-exp-1206": {
        "name": "Gemini Experimental 1206", 
        "description": "Advanced experimental model with improved capabilities and precision",
        "temperature_range": (0.0, 2.0),
        "max_tokens": 8192,
        "best_for": ["complex_reasoning", "analysis", "precision"],
        "performance": "🎯 Most Precise",
        "release": "2024-12"
    },
    "gemini-exp-1121": {
        "name": "Gemini Experimental 1121",
        "description": "Enhanced experimental model for precision tasks and deep analysis",
        "temperature_range": (0.0, 2.0), 
        "max_tokens": 8192,
        "best_for": ["precision", "analysis", "research"],
        "performance": "📊 Analytical",
        "release": "2024-11"
    },
    "gemini-1.5-pro": {
        "name": "Gemini 1.5 Pro",
        "description": "Stable high-performance model with proven reliability",
        "temperature_range": (0.0, 2.0),
        "max_tokens": 8192,
        "best_for": ["general", "reliable", "production"],
        "performance": "🛡️ Most Stable",
        "release": "2024-05"
    },
    "gemini-1.5-flash": {
        "name": "Gemini 1.5 Flash", 
        "description": "Fast and efficient model optimized for quick responses",
        "temperature_range": (0.0, 2.0),
        "max_tokens": 8192,
        "best_for": ["speed", "efficiency", "quick_tasks"],
        "performance": "⚡ Speed Optimized",
        "release": "2024-05"
    }
}

def get_llm_chain(vectorstore, model_name: Optional[str] = None, temperature: float = 0.1):
    """
    Create LLM chain with specified model and enhanced precision settings.
    
    Args:
        vectorstore: The vector store for retrieval
        model_name: Gemini model to use (defaults to latest experimental)
        temperature: Temperature for response generation (lower = more precise)
    """
    
    # Default to latest experimental model for best precision
    if model_name is None:
        model_name = "gemini-exp-1206"
    
    # Validate model
    if model_name not in AVAILABLE_MODELS:
        print(f"⚠️ Model {model_name} not found, using gemini-1.5-pro")
        model_name = "gemini-1.5-pro"
    
    model_info = AVAILABLE_MODELS[model_name]
    
    # Ensure temperature is within valid range
    min_temp, max_temp = model_info["temperature_range"]
    temperature = max(min_temp, min(max_temp, temperature))
    
    print(f"🤖 Using {model_info['name']} (temperature: {temperature})")
    
    llm = ChatGoogleGenerativeAI(
        google_api_key=GEMINI_API_KEY,
        model=model_name,
        temperature=temperature,
        max_tokens=model_info["max_tokens"],
        # Enhanced settings for better precision
        top_p=0.8,  # Nucleus sampling for better quality
        top_k=40,   # Top-k sampling for diversity control
    )
    
    # Enhanced retriever settings for better context
    retriever = vectorstore.as_retriever(
        search_kwargs={
            "k": 5,  # Retrieve more documents for better context
            "fetch_k": 10,  # Fetch more candidates before filtering
        }
    )
    
    return RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        # Add custom prompt template for better responses
        chain_type_kwargs={
            "prompt": get_custom_prompt_template()
        }
    )

def get_custom_prompt_template():
    """Enhanced prompt template for better precision and accuracy."""
    from langchain.prompts import PromptTemplate
    
    template = """You are an intelligent assistant that answers questions based on the provided context with high precision and accuracy.

Instructions:
1. Use ONLY the information provided in the context below
2. If the answer is not fully contained in the context, clearly state what information is missing
3. Provide detailed, accurate, and well-structured responses
4. Cite specific parts of the context when possible
5. If you're uncertain about any detail, express that uncertainty
6. Focus on being helpful while maintaining complete accuracy

Context:
{context}

Question: {question}

Answer: Let me analyze the provided context to give you a precise and accurate response."""

    return PromptTemplate(
        template=template,
        input_variables=["context", "question"]
    )

def get_available_models():
    """Return information about available models."""
    return AVAILABLE_MODELS