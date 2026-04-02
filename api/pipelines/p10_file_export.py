from io import BytesIO
import docx

def export_to_docx(text: str) -> BytesIO:
    """
    Pipeline 10: File Export Pipeline
    Generates a .docx file in-memory.
    """
    doc = docx.Document()
    doc.add_paragraph(text)
    
    # Save to a BytesIO stream
    byte_stream = BytesIO()
    doc.save(byte_stream)
    byte_stream.seek(0)
    
    return byte_stream
