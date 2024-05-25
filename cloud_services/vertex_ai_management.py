import os
import cv2
from flask import Flask, render_template, Response, request, jsonify
from flask_socketio import SocketIO, emit
from google.cloud import aiplatform
from dotenv import load_dotenv

app = Flask(__name__)
socketio = SocketIO(app, async_mode='threading')

load_dotenv()  # Load environment variables from .env file

def init_client(location):
    """Initialize and return the AI Platform client."""
    client_options = {"api_endpoint": f"{location}-aiplatform.googleapis.com"}
    return aiplatform.gapic.EndpointServiceClient(client_options=client_options)

def create_endpoint(client, project_id, location, display_name="My Model Endpoint", description="Endpoint for a model"):
    """Create a new endpoint for deploying models."""
    endpoint = {"display_name": display_name, "description": description}
    parent = f"projects/{project_id}/locations/{location}"
    print("Creating endpoint...")
    operation = client.create_endpoint(parent=parent, endpoint=endpoint)
    return operation.result()

def deploy_model_to_endpoint(client, endpoint_name, model_name):
    """Deploy a machine learning model to an existing endpoint."""
    deployed_model = {
        "model": model_name,
        "display_name": "Deployment of Model",
        "dedicated_resources": {
            "min_replica_count": 1,
            "max_replica_count": 1,
            "machine_spec": {"machine_type": "n1-standard-4"},
        },
    }
    print(f"Deploying model {model_name} to endpoint {endpoint_name}...")
    operation = client.deploy_model(endpoint=endpoint_name, deployed_model=deployed_model)
    return operation.result()

@app.route('/')
def index():
    return render_template('index.html')

def gen_frames():
    camera = cv2.VideoCapture(0)  # Use the default camera
    try:
        while True:
            success, frame = camera.read()  # read the camera frame
            if not success:
                break
            else:
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    finally:
        camera.release()  # Ensure the camera is released when done

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@socketio.on('connect')
def test_connect():
    emit('my response', {'data': 'Connected'})

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

@app.route('/create_endpoint', methods=['POST'])
def create_endpoint_route():
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    location = os.getenv('GOOGLE_CLOUD_REGION', 'us-central1')
    display_name = request.json.get('display_name', 'My Model Endpoint')
    description = request.json.get('description', 'Endpoint for a model')

    client = init_client(location)
    endpoint = create_endpoint(client, project_id, location, display_name, description)
    return jsonify({"endpoint": endpoint.name})

@app.route('/deploy_model', methods=['POST'])
def deploy_model_route():
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    location = os.getenv('GOOGLE_CLOUD_REGION', 'us-central1')
    endpoint_name = request.json.get('endpoint_name')
    model_id = request.json.get('model_id')

    client = init_client(location)
    model_name = f'projects/{project_id}/locations/{location}/models/{model_id}'
    deployment_result = deploy_model_to_endpoint(client, endpoint_name, model_name)
    return jsonify({"deployment_result": deployment_result})

if __name__ == '__main__':
    socketio.run(app, debug=True)
