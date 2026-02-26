import os
from dotenv import load_dotenv

print("Testing .env file...")
print("-" * 40)

# Load .env
load_dotenv()

# Get API key
key = os.getenv('GOOGLE_API_KEY')
print(f"GOOGLE_API_KEY from os.getenv: {key is not None}")
if key:
    print(f"Key length: {len(key)}")
    print(f"First 10 chars: {key[:10]}")

# Read file directly
print("\nReading .env file directly:")
try:
    with open('.env', 'r') as f:
        content = f.read()
        print(f"Raw content: {repr(content)}")
        if 'GOOGLE_API_KEY=' in content:
            parts = content.split('=')
            if len(parts) > 1:
                key_from_file = parts[1].strip()
                print(f"Key from file: {key_from_file[:10]}...")
except Exception as e:
    print(f"Error: {e}")

print("-" * 40)
