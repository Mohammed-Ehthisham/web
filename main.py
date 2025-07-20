from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict
import pytesseract
from PIL import Image
import io
import re

app = FastAPI()

# Allow CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

EMAIL = "23f3000804@ds.study.iitm.ac.in"

@app.post("/captcha")
async def solve_captcha(file: UploadFile = File(...)) -> Dict:
    # Read the uploaded file
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes))

    # OCR to extract text
    text = pytesseract.image_to_string(image)

    # Extract two 8-digit numbers using regex
    numbers = re.findall(r"\d{8}", text)
    if len(numbers) >= 2:
        num1 = int(numbers[0])
        num2 = int(numbers[1])
        result = num1 * num2
    else:
        return {"error": "Could not extract two 8-digit numbers."}

    return {
        "answer": result,
        "email": EMAIL
    }