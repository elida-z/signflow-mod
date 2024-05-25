from google.cloud import speech
from config import google_application_credentials
import os

def create_speech_client():
    client = speech.SpeechClient()
    return client

def transcribe_audio(audio_path):
    client = create_speech_client()

    with open(audio_path, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US"
    )

    response = client.recognize(config=config, audio=audio)
    
    for result in response.results:
        print(f"Transcript: {result.alternatives[0].transcript}")

# Example usage
if __name__ == "__main__":
    transcribe_audio("test_capture.wav")
