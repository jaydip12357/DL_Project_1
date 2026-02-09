# Model API Integration

This document explains how the web application integrates with the external pneumonia detection model API.

## Architecture Overview

The web application acts as a frontend that:
1. Accepts X-ray image uploads from users
2. Forwards images to the model API for analysis
3. Displays results from the model API to users

```
User → Web App (Flask) → Model API → CNN Inference → Response → Web App → User
```

The ML model is deployed separately and accessed via HTTP.

## API Contract

### Prediction Endpoint

**URL**: Configured via `MODEL_API_URL` environment variable

**Method**: `POST`

**Content-Type**: `multipart/form-data`

**Request Body**:
| Field | Type | Description |
|-------|------|-------------|
| image | File | The chest X-ray image (JPG/PNG) |

**Success Response** (200 OK):
```json
{
  "prediction": "PNEUMONIA",
  "confidence": 0.87,
  "probabilities": {
    "NORMAL": 0.13,
    "PNEUMONIA": 0.87
  },
  "processing_time_ms": 245,
  "model_version": "v1.2",
  "heatmap": "<base64-encoded-png>"
}
```

**Required fields**: `prediction`, `confidence`

**Optional fields**: `probabilities`, `processing_time_ms`, `model_version`, `heatmap`

**Error Response** (4xx/5xx):
```json
{
  "error": "Description of what went wrong",
  "status": "failed"
}
```

### Health Check Endpoint

**URL**: Configured via `MODEL_API_HEALTH_URL` environment variable

**Method**: `GET`

**Success Response** (200 OK):
```json
{
  "status": "healthy"
}
```

## Environment Variables

Set these in your `.env` file (local) or Railway dashboard (production):

```bash
# Required
MODEL_API_URL=https://your-model-api.railway.app/predict

# Optional
MODEL_API_HEALTH_URL=https://your-model-api.railway.app/health
MODEL_API_KEY=your-api-key-if-needed
API_TIMEOUT_SECONDS=10
```

## Error Handling

The web app handles these error scenarios:

| Scenario | User Message |
|----------|-------------|
| Model API timeout | "Analysis is taking longer than expected. Please try again." |
| Network error | "Unable to connect to analysis service. Please check your connection." |
| API returns error | Displays the error message from the API |
| Invalid response format | "Invalid response format from model API" |

## Testing Without Model API

For local development without the model API:

1. The app will work for everything except the actual analysis
2. Uploading an image will show an appropriate error
3. You can mock the API response by modifying `api_client.py` temporarily

## Authentication

If the model API requires authentication:

1. Set `MODEL_API_KEY` environment variable
2. The app will automatically add `Authorization: Bearer <key>` header

## Troubleshooting

**"Model API URL not configured"**
- Set the `MODEL_API_URL` environment variable

**Timeout errors**
- Increase `API_TIMEOUT_SECONDS` (default is 10)
- Check if model API is responding

**Connection errors**
- Verify the API URL is correct
- Check if the model API is running
- Ensure network connectivity

**Health check shows "disconnected"**
- The model API may be down
- Check `MODEL_API_HEALTH_URL` is set correctly
