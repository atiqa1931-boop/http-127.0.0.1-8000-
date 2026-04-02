from fastapi import UploadFile, HTTPException

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
    Handles uploaded text files. 
    Currently supports .txt files. Future pipelines will support .docx.
    """
    if file.filename.endswith(".txt"):
        content = await file.read()
        try:
            text = content.decode("utf-8")
            if not text.strip():
                raise HTTPException(status_code=400, detail="Uploaded file is empty.")
            return text.strip()
        except UnicodeDecodeError:
            raise HTTPException(status_code=400, detail="Error reading .txt file. Ensure it is utf-8 encoded.")
    else:
        # Fallback error for non-txt files at this stage
        raise HTTPException(status_code=400, detail="Unsupported file type. Please upload a .txt file.")
