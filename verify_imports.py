try:
    from dotenv import load_dotenv
    import google.generativeai as genai
    print("Imports successful")
except ImportError as e:
    print("Import error:", e)
