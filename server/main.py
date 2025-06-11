from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from modules.load_vectorstore import load_vectorstore
from modules.llm import get_llm_chain, get_available_models
from modules.query_handlers import query_chain
from logger import logger

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
    except Exception as exc:
        logger.exception("UNHANDLED EXCEPTION")
        return JSONResponse(status_code=500,content={"error":str(exc)})
    
@app.post("/upload_pdfs/")
async def upload_pdfs(files:List[UploadFile]=File(...)):
    try:
        logger.info(f"recieved {len(files)} files")
        load_vectorstore(files)
        logger.info("documents added to chroma")
        return {"message":"Files processed and vectorstore updated"}
    except Exception as e:
        logger.exception("Error during pdf upload")
        return JSONResponse(status_code=500,content={"error":str(e)})


@app.post("/ask/")
async def ask_question(question: str = Form(...), model_name: str = Form(None), temperature: float = Form(0.1)):
    """
    Ask a question with optional model selection and temperature control.
    
    Args:
        question: The question to ask
        model_name: Optional Gemini model to use (defaults to latest experimental)
        temperature: Temperature for response generation (0.0-2.0, lower = more precise)
    """
    try:
        logger.info(f"User query: {question}")
        logger.info(f"Model: {model_name or 'default'}, Temperature: {temperature}")
        
        from langchain_chroma import Chroma
        from langchain_google_genai import GoogleGenerativeAIEmbeddings
        from modules.load_vectorstore import PERSIST_DIR
        import os
        from dotenv import load_dotenv
        
        load_dotenv()
        
        vectorstore = Chroma(
            persist_directory=PERSIST_DIR,
            embedding_function=GoogleGenerativeAIEmbeddings(
                model="models/embedding-001",
                google_api_key=os.environ.get("GEMINI_API_KEY")
            )
        )
        
        # Use enhanced LLM chain with model selection
        chain = get_llm_chain(vectorstore, model_name=model_name, temperature=temperature)
        result = query_chain(chain, question)
        
        logger.info("Query successful")
        return result
    except Exception as e:
        logger.exception("Error processing question")
        return JSONResponse(status_code=500, content={"error": str(e)})



@app.get("/test")
async def test():
    return {"message": "Testing successful..."}


@app.get("/models")
async def get_models():
    """Get available Gemini models with their capabilities."""
    try:
        models = get_available_models()
        return {
            "available_models": models,
            "default_model": "gemini-exp-1206",
            "recommended_temperature": 0.1
        }
    except Exception as e:
        logger.exception("Error getting models")
        return JSONResponse(status_code=500, content={"error": str(e)})