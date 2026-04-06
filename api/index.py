from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional
import os
import sys

# Ensure the 'api' directory is in the path for serverless environment
sys.path.append(os.path.dirname(__file__))

from pipelines.p1_input_handling import handle_text_input, handle_file_upload
from pipelines.p2_preprocessing import preprocess_text

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "Translation Consistency System API is running"}

# Endpoint for processing text/file
@app.post("/api/process")
@app.post("/process")
async def process_data(
    text: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None)
):
    # --- Pipeline 1: Input Handling ---
    if file:
        raw_text = await handle_file_upload(file)
    elif text:
        raw_text = await handle_text_input(text)
    else:
        raise HTTPException(status_code=400, detail="No input provided. Upload a file or paste text.")

    # --- Pipeline 2: Text Preprocessing ---
    preprocessed_text = preprocess_text(raw_text)

    # --- Pipeline 11: System Integration (Runs P3-P9) ---
    from pipelines.p11_integration import run_analytical_pipelines
    try:
        analytics = run_analytical_pipelines(preprocessed_text)
        
        # Returning data for the UI Dashboard
        return {
            "status": "success",
            "extracted_text": raw_text,
            "preprocessed_text": preprocessed_text,
            "final_text": analytics.get("final_text", raw_text),
            "report": analytics.get("report", {"total_corrections": 0, "details": []})
        }
    except Exception as e:
        # Catch unexpected errors in the pipeline to prevent hanging
        return {
            "status": "error",
            "detail": f"An error occurred during linguistic analysis: {str(e)}",
            "extracted_text": raw_text,
            "final_text": raw_text,
            "report": {"total_corrections": 0, "details": []}
        }
    
from fastapi.responses import StreamingResponse
from pipelines.p10_file_export import export_to_docx

@app.post("/api/download-docx")
@app.post("/download-docx")
async def download_docx(text: str = Form(...)):
    """
    Pipeline 10 (File Export)
    Endpoint specifically for providing the docx file download stream.
    """
    byte_stream = export_to_docx(text)
    return StreamingResponse(
        byte_stream,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": "attachment; filename=consistent_translation.docx"}
    )
