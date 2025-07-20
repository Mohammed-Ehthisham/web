from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image
import pytesseract
import io

app = FastAPI()

@app.post("/captcha")
async def solve_captcha(file: UploadFile = File(...)):
    # Read and open the image
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))

    # Use Tesseract to extract text
    text = pytesseract.image_to_string(image)

    # Try to find the multiplication expression in the text
    import re
    match = re.search(r'(\d{8})\D+(\d{8})', text)
    if match:
        a, b = int(match.group(1)), int(match.group(2))
        answer = a * b
    else:
        return JSONResponse(status_code=400, content={"error": "Could not parse numbers"})

    return {
        "answer": answer,
        "email": "23f3000804@ds.study.iitm.ac.in"
    }
