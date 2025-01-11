import os
import fitz  # PyMuPDF
from App.nlp.query_with_langchain import query_with_langchain

UPLOAD_DIR = "APP/storage/"

def save_pdf(file):
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    return file_path

def extract_text(file_path):
    text = ""
    with fitz.open(file_path) as pdf:
        for page in pdf:
            text += page.get_text()
    return text

def process_question(file_id, question):
    file_path = os.path.join(UPLOAD_DIR, file_id)
    # Ensure query_with_langchain is callable
    if not callable(query_with_langchain):
        raise TypeError(f"query_with_langchain is not callable: {query_with_langchain}")
    return query_with_langchain(file_path, question)
