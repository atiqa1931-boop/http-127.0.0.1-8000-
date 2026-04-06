from fastapi import UploadFile, HTTPException
import io
import docx
from pdfminer.high_level import extract_text as pdf_extract_text

async def handle_text_input(text: str) -> str:
    """
    Handles raw text input from the paste option.
    Ensures input is not empty.
    """
    if not text or not text.strip():
        raise HTTPException(status_code=400, detail="Text input is empty.")
    return text.strip()

async def handle_file_upload(file: UploadFile) -> str:
    """
    Handles uploaded files (.txt, .docx, .pdf). 
    Extracts text content based on file extension.
    """
    filename = file.filename.lower()
    content = await file.read()
    
    if filename.endswith(".txt"):
        try:
            text = content.decode("utf-8")
        except UnicodeDecodeError:
            try:
                # Try latin-1 if utf-8 fails
                text = content.decode("latin-1")
            except:
                raise HTTPException(status_code=400, detail="Error reading .txt file. Ensure it is text-encoded.")
    
    elif filename.endswith(".docx"):
        text = extract_text_from_docx(content)
        
    elif filename.endswith(".pdf"):
        text = extract_text_from_pdf(content)
        
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type. Please upload a .txt, .docx, or .pdf file.")

    if not text or not text.strip():
        raise HTTPException(status_code=400, detail="The uploaded file contains no readable text.")
        
    return text.strip()

def extract_text_from_docx(content: bytes) -> str:
    """Extracts text from a .docx file content."""
    try:
        doc = docx.Document(io.BytesIO(content))
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        return "\n".join(full_text)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading .docx file: {str(e)}")

def extract_text_from_pdf(content: bytes) -> str:
    """Extracts text from a .pdf file content using pdfminer."""
    try:
        text = pdf_extract_text(io.BytesIO(content))
        return text
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading .pdf file: {str(e)}")
