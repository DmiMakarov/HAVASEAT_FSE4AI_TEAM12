import cv2
import numpy as np
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse

from ..model.model import MNISTModel as Model

app = FastAPI(title="Digit Recognition API", version="1.0.0")
model = Model()


@app.post("/recognize_digit")
async def recognize_digit_endpoint(image: UploadFile = File(...)):
    """
    Recognize digit from uploaded image
    """
    # Validate file type
    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    try:
        # Read image file
        image_bytes = await image.read()

        # Convert bytes to numpy array
        nparr = np.frombuffer(image_bytes, np.uint8)

        # Decode image
        decoded_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if decoded_image is None:
            raise HTTPException(status_code=400, detail="Could not decode image")

        # Call the recognition function
        result = model.recognize_digit(image)
        if result is None:
            result = "Recognition failed"

        return JSONResponse(content={"status": "success", "recognized_digit": result, "filename": image.filename})

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
