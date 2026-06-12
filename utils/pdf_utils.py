"""
Utility to extract text from an uploaded resume PDF.
"""

import PyPDF2


def extract_text_from_pdf(uploaded_file) -> str:
    """Extract all text from an uploaded PDF file (Streamlit UploadedFile)."""
    reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text.strip()
