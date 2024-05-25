from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access environment variables
google_application_credentials = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
google_cloud_project = os.getenv('GOOGLE_CLOUD_PROJECT')
google_cloud_region = os.getenv('GOOGLE_CLOUD_REGION')
google_cloud_storage_bucket = os.getenv('GOOGLE_CLOUD_STORAGE_BUCKET')
vertex_ai_api_endpoint = os.getenv('VERTEX_AI_API_ENDPOINT')
video_intelligence_api_endpoint = os.getenv('VIDEO_INTELLIGENCE_API_ENDPOINT')
vision_api_endpoint = os.getenv('VISION_API_ENDPOINT')
google_api_key = os.getenv('GOOGLE_API_KEY')
gemini_api_key = os.getenv('GEMINI_API_KEY')

def get_google_api_key():
    return google_api_key

def get_gemini_api_key():
    return gemini_api_key

# Example of using the functions
if __name__ == "__main__":
    print("Google Application Credentials:", google_application_credentials)
    print("Google Cloud Project:", google_cloud_project)
    print("Google Cloud Region:", google_cloud_region)
    print("Google Cloud Storage Bucket:", google_cloud_storage_bucket)
    print("Vertex AI API Endpoint:", vertex_ai_api_endpoint)
    print("Video Intelligence API Endpoint:", video_intelligence_api_endpoint)
    print("Vision API Endpoint:", vision_api_endpoint)
    print("Google API Key:", get_google_api_key())
    print("Gemini API Key:", get_gemini_api_key())
