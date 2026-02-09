import requests
from .config import Config


class ModelAPIError(Exception):
    """Raised when the model API returns an error or is unreachable."""
    pass


def check_model_health():
    """
    Ping the model API health endpoint.
    Returns True if healthy, False otherwise.
    """
    if not Config.MODEL_API_HEALTH_URL:
        return False
    
    try:
        resp = requests.get(
            Config.MODEL_API_HEALTH_URL,
            timeout=5
        )
        return resp.status_code == 200
    except requests.RequestException:
        return False


def get_prediction(image_file):
    """
    Send an image to the model API and get a prediction.
    
    Args:
        image_file: A file-like object (from request.files)
    
    Returns:
        dict with keys: prediction, confidence, probabilities, 
        processing_time_ms, model_version, heatmap (optional)
    
    Raises:
        ModelAPIError: If the API request fails or returns an error
    """
    if not Config.MODEL_API_URL:
        raise ModelAPIError("Model API URL not configured")
    
    try:
        # Reset file pointer in case it was read before
        image_file.seek(0)
        image_data = image_file.read()
        
        headers = {}
        if Config.MODEL_API_KEY:
            headers['Authorization'] = f'Bearer {Config.MODEL_API_KEY}'
        
        # Hugging Face Inference API expects binary body for image tasks
        resp = requests.post(
            Config.MODEL_API_URL,
            data=image_data,
            headers=headers,
            timeout=Config.API_TIMEOUT_SECONDS
        )
        
        if resp.status_code != 200:
            # Try to get error message from response
            try:
                error_data = resp.json()
                msg = error_data.get('error', f'API returned status {resp.status_code}')
            except ValueError:
                msg = f'API returned status {resp.status_code}'
            raise ModelAPIError(msg)
        
        # Hugging Face Image Classification returns a list of dicts:
        # [{'label': 'tabby, tabby cat', 'score': 0.98}, ...]
        data = resp.json()
        
        if not isinstance(data, list) or not data:
             # Handle case where model might still be loading
             if isinstance(data, dict) and 'error' in data:
                 raise ModelAPIError(f"Model Error: {data['error']}")
             raise ModelAPIError("Invalid response format from Hugging Face API")

        # Parse HF response to match our app's expected format
        top_result = data[0]
        prediction = top_result.get('label', 'Unknown')
        confidence = top_result.get('score', 0.0)
        
        # Convert list of scores to probabilities dict
        probabilities = {item['label']: item['score'] for item in data[:5]}
        
        return {
            "prediction": prediction,
            "confidence": confidence,
            "probabilities": probabilities,
            "processing_time_ms": int(resp.elapsed.total_seconds() * 1000),
            "model_version": "HF-ResNet50", # Placeholder
            "heatmap": None # HF API doesn't return heatmaps by default
        }
        
    except requests.Timeout:
        raise ModelAPIError("Analysis is taking longer than expected. Please try again.")
    except requests.ConnectionError:
        raise ModelAPIError("Unable to connect to analysis service. Please check your connection.")
    except requests.RequestException as e:
        raise ModelAPIError(f"Request failed: {str(e)}")
