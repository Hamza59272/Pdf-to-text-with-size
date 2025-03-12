# FastAPI PDF Text Size Detector

This is a FastAPI-based backend service that allows users to upload a PDF file and detect the text size based on a given height and width in centimeters.

## Features
- Upload a PDF and analyze the text size.
- Input dimensions in centimeters (width and height) for accurate measurement.
- Uses `pymupdf`, `OpenCV`, and `numpy` for text extraction and size detection.
- Supports deployment via `fly.io` and Docker.

## Requirements
Ensure you have the following dependencies installed:

```
fastapi
uvicorn>=0.15.0
pymupdf>=1.18.0
opencv-python-headless>=4.5.0
python-multipart>=0.0.5
numpy>=1.21.0
pillow>=8.3.0
```

## Installation & Running the API

### Running Locally (without Docker)
1. Clone the repository:
    ```sh
    git clone https://github.com/Hamza59272/Pdf-to-text-with-size.git
    cd Pdf-to-text-with-size
    ```
2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use: venv\Scripts\activate
    ```
3. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```
4. Run the FastAPI server:
    ```sh
    uvicorn main:app --host 0.0.0.0 --port 8000 --reload
    ```
5. API will be available at: `http://127.0.0.1:8000/`

### Running with Docker
1. Build the Docker image:
    ```sh
    docker build -t pdf-text-size-detector .
    ```
2. Run the container:
    ```sh
    docker run -p 8000:8000 pdf-text-size-detector
    ```

## API Endpoint
### Detect Text Size
- **Endpoint:** `POST /detect-letters/`
- **Input Parameters:**
    - `file`: PDF file (multipart/form-data)
    - `target_width`: Target width in cm (float)
    - `target_height`: Target height in cm (float)
- **Response:** JSON containing detected text sizes.

#### Example Request (Using `cURL`)
```sh
curl -X 'POST' \
  'http://127.0.0.1:8000/detect-letters/' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@sample.pdf' \
  -F 'target_width=5' \
  -F 'target_height=10'
```

## Deployment on Fly.io
1. Install Fly CLI:
    ```sh
    curl -fsSL https://fly.io/install.sh | sh
    ```
2. Login to Fly.io:
    ```sh
    fly auth login
    ```
3. Create and deploy the application:
    ```sh
    fly launch
    fly deploy
    ```

Now, your API will be accessible via the Fly.io provided domain.

---

This backend service is ideal for text size detection in PDF documents with precise dimensional control using FastAPI, OpenCV, and pymupdf.

