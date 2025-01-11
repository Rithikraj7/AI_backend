# from transformers import pipeline
# from PyPDF2 import PdfReader
#
# def extract_text_from_pdf(file_path):
#     """Extract text from a PDF file."""
#     reader = PdfReader(file_path)
#     text = ""
#     for page in reader.pages:
#         text += page.extract_text()
#     return text
#
# def query_with_langchain(file_path, question):
#     """Query a PDF document using a Hugging Face model."""
#     # Extract text from PDF
#     context = extract_text_from_pdf(file_path)
#
#     # Initialize the Hugging Face pipeline for Question Answering
#     nlp = pipeline("question-answering", model="deepset/roberta-base-squad2")
#
#     # Run the QA model with the extracted context and provided question
#     result = nlp(question=question, context=context)
#
#     return result['answer']


import openai
from langchain_community.document_loaders import PyPDFLoader
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Set your OpenAI API key
openai.api_key = os.getenv("API_KEY")

# Function to extract the context from the PDF using LangChain
def extract_pdf_content(file_path):
    loader = PyPDFLoader(file_path)
    pages = loader.load_and_split()  # Load and split the PDF into pages
    return pages

# Function to perform Question Answering using OpenAI's Chat API
def question_answering_with_openai(question, context):
    # Use the ChatCompletion API
    messages = [
        {"role": "system", "content": "You are an AI assistant that answers questions based only on the provided context."},
        {"role": "user", "content": f"Context: {context}\n\nQuestion: {question}\n\nAnswer only based on the context above."}
    ]

    # Call OpenAI's Chat API
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",  # Use "gpt-3.5-turbo" or "gpt-4" as available
        messages=messages,
        max_tokens=300,
        temperature=0.2  # Low temperature for more deterministic responses
    )

    # Extract and return the answer from the response
    return response["choices"][0]["message"]["content"].strip()

# Function to query the PDF with LangChain and OpenAI
def query_with_langchain(file_path, question):
    # Extract the PDF content using LangChain
    pages = extract_pdf_content(file_path)

    # Combine all the extracted text (you can also implement text chunking for large PDFs)
    full_text = " ".join([page.page_content for page in pages])

    # Ensure that the model only answers based on the context (document text)
    if full_text.strip() == "":
        return "No content found in the document."

    # Use OpenAI's API for question answering
    answer = question_answering_with_openai(question, full_text)
    return answer
