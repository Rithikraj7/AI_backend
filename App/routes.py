from fastapi import APIRouter, UploadFile, Form, HTTPException
from App.utils import save_pdf, extract_text, process_question, UPLOAD_DIR
import os
from fastapi.responses import JSONResponse

api_router = APIRouter()

# Upload PDF endpoint
@api_router.post("/upload/")
async def upload_pdf(file: UploadFile):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a PDF.")
    file_path = save_pdf(file)
    text_content = extract_text(file_path)
    filename = os.path.basename(file.filename)  # Get a safe base filename
    return {"message": "PDF uploaded successfully", "text": text_content, "file_id": filename}

# Ask question endpoint
@api_router.post("/ask/")
async def ask_question(file_id: str = Form(...), question: str = Form(...)):
    try:
        answer = process_question(file_id, question)  # This is just an example
        return {"answer": answer}
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})


# Delete file endpoint
@api_router.delete("/delete/{file_id}")
async def delete_file(file_id: str):
    file_path = os.path.join(UPLOAD_DIR, file_id)  # Adjust the storage path accordingly
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found.")

    try:
        os.remove(file_path)
        return {"message": f"File '{file_id}' deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while deleting the file: {str(e)}")
