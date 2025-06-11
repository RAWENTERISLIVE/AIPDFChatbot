import os
from pathlib import Path
from typing import List
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
import pytesseract
from pdf2image import convert_from_path
import tempfile
from PIL import Image


class EnhancedPDFLoader:
    """
    Enhanced PDF loader that can handle both text-based and image-based (scanned) PDFs.
    Uses PyPDFLoader for text extraction and OCR (Tesseract) for scanned documents.
    """
    
    def __init__(self, file_path: str):
        self.file_path = file_path
    
    def load(self) -> List[Document]:
        """Load and extract text from PDF using text extraction and OCR fallback."""
        
        # First, try standard text extraction
        try:
            loader = PyPDFLoader(self.file_path)
            docs = loader.load()
            
            # Check if we got meaningful text content
            total_text_length = sum(len(doc.page_content.strip()) for doc in docs)
            
            if total_text_length > 50:  # If we have substantial text content
                print(f"✓ Extracted text from PDF using standard method: {total_text_length} characters")
                return docs
            else:
                print("⚠ Standard text extraction yielded minimal content, trying OCR...")
                return self._load_with_ocr()
                
        except Exception as e:
            print(f"⚠ Standard text extraction failed: {e}, trying OCR...")
            return self._load_with_ocr()
    
    def _load_with_ocr(self) -> List[Document]:
        """Extract text using OCR (Optical Character Recognition)."""
        
        try:
            # Convert PDF pages to images
            print("📄 Converting PDF pages to images...")
            pages = convert_from_path(self.file_path, dpi=300)
            
            documents = []
            
            for page_num, page_image in enumerate(pages, 1):
                print(f"🔍 Processing page {page_num}/{len(pages)} with OCR...")
                
                # Use Tesseract to extract text from the image
                text = pytesseract.image_to_string(page_image, lang='eng')
                
                # Create a document for this page
                if text.strip():  # Only add if there's actual text
                    doc = Document(
                        page_content=text,
                        metadata={
                            "source": self.file_path,
                            "page": page_num - 1,  # 0-indexed like PyPDFLoader
                            "extraction_method": "ocr"
                        }
                    )
                    documents.append(doc)
                else:
                    print(f"⚠ No text found on page {page_num}")
            
            total_text_length = sum(len(doc.page_content) for doc in documents)
            print(f"✓ OCR extraction completed: {len(documents)} pages, {total_text_length} characters")
            
            return documents
            
        except Exception as e:
            print(f"❌ OCR extraction failed: {e}")
            # Return empty document rather than failing completely
            return [Document(
                page_content=f"Failed to extract text from {os.path.basename(self.file_path)}. Error: {str(e)}",
                metadata={"source": self.file_path, "extraction_method": "failed"}
            )]
