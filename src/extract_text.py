import fitz  # PyMuPDF
import io

def extract_text(uploaded_file):
    # uploaded_file is a stream (BytesIO), not a path
    pdf_bytes = uploaded_file.read()       # read bytes
    pdf_stream = io.BytesIO(pdf_bytes)     # convert to stream
    doc = fitz.open(stream=pdf_stream, filetype="pdf")
    
    text = ""
    for page in doc:
        text += page.get_text()
    return text
