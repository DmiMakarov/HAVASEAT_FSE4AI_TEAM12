import cv2
import numpy as np
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from model.model import MNISTModel as Model

app = FastAPI(title="Digit Recognition API", version="1.0.0")
model = Model()


@app.post("/recognize_digit")
async def recognize_digit_endpoint(image_file: UploadFile = File(...)):
    """
    Recognize digit from uploaded image
    """

    if not image_file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    try:

        image_bytes = await image_file.read()

        nparr = np.frombuffer(image_bytes, np.uint8)
        if nparr is None:
            raise HTTPException(status_code=400, detail="Could not decode image")

        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        digit, confidence = model.recognize_digit(image)
        if digit is None or confidence is None:
            raise HTTPException(status_code=500, detail=f"Model inference error")

        return JSONResponse(
            content={
                "status": "success",
                "recognized_digit": digit,
                "model_confidence": round(confidence, 3),
                "filename": image_file.filename,
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")


@app.get("/")
async def root():
    return {"message": "Digit Recognition API is running"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    raise ImportError("This is not main module")
