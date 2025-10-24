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
        result = model.process_and_recognize(image_bytes, image_file.filename)
        return JSONResponse(content=result)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@app.get("/")
async def root():
    return {"message": "Digit Recognition API is running"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    raise ImportError("This is not main module")
