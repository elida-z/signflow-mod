import os
from google.cloud import storage, vision, speech, texttospeech, language_v1
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Google Cloud Storage client
def init_storage_client():
    return storage.Client()

def upload_frame(frame_path):
    bucket_name = os.getenv('GOOGLE_CLOUD_STORAGE_BUCKET')
    client = init_storage_client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(os.path.basename(frame_path))
    blob.upload_from_filename(frame_path)
    return blob.public_url

def generate_content_from_frames(frame_uris, prompt):
    parts = [{'text': prompt}]
    for uri in frame_uris:
        parts.append({'fileData': {'fileUri': uri, 'mimeType': 'image/jpeg'}})
    response = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest").generate_content(parts)
    return response.text

def analyze_image(image_content):
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_content)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    return [text.description for text in texts]

def transcribe_audio(audio_content):
    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
        enable_speaker_diarization=True,
        diarization_speaker_count=2
    )
    audio = speech.RecognitionAudio(content=audio_content)
    response = client.recognize(config=config, audio=audio)
    return [{"transcript": result.alternatives[0].transcript, "confidence": result.alternatives[0].confidence} for result in response.results]

def synthesize_speech(text):
    client = texttospeech.TextToSpeechClient()
    input_text = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL)
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    response = client.synthesize_speech(input=input_text, voice=voice, audio_config=audio_config)
    return response.audio_content

def analyze_sentiment(text):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    response = client.analyze_sentiment(document=document)
    sentiment = response.document_sentiment
    return {"score": sentiment.score, "magnitude": sentiment.magnitude}
