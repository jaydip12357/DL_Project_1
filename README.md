# Fashion Classification Web Application

A web application for classifying fashion items (shoes, bags, clothing) using AI. Built with Flask and powered by Hugging Face Inference API.

## Features

* Upload fashion item images via drag-and-drop or file picker
* Get instant classification with confidence scores
* Uses state-of-the-art ResNet-50 model
* Responsive design for mobile and desktop

## Technology Stack

* **Backend**: Python 3.10, Flask
* **Frontend**: HTML5, CSS3, JavaScript
* **AI Model**: Hugging Face Inference API (microsoft/resnet-50)
* **Deployment**: Render / Railway

## Architecture

```
User Browser → Web App (Flask) → Hugging Face API → Response → User
```

## Setup

### Prerequisites

* Python 3.10+
* pip

### Installation

1. Clone the repository
2. Create virtual environment and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create `.env` file (optional, defaults provided):
   ```
   MODEL_API_KEY=<your-huggingface-token>
   ```
4. Run:
   ```bash
   python -m flask --app app.main run --debug
   ```

## License

MIT License
