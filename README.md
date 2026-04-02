# Proper Noun Consistency System

A modular web-based system designed to automatically detect, analyze, and standardize inconsistent spellings of proper nouns in text.

## Features
- **File Upload & Text Input**: Supports `.txt` and `.docx` files.
- **Pipeline-Based Analysis**: Processes text through multiple stages (Normalizer, Tokenizer, Pattern Analysis, Detection, Canonical Form Selection, and Correction).
- **Interactive Dashboard**: View and review detected inconsistencies.
- **Data Export**: Download the corrected text in `.txt` or `.docx` formats.

## Tech Stack
- **Backend**: Python (Flask/FastAPI)
- **Frontend**: Vanilla HTML5, CSS3, and JavaScript
- **Deployment**: Vercel-ready with serverless function support.

## Project Structure
- `backend/`: Core logic and processing pipelines.
- `frontend/`: User interface and interactive components.
- `project/`: Vercel API wrappers for serverless deployment.
- `requirements.txt`: List of Python dependencies.

## Local Setup
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```
3. Run the backend server:
   ```bash
   python backend/main.py
   ```
4. Open `frontend/index.html` in your browser.

## Deployment
The project is configured for easy deployment on **Vercel** (`vercel.json`) or **Render** (`render.yaml`).
