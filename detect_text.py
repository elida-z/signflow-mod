from google.cloud import vision
from config import google_application_credentials
import os

def create_vision_client():
    client = vision.ImageAnnotatorClient()
    return client

def detect_text_in_image(image_path):
    client = create_vision_client()

    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations

    for text in texts:
        print(f"Text: {text.description}")

# Example usage
if __name__ == "__main__":
    detect_text_in_image("path/to/your/imagefile.jpg")
