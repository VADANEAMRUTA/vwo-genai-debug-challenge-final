import os
from dotenv import load_dotenv

print("Current directory:", os.getcwd())
print("Files:", os.listdir('.'))

load_dotenv()
print("After load_dotenv()")

key = os.getenv('GOOGLE_API_KEY')
print(f"GOOGLE_API_KEY found: {key is not None}")
if key:
    print(f"Key length: {len(key)}")
    print(f"First 10 chars: {key[:10]}")
