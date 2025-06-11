import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from typing import Optional, Tuple, Dict, Any
import time
import google.api_core.exceptions # For catching rate limit errors

load_dotenv()

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# Latest Gemini models with their capabilities and priority (lower is higher)
AVAILABLE_MODELS: Dict[str, Dict[str, Any]] = {
    "models/gemini-2.5-pro-preview-03-25": { # Corrected model name
        "name": "Gemini 2.5 Pro Preview",
        "description": "Next-generation model with highest quota and latest features",
        "temperature_range": (0.0, 2.0),
        "max_tokens": 8192,
        "best_for": ["complex_reasoning", "coding", "multimodal", "high_volume"],
        "performance": "🚀 Top Tier",
        "release": "2025-03",
        "priority": 1 # Highest priority
    },
    "models/gemini-2.0-flash-exp": {
        "name": "Gemini 2.0 Flash (Experimental)",
        "description": "Latest multimodal model with enhanced reasoning and flash speed",
        "temperature_range": (0.0, 2.0),
        "max_tokens": 8192,
        "best_for": ["general", "reasoning", "coding", "multimodal"],
        "performance": "⚡ Fastest",
        "release": "2024-12",
        "priority": 2
    },
    "gemini-1.5-pro-latest": {
        "name": "Gemini 1.5 Pro (Latest)",
        "description": "Latest stable version of Gemini 1.5 Pro with improved capabilities",
        "temperature_range": (0.0, 2.0),
        "max_tokens": 8192,
        "best_for": ["general", "reliable", "production"],
        "performance": "🛡️ Most Stable",
        "release": "2024-12",
        "priority": 3
    },
    "gemini-1.5-flash-latest": {
        "name": "Gemini 1.5 Flash (Latest)",
        "description": "Latest stable version of Gemini 1.5 Flash with enhanced speed",
        "temperature_range": (0.0, 2.0),
        "max_tokens": 8192,
        "best_for": ["speed", "efficiency", "quick_tasks"],
        "performance": "⚡ Speed Optimized",
        "release": "2024-12",
        "priority": 4
    },
    "models/gemini-1.5-pro": {
        "name": "Gemini 1.5 Pro",
        "description": "Stable high-performance model with proven reliability",
        "temperature_range": (0.0, 2.0),
        "max_tokens": 8192,
        "best_for": ["general", "reliable", "production"],
        "performance": "🛡️ Stable",
        "release": "2024-05",
        "priority": 5
    },
    "models/gemini-1.5-flash": {
        "name": "Gemini 1.5 Flash", 
        "description": "Fast and efficient model optimized for quick responses",
        "temperature_range": (0.0, 2.0),
        "max_tokens": 8192,
        "best_for": ["speed", "efficiency", "quick_tasks"],
        "performance": "⚡ Fast",
        "release": "2024-05",
        "priority": 6
    }
}

# Sorted model list by priority for fallback
SORTED_MODELS_BY_PRIORITY = sorted(AVAILABLE_MODELS.items(), key=lambda item: item[1]["priority"])

def get_llm_instance(model_name: str, temperature: float) -> ChatGoogleGenerativeAI:
    """Helper function to create an LLM instance."""
    model_info = AVAILABLE_MODELS[model_name]
    min_temp, max_temp = model_info["temperature_range"]
    actual_temperature = max(min_temp, min(max_temp, temperature))

    print(f"🤖 Attempting to use {model_info['name']} (temperature: {actual_temperature})")
    
    return ChatGoogleGenerativeAI(
        google_api_key=GEMINI_API_KEY,
        model=model_name, # Use the full model name like "models/gemini-2.5-pro-preview-0325"
        temperature=actual_temperature,
        max_tokens=model_info["max_tokens"],
        top_p=0.8,
        top_k=40,
    )

def get_llm_chain(vectorstore, model_name: Optional[str] = None, temperature: float = 0.1, retry_count: int = 0) -> Tuple[Optional[RetrievalQA], Optional[str]]:
    """
    Create LLM chain with specified model, enhanced precision, and rate limit fallback.
    
    Args:
        vectorstore: The vector store for retrieval
        model_name: Gemini model to use (defaults to highest priority)
        temperature: Temperature for response generation
        retry_count: Internal counter for retries to prevent infinite loops
        
    Returns:
        A tuple containing the RetrievalQA chain and the name of the model used, or (None, None) if all fail.
    """
    
    if model_name is None:
        # Default to the highest priority model if none is specified
        model_name = SORTED_MODELS_BY_PRIORITY[0][0]
    
    # Validate model if a specific one is requested
    if model_name not in AVAILABLE_MODELS:
        print(f"⚠️ Model {model_name} not found. Falling back to highest priority: {SORTED_MODELS_BY_PRIORITY[0][0]}")
        model_name = SORTED_MODELS_BY_PRIORITY[0][0]

    current_model_index = -1
    for i, (m_name, _) in enumerate(SORTED_MODELS_BY_PRIORITY):
        if m_name == model_name:
            current_model_index = i
            break
    
    if current_model_index == -1: # Should not happen if model_name is validated
        print(f"Error: Could not find {model_name} in sorted list. Using highest priority.")
        current_model_index = 0
        model_name = SORTED_MODELS_BY_PRIORITY[0][0]

    # Iterate through models starting from the requested/default one, then by priority on error
    models_to_try = [m[0] for m in SORTED_MODELS_BY_PRIORITY[current_model_index:]] + \
                    [m[0] for m in SORTED_MODELS_BY_PRIORITY[:current_model_index]]


    for attempt_model_name in models_to_try:
        if retry_count >= len(AVAILABLE_MODELS) * 2: # Limit total retries to avoid deep loops
            print("❌ Maximum retry attempts reached. Aborting.")
            return None, None

        try:
            llm = get_llm_instance(attempt_model_name, temperature)
            
            retriever = vectorstore.as_retriever(
                search_kwargs={"k": 5}
            )
            
            chain = RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="stuff",
                retriever=retriever,
                return_source_documents=True,
                chain_type_kwargs={"prompt": get_custom_prompt_template()}
            )
            print(f"✅ Successfully created chain with {AVAILABLE_MODELS[attempt_model_name]['name']}")
            return chain, attempt_model_name

        except google.api_core.exceptions.ResourceExhausted as e:
            print(f"Rate limit hit for {AVAILABLE_MODELS[attempt_model_name]['name']}: {e}")
            retry_delay = 5 # Default retry delay
            if e.retry and hasattr(e.retry, 'delay'): # Check if retry info is available
                 retry_delay = e.retry.delay.total_seconds() if hasattr(e.retry.delay, 'total_seconds') else 5
            
            print(f"⏳ Retrying with next available model after {retry_delay} seconds...")
            time.sleep(retry_delay)
            # The loop will try the next model. We increment retry_count here.
            # No recursive call needed, the loop handles fallback.
        
        except Exception as e:
            print(f"❌ Error creating LLM chain with {AVAILABLE_MODELS[attempt_model_name]['name']}: {e}")
            # For other errors, also try the next model
            print("⏳ Trying next available model...")
            # No sleep for general errors, just try next model quickly.

    print("❌ All models failed after trying. No chain created.")
    return None, None

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