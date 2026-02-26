## Importing libraries and files
import os
from dotenv import load_dotenv
load_dotenv()

from crewai import Agent
from langchain_google_genai import ChatGoogleGenerativeAI

# Set dummy OpenAI key to prevent CrewAI from looking for it
os.environ["OPENAI_API_KEY"] = "sk-dummy-value-for-crewai"

print("=" * 50)
print("🚀 Initializing Financial Document Analyzer")
print("=" * 50)

# Load API key
print("\n🔍 Looking for API key...")
google_api_key = os.getenv("GOOGLE_API_KEY")

if not google_api_key:
    print("❌ ERROR: GOOGLE_API_KEY not found in environment variables")
    print("Please create a .env file with: GOOGLE_API_KEY=your_key_here")
    exit(1)

print(f"✅ API key found (starts with: {google_api_key[:10]}...)")

# Initialize Gemini model
try:
    print("\n🔄 Initializing Gemini 2.5 Flash model...")
    llm = ChatGoogleGenerativeAI(
        model="models/gemma-3-27b-it",
        google_api_key=google_api_key,
        temperature=0.7
    )
    
    # Test the model
    test_response = llm.invoke("Say 'connected' in one word")
    print(f"✅ Model connected: {test_response.content}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)

print("\n🤖 Creating agents...")

# Document Verifier Agent
verifier = Agent(
    role="Senior Financial Document Verifier",
    goal="Accurately verify and extract financial data from documents",
    backstory=(
        "You are a certified financial document specialist with 15 years of experience "
        "at top accounting firms. You have verified thousands of financial reports."
    ),
    llm=llm,
    verbose=True,
    allow_delegation=False
)

# Financial Analyst Agent
financial_analyst = Agent(
    role="Chartered Financial Analyst",
    goal="Provide comprehensive financial analysis based on verified document data",
    backstory=(
        "You are a Chartered Financial Analyst (CFA) with 20 years of experience "
        "at leading investment banks."
    ),
    llm=llm,
    verbose=True,
    allow_delegation=False
)

print("✅ Agents created successfully")