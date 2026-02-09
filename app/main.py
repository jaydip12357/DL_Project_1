import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from .config import Config
from .api_client import get_prediction, check_model_health, ModelAPIError
from .utils import allowed_file, validate_file_size


app = Flask(__name__, 
            template_folder='../templates',
            static_folder='../static')
app.secret_key = Config.SECRET_KEY


@app.route('/api/predict', methods=['POST'])
def api_predict():
    """
    API endpoint for direct image prediction.
    Returns JSON response instead of rendering a template.
    """
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    
    file = request.files['image']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
        
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Allowed: jpg, jpeg, png'}), 400

    try:
        result = get_prediction(file)
        return jsonify(result)
        
    except ModelAPIError as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    """Home page with upload interface."""
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    """Handle image upload and call model API."""
    
    if 'image' not in request.files:
        return render_template('error.html', 
            error="No file was uploaded. Please select an image.")
    
    file = request.files['image']
    
    if file.filename == '':
        return render_template('error.html',
            error="No file selected. Please choose an image to upload.")
    
    if not allowed_file(file.filename):
        return render_template('error.html',
            error="Invalid file type. Please upload a JPG or PNG image.")
    
    if not validate_file_size(file):
        return render_template('error.html',
            error=f"File is too large. Maximum size is {Config.MAX_FILE_SIZE_MB}MB.")
    
    try:
        result = get_prediction(file)
        
        # Store result in session for the results page
        session['prediction'] = result.get('prediction')
        session['confidence'] = result.get('confidence')
        session['probabilities'] = result.get('probabilities', {})
        session['processing_time_ms'] = result.get('processing_time_ms')
        session['model_version'] = result.get('model_version')
        session['heatmap'] = result.get('heatmap')  # Base64 encoded if present
        session['analyzed_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Save original image as base64 for display
        file.seek(0)
        import base64
        session['original_image'] = base64.b64encode(file.read()).decode('utf-8')
        session['original_filename'] = file.filename
        session['original_mimetype'] = file.content_type or 'image/jpeg'
        
        return redirect(url_for('results'))
        
    except ModelAPIError as e:
        return render_template('error.html', error=str(e))


@app.route('/results')
def results():
    """Display analysis results."""
    
    prediction = session.get('prediction')
    if not prediction:
        return redirect(url_for('index'))
    
    return render_template('results.html',
        prediction=prediction,
        confidence=session.get('confidence'),
        probabilities=session.get('probabilities', {}),
        processing_time_ms=session.get('processing_time_ms'),
        model_version=session.get('model_version'),
        heatmap=session.get('heatmap'),
        analyzed_at=session.get('analyzed_at'),
        original_image=session.get('original_image'),
        original_filename=session.get('original_filename'),
        original_mimetype=session.get('original_mimetype')
    )


@app.route('/health')
def health():
    """Health check endpoint for Railway monitoring."""
    model_status = 'connected' if check_model_health() else 'disconnected'
    
    return jsonify({
        'status': 'healthy',
        'model_api': model_status
    })


if __name__ == '__main__':
    app.run(debug=Config.DEBUG, port=5000)
