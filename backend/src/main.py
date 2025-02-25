from fastapi import FastAPI, Form, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from .extractor import extract
import uuid
import os

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.post("/extract_from_doc")
def extract_from_doc(
    file: UploadFile = File(...),
    file_format: str = Form(...)
):
    print(f"Received file: {file.filename}, Format: {file_format}")

    content = file.file.read()
    print("Current working directory:", os.getcwd())
    FILE_PATH = os.path.join(os.getcwd(), "uploads", str(uuid.uuid4()) + ".pdf")

    with open(FILE_PATH, "wb") as f:
        f.write(content)

    try:
        data = extract(FILE_PATH, file_format)
    except Exception as e:
        data = {
            'error': str(e)
        }

    if os.path.exists(FILE_PATH):
        os.remove(FILE_PATH)

    return data


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=9000)