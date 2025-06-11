import os
from pathlib import Path
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from .enhanced_pdf_loader import EnhancedPDFLoader

load_dotenv()



PERSIST_DIR="./chroma_store"
UPLOAD_DIR="./uploaded_pdfs"
os.makedirs(UPLOAD_DIR,exist_ok=True)


def load_vectorstore(uploaded_files):
    file_paths=[]

    for file in uploaded_files:
        save_path=Path(UPLOAD_DIR)/file.filename
        with open(save_path,"wb") as f:
            f.write(file.file.read())
        file_paths.append(str(save_path))

    docs=[]
    for path in file_paths:
        loader=EnhancedPDFLoader(path)
        docs.extend(loader.load())

    if not docs:
        raise ValueError("No documents were loaded from the uploaded files")

    splitter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=100)
    texts=splitter.split_documents(docs)

    if not texts:
        raise ValueError("No text was extracted from the documents")

    embeddings=GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-exp-03-07",
        google_api_key=os.environ.get("GEMINI_API_KEY")
    )

    if os.path.exists(PERSIST_DIR) and os.listdir(PERSIST_DIR):
        vectorstore=Chroma(persist_directory=PERSIST_DIR,embedding_function=embeddings)
        vectorstore.add_documents(texts)
    else:
        vectorstore=Chroma.from_documents(
            documents=texts,
            embedding=embeddings,
            persist_directory=PERSIST_DIR
        )

    return vectorstore