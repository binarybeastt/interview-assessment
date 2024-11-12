from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from .model import VitClassifier
from .metrics import MetricsTracker
import time

app = FastAPI()
model = VitClassifier()
metrics = MetricsTracker()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    start_time = time.time()
    success = False
    
    try:
        contents = await file.read()
        predicted_class, confidence, inference_time = model.predict(contents)
        success = True
        
        return {
            "class": predicted_class,
            "confidence": confidence,
            "inference_time": inference_time
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        request_time = time.time() - start_time
        metrics.track_request(request_time, success)

@app.get("/metrics")
async def get_metrics():
    return {
        "total_requests": metrics.requests_total._value.get(),
        "successful_requests": metrics.successful_requests._value.get(),
        "failed_requests": metrics.failed_requests._value.get(),
        "average_inference_time": (
        next(sample.value for sample in list(metrics.inference_time.collect())[0].samples if sample.name == 'model_inference_time_seconds_sum') / 
        max(next(sample.value for sample in list(metrics.inference_time.collect())[0].samples if sample.name == 'model_inference_time_seconds_count'), 1)
    )
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)