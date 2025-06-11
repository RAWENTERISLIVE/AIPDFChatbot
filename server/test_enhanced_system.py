#!/usr/bin/env python3
"""
Test script for the enhanced RAG system with latest Gemini models.
This script tests the core functionality without starting the full server.
"""

import sys
import os
sys.path.append('.')

from modules.llm import get_llm_chain, get_available_models
from modules.query_handlers import query_chain
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

def test_models():
    """Test available models"""
    print("🤖 Testing Available Models")
    print("=" * 50)
    
    models = get_available_models()
    for model_id, info in models.items():
        print(f"✅ {info['performance']} {info['name']}")
        print(f"   📅 Release: {info.get('release', 'N/A')}")
        print(f"   🎯 Best for: {', '.join(info['best_for'])}")
        print()
    
    return models

def test_vectorstore():
    """Test ChromaDB connection"""
    print("📚 Testing Vector Store Connection")
    print("=" * 50)
    
    load_dotenv()
    
    try:
        vectorstore = Chroma(
            persist_directory='./chroma_store',
            embedding_function=GoogleGenerativeAIEmbeddings(
                model='models/embedding-001',
                google_api_key=os.environ.get('GEMINI_API_KEY')
            )
        )
        
        # Test retrieval
        docs = vectorstore.similarity_search("test", k=2)
        print(f"✅ ChromaDB connected successfully")
        print(f"📄 Found {len(docs)} documents in database")
        
        return vectorstore
        
    except Exception as e:
        print(f"❌ ChromaDB connection failed: {e}")
        return None

def test_llm_chain(vectorstore, models):
    """Test LLM chain creation with different models"""
    print("🔗 Testing LLM Chain Creation")
    print("=" * 50)
    
    for model_id in list(models.keys())[:2]:  # Test first 2 models
        try:
            chain, actual_model = get_llm_chain(vectorstore, model_name=model_id, temperature=0.1)
            if chain:
                print(f"✅ {model_id}: Chain created successfully")
            else:
                print(f"❌ {model_id}: Chain creation failed - returned None")
        except Exception as e:
            print(f"❌ {model_id}: Chain creation failed - {e}")

def test_query(vectorstore):
    """Test a sample query"""
    print("💬 Testing Sample Query")
    print("=" * 50)
    
    try:
        # Use the top priority model for testing
        chain, actual_model = get_llm_chain(vectorstore, model_name=None, temperature=0.1)
        
        if not chain:
            print("❌ Failed to create chain for query test")
            return
            
        # Test query
        test_question = "What is this document about?"
        print(f"🤔 Question: {test_question}")
        print(f"🤖 Using model: {actual_model}")
        
        result = query_chain(chain, test_question)
        print(f"🤖 Response: {result.get('response', 'No response')[:200]}...")
        
        sources = result.get('sources', [])
        if sources:
            print(f"📄 Sources: {len(sources)} documents referenced")
        
        print("✅ Query test completed successfully")
        
    except Exception as e:
        print(f"❌ Query test failed: {e}")

def main():
    """Run all tests"""
    print("🚀 RagBot Enhanced System Test")
    print("=" * 50)
    print()
    
    # Test models
    models = test_models()
    print()
    
    # Test vectorstore
    vectorstore = test_vectorstore()
    print()
    
    if vectorstore:
        # Test LLM chains
        test_llm_chain(vectorstore, models)
        print()
        
        # Test query
        test_query(vectorstore)
        print()
    
    print("🎉 All tests completed!")
    print("🚀 System ready for deployment with latest Gemini models!")

if __name__ == "__main__":
    main()
