import cv2
from model.load_model import get_model

model = get_model()

def preprocess(frame):
    """ Apply preprocessing steps before feeding the frame to the model. """
    frame_resized = cv2.resize(frame, (224, 224))
    frame_gray = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2GRAY)
    frame_normalized = frame_gray / 255.0
    frame_normalized = frame_normalized.reshape(224, 224, 1)
    return frame_normalized

def recognize_gestures(frame):
    """ Use the model to predict gestures based on the preprocessed frame. """
    result = model.predict(frame[None, :, :, :])
    return result

def annotate_frame(frame, results):
    """ Annotate the frame based on model's prediction results. """
    # Assuming results is a list of tuples (x, y, w, h, label)
    for (x, y, w, h, label) in results:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
    return frame

def generate_frames():
    """ Capture frames from the webcam, process, and yield them for HTTP streaming. """
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise Exception("Could not open video device")
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            processed_frame = preprocess(frame)
            gesture_results = recognize_gestures(processed_frame)
            annotated_frame = annotate_frame(frame, gesture_results)
            _, buffer = cv2.imencode('.jpg', annotated_frame)
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
    finally:
        cap.release()
