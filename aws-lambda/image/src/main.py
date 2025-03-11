# from fastapi import FastAPI, UploadFile, File, HTTPException
# import shutil

# app = FastAPI()

# @app.post("/")
# def mock_post(image: UploadFile = File(...)):
#     if not image.content_type.startswith("image/"):
#         raise HTTPException(status_code=415, detail="Not an image")
    
#     try:
#         with open("out.jpg","wb") as buffer:
#             shutil.copyfileobj(image.file, buffer)
#     finally:
#         image.file.close()
    
#     return {
#         "type": "test-1",
#         "status": "test-1",
#         "confidence": 1,
#     }
import json
import base64

def handler(event, context):
    imageBinary: str = event["image"]
    
    # convert it into jpeg binary
    base64.b64decode(imageBinary)
    
    # call model
    
    # extract results
    
    # done
    
    return {
        "type": "test-1",
        "status": "test-1",
        "confidence": 1,
    }