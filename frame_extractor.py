#utils/frame_extractor.py
import cv2
import os
from google.cloud import storage

def extract_frames(video_path, gcs_bucket_name, frame_rate=30, output_format='jpg'):
    # No need to explicitly create a client if using environment variable
    client = storage.Client()  
    bucket = client.bucket(gcs_bucket_name)

    if not os.path.exists(video_path):
        raise ValueError("Invalid video path.")

    vidcap = cv2.VideoCapture(video_path)
    count = 0
    success, image = vidcap.read()
    while success:
        if count % frame_rate == 0:
            frame_filename = f"frame_{count//frame_rate}.{output_format}"
            _, buffer = cv2.imencode('.' + output_format, image)
            blob = bucket.blob(frame_filename)
            blob.upload_from_string(buffer.tobytes())
            # Add logging or print statements for progress tracking
        success, image = vidcap.read()
        count += 1
    vidcap.release()

# Example usage (assuming you have set up Google Cloud credentials)
extract_frames("path/to/video.mp4", "your-gcs-bucket-name")