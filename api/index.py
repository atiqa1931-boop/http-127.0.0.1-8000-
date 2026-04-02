from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional
import os

from pipelines.p1_input_handling import handle_text_input, handle_file_upload
from pipelines.p2_preprocessing import preprocess_text

app = FastAPI(title="Proper Noun Consistency Checker")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint for processing text/file
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
        raise HTTPException(status_code=400, detail="No input provided. Upload a file or paste text.")

    # --- Pipeline 2: Text Preprocessing ---
    preprocessed_text = preprocess_text(raw_text)

    # --- Pipeline 11: System Integration (Runs P3-P9) ---
    from pipelines.p11_integration import run_analytical_pipelines
    analytics = run_analytical_pipelines(preprocessed_text)
    
    # Returning data for the UI Dashboard
    return {
        "status": "success",
        "extracted_text": raw_text,
        "preprocessed_text": preprocessed_text,
        "final_text": analytics["final_text"],
        "report": analytics["report"]
    }
    
from fastapi.responses import StreamingResponse
from pipelines.p10_file_export import export_to_docx

@app.post("/api/download-docx")
async def download_docx(text: str = Form(...)):
    """
    Pipeline 10 (File Export)
    Endpoint specifically for providing the docx file download stream.
    """
    byte_stream = export_to_docx(text)
    return StreamingResponse(
        byte_stream,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": "attachment; filename=corrected_document.docx"}
    )

# Ensure the frontend directory exists before mounting, mostly for safety
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
