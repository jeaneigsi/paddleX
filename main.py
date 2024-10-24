from fastapi import FastAPI, UploadFile, HTTPException, Request,File
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from paddlex import create_pipeline
from PIL import Image
import numpy as np
import os
import json
from fastapi.middleware.cors import CORSMiddleware
import logging
from paddlex import create_pipeline
import io
import json
from typing import Union, List

app = FastAPI()
templates = Jinja2Templates(directory="templates")
# logging.basicConfig(level=logging.INFO)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

def pil_to_np(img: Image.Image) -> np.ndarray:
    """Convertir une image PIL en tableau NumPy."""
    return np.array(img)


def get_ocr_batch():
    json_dir = "./output"
    results = {}
    for filename in os.listdir(json_dir):
        if filename.endswith(".json"):
            with open(os.path.join(json_dir, filename), 'r') as json_file:
                results[filename] = json.load(json_file)
    return results



@app.get("/")
async def home(request : Request):
    return templates.TemplateResponse("index.html", {"request": request})



@app.post("/ocr")
async def ocr_pipeline(image: UploadFile = File(...)):
    try:
        img_bytes = await image.read()
        name, _ = os.path.splitext(image.filename)
        print(f"Received file: {image.filename}, size: {len(img_bytes)} bytes") 
        img = Image.open(io.BytesIO(img_bytes))
        image = pil_to_np(img)
        pipeline = create_pipeline(pipeline="./OCR.yaml", device="cpu")
        output = pipeline.predict(image)
        for res in output:
            res.print()
            res.save_to_json(f"./output/{name}.json")
        with open(f"./output/{name}.json",'r') as files:
            data=json.load(files)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

@app.post("/ocr_batch")
async def ocr_batch_pipeline(images):
    try:
          # Step 2: Create and run the OCR pipeline on the list of NumPy arrays
        pipeline = create_pipeline(pipeline="./OCR.yaml", device="cpu")
        results = pipeline.predict(images)  # Run OCR on the list of NumPy arrays
        for res in results:
            res.print()
            res.save_to_json(f"./output/")
        results=get_ocr_batch()
        return JSONResponse(content=results)
    except Exception as e:
        raise HTTPException (status_code=500, detail=f"Error processing images: {str(e)}")
