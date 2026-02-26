import os
import json
from celery import Celery
from datetime import datetime
from crewai import Crew, Process
from app.agents import financial_analyst
from app.tasks import analyze_financial_document
from app.tools import read_financial_document

# Redis connection
REDIS_URL = "redis://localhost:6379/0"

# Create Celery app
celery_app = Celery(
    "financial_analyzer",
    broker=REDIS_URL,
    backend=REDIS_URL
)

# Simple JSON database
DB_FILE = "results.json"

def save_result(document_id, filename, query, result):
    """Save result to JSON file"""
    try:
        if os.path.exists(DB_FILE):
            with open(DB_FILE, 'r') as f:
                data = json.load(f)
        else:
            data = []
        
        data.append({
            "document_id": document_id,
            "filename": filename,
            "query": query,
            "result": str(result),
            "timestamp": datetime.now().isoformat(),
            "status": "completed"
        })
        
        with open(DB_FILE, 'w') as f:
            json.dump(data, f, indent=2)
            print(f"✅ Result saved for {filename}")
            
    except Exception as e:
        print(f"❌ Save error: {e}")

@celery_app.task(bind=True)
def analyze_document_task(self, document_id, file_path, filename, query):
    """Background task for document analysis"""
    
    try:
        print(f"\n🚀 Starting analysis task for {filename}")
        
        # Update progress
        self.update_state(state="PROGRESS", meta={"progress": 10, "status": "Reading document..."})
        print("📄 Reading document...")
        
        # Read document
        document_text = read_financial_document(file_path)
        
        # Update progress
        self.update_state(state="PROGRESS", meta={"progress": 50, "status": "Analyzing with AI..."})
        print("🤖 Analyzing with AI...")
        
        # Run analysis
        crew = Crew(
            agents=[financial_analyst],
            tasks=[analyze_financial_document],
            process=Process.sequential,
            verbose=True
        )
        
        result = crew.kickoff({
            'query': query,
            'document_text': document_text
        })
        
        print("✅ Analysis complete")
        
        # Save result
        save_result(document_id, filename, query, result)
        
        # Clean up
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"🧹 Cleaned up: {file_path}")
        
        return {
            "document_id": document_id,
            "status": "completed",
            "result": str(result)
        }
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return {
            "document_id": document_id,
            "status": "failed",
            "error": str(e)
        }

print("✅ Celery worker initialized successfully")