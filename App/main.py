from fastapi import FastAPI
from App.routes import api_router

app = FastAPI(
    title="PDF Question Answering System",
    description="Upload PDFs and ask questions about their content",
    version="1.0.0",
)

app.include_router(api_router)

