# Pneumonia Detection Web Application

A web application for analyzing chest X-ray images to detect signs of pneumonia using AI. Built with Flask and designed to work with an external model API.

## Features

- Upload chest X-ray images via drag-and-drop or file picker
- Get instant pneumonia predictions with confidence scores
- View analysis heatmaps when available
- Responsive design for mobile and desktop
- Health check endpoint for monitoring

## Technology Stack

- **Backend**: Python 3.10, Flask
- **Frontend**: HTML5, CSS3, JavaScript (vanilla)
- **HTTP Client**: Requests
- **Deployment**: Railway (with Gunicorn)

## Architecture

```
User Browser → Web App (Flask/Railway) → Model API (External) → Response → User
```

This application is the web frontend component. It does not perform ML inference directly—instead, it forwards images to an external model API and displays the results.

## Setup

### Prerequisites

- Python 3.10+
- pip

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd pneumonia-detection-web
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file:
   ```
   MODEL_API_URL=<your-model-api-url>/predict
   MODEL_API_HEALTH_URL=<your-model-api-url>/health
   MODEL_API_KEY=<optional-api-key>
   SECRET_KEY=<generate-a-random-key>
   ```

5. Run the development server:
   ```bash
   python -m flask --app app.main run --debug
   ```

6. Open http://localhost:5000

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `MODEL_API_URL` | Yes | - | URL of the model prediction endpoint |
| `MODEL_API_HEALTH_URL` | No | - | URL for model API health checks |
| `MODEL_API_KEY` | No | - | API key if authentication is required |
| `API_TIMEOUT_SECONDS` | No | 10 | Timeout for API requests |
| `MAX_FILE_SIZE_MB` | No | 10 | Maximum upload file size |
| `SECRET_KEY` | No | dev-key | Flask session secret key |
| `DEBUG` | No | False | Enable debug mode |

## Model API Integration

The application expects the model API to follow this contract:

**Request:**
```
POST /predict
Content-Type: multipart/form-data
Body: image (file)
```

**Response:**
```json
{
  "prediction": "PNEUMONIA",
  "confidence": 0.87,
  "probabilities": {"NORMAL": 0.13, "PNEUMONIA": 0.87},
  "processing_time_ms": 245,
  "model_version": "v1.2",
  "heatmap": "<base64-encoded-image>"
}
```

See [docs/API_INTEGRATION.md](docs/API_INTEGRATION.md) for details.

## Testing

Run the test suite:
```bash
python -m pytest tests/ -v
```

### Manual Testing Checklist

- [ ] Upload valid JPG image
- [ ] Upload valid PNG image
- [ ] Upload file > 10MB (should show error)
- [ ] Upload non-image file (should show error)
- [ ] Check `/health` endpoint
- [ ] Test on mobile viewport

## Deployment

See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for Railway deployment instructions.

Quick steps:
1. Connect GitHub repo to Railway
2. Set environment variables in Railway dashboard
3. Deploy from main branch

## Project Structure

```
pneumonia-detection-web/
├── app/
│   ├── main.py         # Flask routes
│   ├── config.py       # Configuration
│   ├── api_client.py   # Model API client
│   └── utils.py        # Utility functions
├── templates/          # HTML templates
├── static/
│   ├── css/           # Stylesheets
│   └── js/            # Client-side JS
├── tests/             # Unit tests
├── docs/              # Documentation
├── requirements.txt
├── Procfile
└── runtime.txt
```

## Contributing

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make changes and commit with clear messages
3. Create a pull request with description of changes
4. Self-review and merge

## Medical Disclaimer

This application is for **educational and research purposes only**. It is not intended for clinical diagnosis. Always consult qualified healthcare professionals for medical advice.

## License

MIT License