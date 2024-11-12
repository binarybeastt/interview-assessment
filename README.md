Project Structure
The directory structure for the project is as follows:

plaintext
Copy code
.
├── Dockerfile               # Defines the Docker image configuration
├── docker-compose.yml       # Manages multi-container setup
├── requirements.txt         # Lists the required Python packages
├── app/
│   ├── main.py              # FastAPI server for backend API
│   ├── model.py             # Wrapper for the Vision Transformer model
│   └── metrics.py           # Code for tracking metrics
├── frontend/
│   └── streamlit_app.py     # Frontend interface using Streamlit
└── models/
    └── queen.jpg            # Sample test image for classification
Each file serves the following purposes:

Dockerfile: Defines the environment for both the backend and frontend services.
docker-compose.yml: Manages the backend and frontend containers, defining their dependencies, ports, and environment variables.
app/: Contains the backend FastAPI server, which handles requests, performs predictions with the Vision Transformer, and tracks metrics.
frontend/: Contains a Streamlit application to provide a simple web-based interface for image upload and display of results.
models/: Stores any model-related files (e.g., pre-trained model, test images).
Step 1: Build and Run with Docker Compose
Install Docker: Ensure Docker and Docker Compose are installed on your system. You can download Docker here.

Clone the Repository: Clone this repository or download the files into your working directory.

Environment Setup: The requirements.txt file lists the necessary Python libraries, including:

transformers: For loading the Vision Transformer model.
torch: The PyTorch framework for deep learning.
FastAPI, Uvicorn: For setting up the API server.
Streamlit: For the frontend interface.
Prometheus client: For tracking API metrics.
Docker Compose Configuration:

docker-compose.yml orchestrates the multi-container setup.
Backend Service (backend):
Builds from the Dockerfile.
Exposes port 8000 for the FastAPI backend.
Mounts the models/ directory to access the model files.
Frontend Service (frontend):
Connects to the backend service and exposes port 8501.
Depends on the backend, ensuring it only starts after the backend service is up.
Step 2: Dockerfile Explanation
The Dockerfile prepares the environment by setting up the required dependencies and copying code files into the image:

dockerfile
Copy code
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

# Create startup script
COPY start.sh .
RUN chmod +x start.sh

CMD ["./start.sh"]
Key elements of the Dockerfile:

Base Image: Uses python:3.9-slim to keep the image lightweight.
Working Directory: Sets /app as the working directory.
Dependencies: Installs libraries specified in requirements.txt.
Code Files: Copies app/, frontend/, and models/ into the image.
Startup Script: The start.sh script launches both backend and frontend servers.
Step 3: Running the Application
With Docker Compose, the application can be easily deployed by running the following commands:

Build the Docker Images:

bash
Copy code
docker-compose build
Start the Containers:

bash
Copy code
docker-compose up
Docker Compose will set up and start both the backend and frontend services. You should see logs indicating that both the FastAPI and Streamlit servers are running.

Access the Application:

Frontend: Go to http://localhost:8501 to access the Streamlit interface, where you can upload images and view classification results.
Backend API: The FastAPI backend is available at http://localhost:8000, where you can access API endpoints (e.g., /predict and /metrics).
Usage
The Streamlit frontend allows you to interact with the model by uploading images for classification:

Upload an image of a chess piece.
Click Classify to send the image to the backend for classification.
The model’s prediction, confidence score, and inference time will be displayed, along with live metrics.
The FastAPI backend provides two key endpoints:

/predict: Accepts an uploaded image file, performs classification, and returns the predicted class with confidence and inference time.
/metrics: Returns performance metrics, such as total requests, successful requests, failed requests, and average inference time.
start.sh Script
The start.sh script simultaneously launches both the backend and frontend services:

bash
Copy code
#!/bin/bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 &
streamlit run frontend/streamlit_app.py --server.port 8501 --server.address 0.0.0.0
This script ensures both servers run in the same container, with the backend on port 8000 and the frontend on port 8501.

Advanced Configuration
You can modify the environment variables in the docker-compose.yml file to customize the backend API URL for the frontend or the path to the model files. Additionally, you can scale the services or adjust resources allocated to each service by altering Docker Compose configurations.
