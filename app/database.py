import os
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

# MongoDB connection
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "financial_analyzer")

# Async client for FastAPI
class MongoDB:
    client: AsyncIOMotorClient = None
    database = None

db = MongoDB()

async def connect_to_mongo():
    """Connect to MongoDB"""
    print("🔌 Connecting to MongoDB...")
    db.client = AsyncIOMotorClient(MONGODB_URL)
    db.database = db.client[DATABASE_NAME]
    
    # Create indexes
    await db.database.documents.create_index("upload_date")
    await db.database.documents.create_index("status")
    await db.database.analysis_results.create_index("document_id")
    await db.database.analysis_results.create_index("created_at")
    
    print("✅ Connected to MongoDB")

async def close_mongo_connection():
    """Close MongoDB connection"""
    if db.client:
        db.client.close()
        print("🔌 MongoDB connection closed")

# Collection getters
def get_documents_collection():
    return db.database.documents

def get_analysis_collection():
    return db.database.analysis_results

def get_users_collection():
    return db.database.users

# Sync client for Celery
def get_sync_db():
    client = MongoClient(MONGODB_URL)
    return client[DATABASE_NAME]