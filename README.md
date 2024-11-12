
# Vision Transformer Image Classification

This project demonstrates an image classification pipeline using a Vision Transformer (ViT) model, designed to classify chess piece images. It includes a backend API powered by FastAPI, a frontend interface built with Streamlit, and metrics tracking with Prometheus. The application is fully containerized using Docker and Docker Compose.

---

## Project Structure

```plaintext
.
├── Dockerfile               # Docker image configuration
├── docker-compose.yml       # Docker Compose setup for multi-container app
├── requirements.txt         # Python dependencies
├── app/
│   ├── main.py              # FastAPI backend server
│   ├── model.py             # Vision Transformer model wrapper
│   └── metrics.py           # Metrics tracking with Prometheus
├── frontend/
│   └── streamlit_app.py     # Frontend interface with Streamlit
└── models/
    └── queen.jpg            # Sample test image
```

- **Dockerfile**: Sets up the environment for both the backend and frontend.
- **docker-compose.yml**: Orchestrates the multi-container application.
- **app/**: Contains backend files for the API, model, and metrics tracking.
- **frontend/**: Houses a Streamlit app for the user interface.
- **models/**: Stores any model-related files, such as pre-trained models or test images.

---

## Requirements

- **Docker** and **Docker Compose** are required to build and run this containerized application.
- Install Docker by following the instructions at [Get Docker](https://docs.docker.com/get-docker/).

---

## Setup Instructions

1. **Clone the Repository**: Clone this repository or download the files into your working directory.

2. **Install Docker and Docker Compose**: Ensure Docker and Docker Compose are installed on your machine.

3. **Build and Run with Docker Compose**:
   - Build the Docker images:
     ```bash
     docker-compose build
     ```
   - Start the application:
     ```bash
     docker-compose up
     ```
   - This command launches both the backend and frontend services. The backend (FastAPI) runs on port `8000`, while the frontend (Streamlit) runs on port `8501`.

4. **Access the Application**:
   - **Frontend**: Go to [http://localhost:8501](http://localhost:8501) to access the Streamlit frontend for uploading images and viewing classification results.
   - **Backend API**: Access the FastAPI backend at [http://localhost:8000](http://localhost:8000), where API endpoints for predictions and metrics are available.

---

## Usage

### Frontend

The **Streamlit frontend** provides an interface to interact with the model by uploading images for classification.

1. Upload an image of a chess piece.
2. Click **Classify** to send the image to the backend for classification.
3. The predicted class, confidence score, and inference time will be displayed, along with real-time metrics.

### Backend API Endpoints

The **FastAPI backend** exposes two main endpoints:

- **/predict**:
   - Accepts an uploaded image file, performs classification, and returns:
     - `class`: Predicted class label.
     - `confidence`: Confidence score.
     - `inference_time`: Time taken for the prediction.
   - Example request:
     ```bash
     curl -X POST "http://localhost:8000/predict" -F "file=@path_to_image.jpg"
     ```

- **/metrics**:
   - Returns metrics data such as:
     - `total_requests`: Total number of requests processed.
     - `successful_requests`: Number of successful requests.
     - `failed_requests`: Number of failed requests.
     - `average_inference_time`: Average inference time per request.

---

## File and Code Descriptions

### Dockerfile

The `Dockerfile` sets up the application environment by installing dependencies and copying code files. 

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application code
COPY app/ app/
COPY frontend/ frontend/
COPY models/ models/

# Expose ports for FastAPI and Streamlit
EXPOSE 8000
EXPOSE 8501

# Copy startup script and make it executable
COPY start.sh .
RUN chmod +x start.sh

CMD ["./start.sh"]
```

### Docker Compose Configuration

The `docker-compose.yml` file orchestrates the application, managing two services: the backend and frontend.

```yaml
version: '3'
services:
  backend:
    build: .
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000
    ports:
      - "8000:8000"
    volumes:
      - ./models:/app/models
    environment:
      - MODEL_PATH=/app/models

  frontend:
    build: .
    command: streamlit run frontend/streamlit_app.py --server.port 8501 --server.address 0.0.0.0
    ports:
      - "8501:8501"
    depends_on:
      - backend
    environment:
      - BACKEND_URL=http://backend:8000
```

- **backend**:
   - Runs FastAPI on port `8000`.
   - Mounts the `models/` directory for access to model files.
- **frontend**:
   - Connects to the backend for predictions and metrics.
   - Exposes the Streamlit interface on port `8501`.

### Requirements File

The `requirements.txt` file lists all necessary Python packages for both backend and frontend.

```plaintext
fastapi==0.68.1
uvicorn==0.15.0
python-multipart==0.0.5
transformers==4.30.2
torch==2.0.1
Pillow==9.5.0
streamlit==1.22.0
prometheus-client==0.16.0
python-jose==3.3.0
requests==2.31.0
```

---

## Custom Python Files

- **app/model.py**: Wraps the Vision Transformer model for handling image classification.
- **app/metrics.py**: Tracks and updates Prometheus metrics for the API.
- **app/main.py**: The FastAPI server handles requests, performs predictions, and tracks metrics.
- **frontend/streamlit_app.py**: Streamlit app displays an interface for uploading images and viewing results.

---

## Startup Script

The `start.sh` script is used to simultaneously launch both backend and frontend services.

```bash
#!/bin/bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 &
streamlit run frontend/streamlit_app.py --server.port 8501 --server.address 0.0.0.0
```

This script runs FastAPI on port `8000` and Streamlit on port `8501`.

---

## Testing and Debugging

To test individual services, you can use the following commands:

- **Backend Only**:
  ```bash
  uvicorn app.main:app --host 0.0.0.0 --port 8000
  ```

- **Frontend Only**:
  ```bash
  streamlit run frontend/streamlit_app.py --server.port 8501 --server.address 0.0.0.0
  ```

If you need to debug, check container logs with:
```bash
docker-compose logs -f
```

---

## Conclusion

This project demonstrates an end-to-end image classification pipeline with a Vision Transformer model. The app is containerized for ease of deployment and scalability. Both the backend and frontend work together to classify images, provide real-time performance metrics, and visualize results.

---
