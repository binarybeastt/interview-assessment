import time
from transformers import ViTImageProcessor, ViTForImageClassification
from PIL import Image
import torch
from typing import Tuple, Dict
import io

class VitClassifier:
    def __init__(self):
        self.processor = ViTImageProcessor.from_pretrained('google/vit-base-patch16-224-in21k')
        self.model = ViTForImageClassification.from_pretrained('Binaryy/test-trainer')
        self.model.eval()

    def predict(self, image_bytes: bytes) -> Tuple[str, float, float]:
        start_time = time.time()
        
        # Load and process image
        image = Image.open(io.BytesIO(image_bytes))
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        inputs = self.processor(images=image, return_tensors="pt")
        
        # Make prediction
        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits
            
            # Get predicted class
            predicted_class_idx = logits.argmax(-1).item()
            predicted_class = self.model.config.id2label[predicted_class_idx]
            
            # Get probability
            probs = torch.nn.functional.softmax(logits, dim=-1)
            confidence = probs[0][predicted_class_idx].item()
        
        inference_time = time.time() - start_time
        
        return predicted_class, confidence, inference_time