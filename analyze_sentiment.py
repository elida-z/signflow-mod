from google.cloud import language_v1
from config import google_application_credentials
import os

def create_language_client():
    client = language_v1.LanguageServiceClient()
    return client

def analyze_sentiment(text):
    client = create_language_client()
    
    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )
    
    response = client.analyze_sentiment(document=document)
    sentiment = response.document_sentiment

    print(f"Sentiment: {sentiment.score}, {sentiment.magnitude}")

# Example usage
if __name__ == "__main__":
    analyze_sentiment("Your text here")
