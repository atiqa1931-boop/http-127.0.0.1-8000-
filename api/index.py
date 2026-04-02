from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional
import os
import sys

# Add current directory to path so imports work correctly on Vercel
sys.path.append(os.path.dirname(__file__))

from pipelines.p1_input_handling import handle_text_input, handle_file_upload
from pipelines.p2_preprocessing import preprocess_text
from pipelines.p11_integration import run_analytical_pipelines
from pipelines.p10_file_export import export_to_docx

app = FastAPI(title="Proper Noun Consistency Checker")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
async def health():
    return {"status": "ok"}

@app.post("/api/process")
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
        raise HTTPException(status_code=400, detail="No input provided.")

    # --- Pipeline 2: Text Preprocessing ---
    preprocessed_text = preprocess_text(raw_text)

    # --- Pipeline 11: System Integration (Runs P3-P9) ---
    analytics = run_analytical_pipelines(preprocessed_text)
    
    # Returning data for the UI Dashboard
    return {
        "status": "success",
        "extracted_text": raw_text,
        "preprocessed_text": preprocessed_text,
        "final_text": analytics["final_text"],
        "report": analytics["report"]
    }

@app.post("/api/download-docx")
async def download_docx(text: str = Form(...)):
    """
    Pipeline 10 (File Export)
    Endpoint for providing the docx file download stream.
    """
    byte_stream = export_to_docx(text)
    return StreamingResponse(
        byte_stream,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": "attachment; filename=corrected_document.docx"}
    )
