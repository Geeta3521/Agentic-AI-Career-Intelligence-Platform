"""utils/pdf_parser.py"""
import io


def extract_pdf(uploaded_file) -> str:
    text = ""
    try:
        import pdfplumber
        with pdfplumber.open(io.BytesIO(uploaded_file.read())) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    text += t + "\n"
        uploaded_file.seek(0)
        if text.strip():
            return text.strip()
    except Exception:
        pass
    try:
        import fitz
        uploaded_file.seek(0)
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        for page in doc:
            text += page.get_text() + "\n"
        uploaded_file.seek(0)
    except Exception:
        pass
    return text.strip() or "Could not extract text from PDF."
