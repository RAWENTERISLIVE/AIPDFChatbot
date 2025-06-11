import os
import time
from pathlib import Path
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from .enhanced_pdf_loader import EnhancedPDFLoader
import google.api_core.exceptions  # For catching rate limit errors
from typing import List

load_dotenv()



PERSIST_DIR="./chroma_store"
UPLOAD_DIR="./uploaded_pdfs"
os.makedirs(UPLOAD_DIR,exist_ok=True)

# Available embedding models in order of preference/fallback
EMBEDDING_MODELS = [
    "models/embedding-001",  # Stable embedding model
    "models/text-embedding-004",  # Alternative if available
    "models/gemini-embedding-exp-03-07"  # Experimental model (original)
]

def create_embeddings_with_retry(api_key: str, max_retries: int = 3) -> GoogleGenerativeAIEmbeddings:
    """
    Create embeddings with retry logic and model fallback for rate limits.
    
    Args:
        api_key: Gemini API key
        max_retries: Maximum number of retry attempts per model
    
    Returns:
        GoogleGenerativeAIEmbeddings instance
    
    Raises:
        Exception: If all models and retries are exhausted
    """
    
    for model_name in EMBEDDING_MODELS:
        print(f"🔄 Attempting to use embedding model: {model_name}")
        
        for attempt in range(max_retries):
            try:
                embeddings = GoogleGenerativeAIEmbeddings(
                    model=model_name,
                    google_api_key=api_key
                )
                
                # Test the embedding with a small text to verify it works
                test_result = embeddings.embed_query("test")
                if test_result:
                    print(f"✅ Successfully initialized embedding model: {model_name}")
                    return embeddings
                    
            except google.api_core.exceptions.ResourceExhausted as e:
                retry_delay = min(2 ** attempt, 30)  # Exponential backoff, max 30 seconds
                print(f"⚠️ Rate limit hit for {model_name} (attempt {attempt + 1}/{max_retries}): {e}")
                
                if attempt < max_retries - 1:
                    print(f"⏳ Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    print(f"❌ Max retries reached for {model_name}, trying next model...")
                    break
                    
            except Exception as e:
                print(f"❌ Error with embedding model {model_name} (attempt {attempt + 1}/{max_retries}): {e}")
                
                if attempt < max_retries - 1:
                    retry_delay = min(2 ** attempt, 10)  # Shorter delay for general errors
                    print(f"⏳ Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    print(f"❌ Max retries reached for {model_name}, trying next model...")
                    break
    
    raise Exception("All embedding models failed after multiple retries. Please check your API quota and try again later.")

def add_documents_with_retry(vectorstore: Chroma, texts: List, max_retries: int = 3):
    """
    Add documents to vectorstore with retry logic for rate limits.
    
    Args:
        vectorstore: Chroma vectorstore instance
        texts: List of document texts to add
        max_retries: Maximum number of retry attempts
    """
    
    for attempt in range(max_retries):
        try:
            print(f"📄 Adding {len(texts)} documents to vectorstore (attempt {attempt + 1}/{max_retries})")
            vectorstore.add_documents(texts)
            print("✅ Documents successfully added to vectorstore")
            return
            
        except google.api_core.exceptions.ResourceExhausted as e:
            retry_delay = min(2 ** attempt * 5, 60)  # Exponential backoff, max 60 seconds
            print(f"⚠️ Rate limit hit while adding documents (attempt {attempt + 1}/{max_retries}): {e}")
            
            if attempt < max_retries - 1:
                print(f"⏳ Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                raise Exception("Failed to add documents after multiple retries due to rate limits. Please try again later.")
                
        except Exception as e:
            print(f"❌ Error adding documents (attempt {attempt + 1}/{max_retries}): {e}")
            
            if attempt < max_retries - 1:
                retry_delay = min(2 ** attempt * 2, 20)  # Shorter delay for general errors
                print(f"⏳ Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                raise Exception(f"Failed to add documents after multiple retries: {e}")

def create_vectorstore_with_retry(texts: List, embeddings: GoogleGenerativeAIEmbeddings, max_retries: int = 3) -> Chroma:
    """
    Create vectorstore from documents with retry logic for rate limits.
    
    Args:
        texts: List of document texts
        embeddings: Embeddings instance
        max_retries: Maximum number of retry attempts
    
    Returns:
        Chroma vectorstore instance
    """
    
    for attempt in range(max_retries):
        try:
            print(f"🏗️ Creating new vectorstore with {len(texts)} documents (attempt {attempt + 1}/{max_retries})")
            vectorstore = Chroma.from_documents(
                documents=texts,
                embedding=embeddings,
                persist_directory=PERSIST_DIR
            )
            print("✅ Vectorstore successfully created")
            return vectorstore
            
        except google.api_core.exceptions.ResourceExhausted as e:
            retry_delay = min(2 ** attempt * 10, 120)  # Exponential backoff, max 2 minutes
            print(f"⚠️ Rate limit hit while creating vectorstore (attempt {attempt + 1}/{max_retries}): {e}")
            
            if attempt < max_retries - 1:
                print(f"⏳ Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                raise Exception("Failed to create vectorstore after multiple retries due to rate limits. Please try again later.")
                
        except Exception as e:
            print(f"❌ Error creating vectorstore (attempt {attempt + 1}/{max_retries}): {e}")
            
            if attempt < max_retries - 1:
                retry_delay = min(2 ** attempt * 5, 30)  # Shorter delay for general errors
                print(f"⏳ Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                raise Exception(f"Failed to create vectorstore after multiple retries: {e}")


def load_vectorstore(uploaded_files):
    """
    Load documents into vectorstore with comprehensive error handling and retry logic.
    
    Args:
        uploaded_files: List of uploaded file objects
    
    Returns:
        Chroma vectorstore instance
    
    Raises:
        ValueError: If no documents can be loaded or processed
        Exception: If vectorstore creation fails after retries
    """
    
    print(f"📁 Processing {len(uploaded_files)} uploaded files")
    file_paths = []

    # Save uploaded files
    for file in uploaded_files:
        save_path = Path(UPLOAD_DIR) / file.filename
        with open(save_path, "wb") as f:
            f.write(file.file.read())
        file_paths.append(str(save_path))

    # Load documents from files
    docs = []
    for path in file_paths:
        try:
            print(f"📖 Loading document: {path}")
            loader = EnhancedPDFLoader(path)
            loaded_docs = loader.load()
            docs.extend(loaded_docs)
            print(f"✅ Successfully loaded {len(loaded_docs)} document chunks from {path}")
        except Exception as e:
            print(f"⚠️ Warning: Failed to load {path}: {e}")
            continue

    if not docs:
        raise ValueError("No documents were loaded from the uploaded files. Please check if the files are valid PDFs.")

    print(f"📚 Total documents loaded: {len(docs)}")

    # Split documents into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    texts = splitter.split_documents(docs)

    if not texts:
        raise ValueError("No text was extracted from the documents after splitting.")

    print(f"📄 Total text chunks created: {len(texts)}")

    # Create embeddings with retry logic
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is not set")
        
    try:
        embeddings = create_embeddings_with_retry(
            api_key=api_key,
            max_retries=3
        )
    except Exception as e:
        raise Exception(f"Failed to initialize embeddings: {e}")

    # Check if vectorstore already exists and add documents or create new one
    try:
        if os.path.exists(PERSIST_DIR) and os.listdir(PERSIST_DIR):
            print("📦 Loading existing vectorstore")
            vectorstore = Chroma(persist_directory=PERSIST_DIR, embedding_function=embeddings)
            
            # Add new documents with retry logic
            add_documents_with_retry(vectorstore, texts, max_retries=3)
        else:
            print("🆕 Creating new vectorstore")
            # Create new vectorstore with retry logic
            vectorstore = create_vectorstore_with_retry(texts, embeddings, max_retries=3)

        print("🎉 Vectorstore successfully updated!")
        return vectorstore
        
    except Exception as e:
        # Clean up any partially created vectorstore on failure
        if os.path.exists(PERSIST_DIR):
            try:
                import shutil
                shutil.rmtree(PERSIST_DIR)
                print("🧹 Cleaned up partial vectorstore on failure")
            except:
                pass
        raise Exception(f"Failed to create or update vectorstore: {e}")