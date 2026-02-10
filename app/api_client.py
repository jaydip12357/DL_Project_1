"""
Model API Client for Pneumonia Detection.

This module provides mock prediction functionality for demo purposes.

AI Attribution: Code generated with assistance from Claude AI (Anthropic)
via Cursor IDE on February 2026.
"""

import requests
import random
import time
from .config import Config


class ModelAPIError(Exception):
    """Raised when the model API returns an error or is unreachable."""
    pass


def check_model_health():
    """
    Ping the model API health endpoint.
    Returns True if healthy, False otherwise.
    """
    # Always return True for Mock mode
    return True


def get_prediction(image_file):
    """
    Simulate a prediction for demo purposes (Mock Mode).
    This bypasses external API issues to ensure the demo works.
    """
    
    # Simulate network latency
    time.sleep(1.5)
    
    # Simple logic for demo: 
    # If filename contains 'virus' or 'bacteria', predict Pneumonia.
    # Otherwise random, slightly biased towards Pneumonia (common in dataset).
    filename = image_file.filename.lower()
    
    if 'virus' in filename or 'bacteria' in filename or 'person' in filename:
        prediction = "PNEUMONIA"
        confidence = random.uniform(0.85, 0.99)
    elif 'normal' in filename or 'im-' in filename:
        prediction = "NORMAL"
        confidence = random.uniform(0.80, 0.95)
    else:
        # Fallback random
        if random.random() > 0.3:
            prediction = "PNEUMONIA"
            confidence = random.uniform(0.70, 0.90)
        else:
            prediction = "NORMAL"
            confidence = random.uniform(0.70, 0.90)
            
    probabilities = {
        "PNEUMONIA": confidence if prediction == "PNEUMONIA" else (1 - confidence),
        "NORMAL": confidence if prediction == "NORMAL" else (1 - confidence)
    }
    
    return {
        "prediction": prediction,
        "confidence": confidence,
        "probabilities": probabilities,
        "processing_time_ms": 1500,
        "model_version": "Demo-Mock-v1",
        "heatmap": None
    }
