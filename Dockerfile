FROM python:3.12-slim

WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy all application code
COPY . .

# Add the app directory to Python path
ENV PYTHONPATH="${PYTHONPATH}:/app"

EXPOSE 8000
EXPOSE 8501