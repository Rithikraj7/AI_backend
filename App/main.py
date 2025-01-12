from fastapi import FastAPI
from App.routes import api_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="PDF Question Answering System",
    description="Upload PDFs and ask questions about their content",
    version="1.0.0",
)

# Define allowed origins (front-end URL)
origins = [
    "https://Rithikraj7.github.io/AI_frontend/",  # Your frontend URL during development
    "http://192.168.50.1:3000/",      # Localhost for testing
]

# Add CORSMiddleware to the app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows CORS for the specified origins
    allow_credentials=True,
    allow_methods=["*"],    # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],    # Allows all headers
)

app.include_router(api_router)

