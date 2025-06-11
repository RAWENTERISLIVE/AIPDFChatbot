from fastapi import FastAPI, UploadFile, File, Form, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from modules.load_vectorstore import load_vectorstore, PERSIST_DIR # Import PERSIST_DIR
from modules.llm import get_llm_chain, get_available_models
from modules.query_handlers import query_chain
from logger import logger
import os
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

app = FastAPI(title="RagBot")

# allow frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.middleware("http")
async def catch_exception_middleware(request:Request,call_next):
    try:
        return await call_next(request)
    except HTTPException as http_exc: # Specifically handle HTTPExceptions to re-raise them
        logger.warning(f"HTTPException caught by middleware: {http_exc.status_code} {http_exc.detail}")
        raise http_exc
    except Exception as exc:
        logger.exception("UNHANDLED EXCEPTION IN MIDDLEWARE")
        return JSONResponse(status_code=500,content={"error":f"An internal server error occurred: {str(exc)}"})

@app.post("/upload_pdfs/")
async def upload_pdfs(files:List[UploadFile]=File(...)):
    try:
        logger.info(f"Received {len(files)} files for processing")
        
        # Validate files
        if not files:
            return JSONResponse(status_code=400, content={"error": "No files provided"})
        
        # Check file types
        invalid_files = [f.filename for f in files if not f.filename.lower().endswith('.pdf')]
        if invalid_files:
            return JSONResponse(
                status_code=400, 
                content={"error": f"Invalid file types detected. Only PDF files are allowed: {invalid_files}"}
            )
        
        logger.info("Starting vectorstore processing...")
        load_vectorstore(files)
        logger.info("Documents successfully added to chroma vectorstore")
        
        return {
            "message": f"Successfully processed {len(files)} PDF files and updated vectorstore",
            "files_processed": [f.filename for f in files]
        }
        
    except ValueError as ve:
        # Handle specific validation errors (e.g., no documents loaded, no text extracted)
        logger.warning(f"Validation error during PDF upload: {ve}")
        return JSONResponse(
            status_code=400, 
            content={
                "error": f"Document processing error: {str(ve)}",
                "suggestion": "Please ensure your PDFs contain readable text or images with text."
            }
        )
        
    except Exception as e:
        error_msg = str(e)
        logger.exception("Error during PDF upload")
        
        # Provide specific guidance for rate limit errors
        if "429" in error_msg or "Resource has been exhausted" in error_msg or "rate limit" in error_msg.lower():
            return JSONResponse(
                status_code=429, 
                content={
                    "error": "Rate limit exceeded for Gemini API",
                    "message": "Please wait a few minutes before uploading more files. The system will automatically retry with alternative models.",
                    "suggestion": "Consider uploading fewer files at once or wait for the rate limit to reset."
                }
            )
        
        # Provide specific guidance for API key errors
        if "api" in error_msg.lower() and ("key" in error_msg.lower() or "authentication" in error_msg.lower()):
            return JSONResponse(
                status_code=401, 
                content={
                    "error": "API authentication error",
                    "message": "There was an issue with the Gemini API configuration.",
                    "suggestion": "Please check that your GEMINI_API_KEY is properly configured."
                }
            )
        
        # Generic error response
        return JSONResponse(
            status_code=500, 
            content={
                "error": f"An error occurred while processing the files: {error_msg}",
                "suggestion": "Please try again. If the problem persists, check your files and API configuration."
            }
        )


@app.post("/ask/")
async def ask_question(question: str = Form(...), model_name: str = Form(None), temperature: float = Form(0.1)):
    """
    Ask a question with optional model selection and temperature control.
    
    Args:
        question: The question to ask
        model_name: Optional Gemini model to use (defaults to highest priority).
        temperature: Temperature for response generation (0.0-1.0, lower = more precise).
    """
    try:
        logger.info(f"User query: '{question}'")
        
        requested_model_for_response = model_name
        if not requested_model_for_response:
            available_models_dict = get_available_models() 
            if available_models_dict:
                sorted_by_priority = sorted(
                    available_models_dict.items(), 
                    key=lambda item: item[1].get('priority', float('inf'))
                )
                if sorted_by_priority:
                    requested_model_for_response = sorted_by_priority[0][0] 
                else:
                    requested_model_for_response = "default (unavailable)"
            else:
                requested_model_for_response = "default (config error)"
        
        logger.info(f"Requested Model: '{requested_model_for_response}', Temperature: {temperature}")
        
        load_dotenv()
        
        vectorstore = Chroma(
            persist_directory=PERSIST_DIR,
            embedding_function=GoogleGenerativeAIEmbeddings(
                model="models/embedding-001", 
                google_api_key=os.environ.get("GEMINI_API_KEY")
            )
        )
        
        chain, actual_model_used = get_llm_chain(
            vectorstore, 
            model_name=model_name, 
            temperature=temperature
        )
        
        if chain is None:
            logger.error(f"All AI models (requested: {model_name or 'default'}) failed to initialize after retries.")
            return JSONResponse(
                status_code=503,
                content={"error": "All AI models are currently unavailable due to high demand or rate limits. Please try again later."}
            )
        
        logger.info(f"Successfully initialized chain with model: '{actual_model_used}' (Requested: '{model_name or 'default'}')")
        
        result_data = query_chain(chain, question)
        
        response_content = {
            "answer": result_data.get("response"),  # Fixed: query_chain returns "response", not "answer"
            "source_documents": result_data.get("sources", []),  # Fixed: query_chain returns "sources", not "source_documents"
            "requested_model": requested_model_for_response, 
            "actual_model_used": actual_model_used
        }

        if model_name and model_name != actual_model_used:
            response_content["status_message"] = f"Requested model '{model_name}' was unavailable or encountered issues. Fallback to '{actual_model_used}' was used."
        elif not model_name and actual_model_used: 
            response_content["status_message"] = f"Using model '{actual_model_used}' by default."
        
        logger.info(f"Query successful. Model used: '{actual_model_used}'.")
        return JSONResponse(content=response_content)
        
    except HTTPException as http_exc: 
        logger.warning(f"HTTPException in /ask: {http_exc.status_code} - {http_exc.detail}")
        raise http_exc 
    except Exception as e:
        logger.exception(f"Error processing question in /ask endpoint (Query: '{question}', Model: {model_name})")
        return JSONResponse(status_code=500, content={"error": f"An unexpected server error occurred: {str(e)}"})

@app.get("/test")
async def test():
    return {"message": "Testing successful..."}


@app.get("/models")
async def get_models_endpoint(): # Renamed to avoid conflict with imported get_available_models
    """Get available Gemini models with their capabilities."""
    try:
        models = get_available_models()
        default_model_id = "gemini-exp-1206" 
        if models:
            sorted_by_priority = sorted(
                models.items(),
                key=lambda item: item[1].get('priority', float('inf'))
            )
            if sorted_by_priority:
                default_model_id = sorted_by_priority[0][0]

        return {
            "available_models": models,
            "default_model": default_model_id, 
            "recommended_temperature": 0.1
        }
    except Exception as e:
        logger.exception("Error getting models")
        return JSONResponse(status_code=500, content={"error": str(e)})