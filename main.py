from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import cv2
import numpy as np
import fitz
from io import BytesIO
import logging

app = FastAPI()

def extract_image(file_bytes: bytes, content_type: str) -> np.ndarray:
    try:
        if content_type == "application/pdf":
            doc = fitz.open(stream=BytesIO(file_bytes))
            if len(doc) == 0:
                raise ValueError("Empty PDF document")
            
            page = doc.load_page(0)
            pix = page.get_pixmap()
            img_array = np.frombuffer(pix.samples, dtype=np.uint8).reshape(
                pix.height, pix.width, pix.n
            )
            return cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

        if content_type in ["image/jpeg", "image/png"]:
            image = cv2.imdecode(np.frombuffer(file_bytes, np.uint8), cv2.IMREAD_COLOR)
            if image is None:
                raise ValueError("Failed to decode image")
            return image

        raise ValueError("Unsupported file format")
    except Exception as e:
        logging.error(f"Image extraction error: {str(e)}")
        raise

def process_image(image: np.ndarray, target_width: int, target_height: int) -> list:
    try:
        # Improved preprocessing
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        
        # Better morphological operations
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
        cleaned = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)
        
        # Find contours with hierarchy
        contours, hierarchy = cv2.findContours(cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Filter and sort contours
        letter_boxes = []
        min_area = 500
        max_aspect_ratio = 3.0
        
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            area = w * h
            aspect_ratio = w / float(h)
            
            if area > min_area and aspect_ratio < max_aspect_ratio:
                letter_boxes.append((x, y, w, h))
        
        # Sort contours from left to right with y-axis tolerance
        letter_boxes.sort(key=lambda b: (b[0], b[1]))
        
        # Merge nearby contours (for characters with disconnected parts)
        merged_boxes = []
        for box in letter_boxes:
            if not merged_boxes:
                merged_boxes.append(box)
            else:
                last = merged_boxes[-1]
                # Merge if boxes are close horizontally
                if box[0] <= (last[0] + last[2] + 5):
                    new_x = min(last[0], box[0])
                    new_y = min(last[1], box[1])
                    new_w = max(last[0] + last[2], box[0] + box[2]) - new_x
                    new_h = max(last[1] + last[3], box[1] + box[3]) - new_y
                    merged_boxes[-1] = (new_x, new_y, new_w, new_h)
                else:
                    merged_boxes.append(box)
        
        # Calculate scaling parameters
        original_widths = [w for _, _, w, h in merged_boxes]
        heights = [h for _, _, w, h in merged_boxes]
        
        if not original_widths:
            return []

        total_original_width = sum(original_widths)
        max_height = max(heights)
        
        # Calculate scaling ratios
        width_ratio = target_width / total_original_width
        height_ratio = target_height / max_height
        
        # Distribute remaining width
        scaled_widths = [int(w * width_ratio) for w in original_widths]
        remaining_width = target_width - sum(scaled_widths)
        
        # Distribute remaining width to widest letters first
        while remaining_width > 0:
            max_index = scaled_widths.index(max(scaled_widths))
            scaled_widths[max_index] += 1
            remaining_width -= 1
        
        # Prepare response with letter numbering
        letters = []
        for idx, (w, h) in enumerate(zip(original_widths, heights)):
            letters.append({
                "letter_number": idx + 1,
                # "original_width": w,
                # "original_height": h,
                "scaled_width": scaled_widths[idx],
                "scaled_height": int(height_ratio * h)
            })
        
        return letters

    except Exception as e:
        logging.error(f"Image processing error: {str(e)}")
        raise

@app.post("/detect-letters/")
async def detect_letters(
    file: UploadFile = File(...),
    target_width: int = Form(200),
    target_height: int = Form(100)
):
    try:
        file_bytes = await file.read()
        image = extract_image(file_bytes, file.content_type)
        letters = process_image(image, target_width, target_height)
        return {"letters": letters}

    except ValueError as e:
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        raise HTTPException(500, detail="Internal server error")
    finally:
        await file.close()

@app.get("/")
async def startup():
        return {"message": "API is Running"}


import os
import uvicorn

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))  # Use Railway’s assigned port
    uvicorn.run(app, host="0.0.0.0", port=port)
