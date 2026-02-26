import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    print("❌ No API key found in .env file")
    print("Please make sure GOOGLE_API_KEY is set in your .env file")
    exit(1)

print(f"✅ API key found (starts with: {api_key[:10]}...)")

# Configure the Gemini API
genai.configure(api_key=api_key)

print("\n📋 Available models that support generateContent:")
print("=" * 60)

try:
    # List all models
    models = genai.list_models()
    
    found_models = False
    for model in models:
        # Check if the model supports content generation
        if 'generateContent' in model.supported_generation_methods:
            print(f"✅ Model: {model.name}")
            print(f"   Display name: {model.display_name}")
            print(f"   Description: {model.description[:100]}...")
            print(f"   Supported methods: {model.supported_generation_methods}")
            print("-" * 60)
            found_models = True
    
    if not found_models:
        print("No models found that support generateContent")
        
except Exception as e:
    print(f"❌ Error listing models: {e}")
    
print("\n💡 Tip: Use the full model name from above in your agents.py")
print("Example: model='models/gemini-1.5-pro' or 'gemini-1.5-pro'")