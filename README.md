# OCR API Documentation

## Overview
This API provides OCR services using FastAPI and PaddleOCR. It supports single and batch image uploads, converting them to text.

---

## API Endpoints

### 1. **Home Page**
- **GET /**: Renders the home page.

### 2. **Single Image OCR**
- **POST /ocr**: Upload an image to extract text.
  
  **Request**:
  ```bash
  curl -X POST "http://localhost:8000/ocr" -F "image=@image.jpg"


**Response JSON**

```bash
 {"text": "Extracted text", "file": "image.json"}
```

