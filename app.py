import os
from flask import Flask, render_template, Response, request, jsonify
from flask_socketio import SocketIO, emit
from dotenv import load_dotenv
from utils.config import init_client, create_endpoint, deploy_model_to_endpoint
from utils.api_utils import upload_frame, generate_content_from_frames, analyze_image, transcribe_audio, synthesize_speech, analyze_sentiment
from video_streaming import generate_frames, get_model

app = Flask(__name__)
socketio = SocketIO(app, async_mode='threading')

load_dotenv()  # Load environment variables from .env file

# Load the pre-trained model
model = get_model()
model.load_weights('path_to_saved_model/gesture_model.h5')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@socketio.on('connect')
def test_connect():
    emit('my response', {'data': 'Connected'})

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

@app.route('/create_endpoint', methods=['POST'])
def create_endpoint_route():
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    location = os.getenv('GOOGLE_CLOUD_REGION')
    display_name = request.json.get('display_name', 'My Model Endpoint')
    description = request.json.get('description', 'Endpoint for a model')

    client = init_client(location)
    endpoint = create_endpoint(client, project_id, location, display_name, description)
    return jsonify({"endpoint": endpoint.name})

@app.route('/deploy_model', methods=['POST'])
def deploy_model_route():
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    location = os.getenv('GOOGLE_CLOUD_REGION')
    endpoint_name = request.json.get('endpoint_name')
    model_id = request.json.get('model_id')

    client = init_client(location)
    model_name = f'projects/{project_id}/locations/{location}/models/{model_id}'
    deployment_result = deploy_model_to_endpoint(client, endpoint_name, model_name)
    return jsonify({"deployment_result": deployment_result})

@app.route('/upload_audio', methods=['POST'])
def upload_audio():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"})
    if file:
        audio_content = file.read()
        results = transcribe_audio(audio_content)
        return jsonify({"transcription": results})
    return jsonify({"error": "Failed to process audio"})

@app.route('/synthesize_speech', methods=['POST'])
def synthesize_speech_route():
    data = request.get_json()
    text = data.get('text', '')
    if not text:
        return jsonify({"error": "No text provided"})
    audio_content = synthesize_speech(text)
    return jsonify({"audio_content": audio_content.decode('ISO-8859-1')})

@app.route('/process_frame', methods=['POST'])
def process_frame():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"})
    if file:
        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)
        frame_uri = upload_frame(file_path)
        return jsonify({"frame_uri": frame_uri})

@app.route('/generate_content', methods=['POST'])
def generate_content():
    data = request.get_json()
    frame_uris = data.get('frame_uris', [])
    prompt = data.get('prompt', 'Generate content based on these frames')
    content = generate_content_from_frames(frame_uris, prompt)
    return jsonify({"content": content})

@app.route('/analyze_image', methods=['POST'])
def analyze_image_route():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"})
    if file:
        image_content = file.read()
        results = analyze_image(image_content)
        return jsonify({"texts": results})

@app.route('/analyze_sentiment', methods=['POST'])
def analyze_sentiment_route():
    data = request.get_json()
    text = data.get('text', '')
    if not text:
        return jsonify({"error": "No text provided"})
    results = analyze_sentiment(text)
    return jsonify(results)

if __name__ == '__main__':
    socketio.run(app, debug=True)
