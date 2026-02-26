from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import os
import uuid
import logging
import traceback
from datetime import datetime

from crewai import Crew, Process
from app.agents import financial_analyst
from app.tasks import analyze_financial_document
from app.tools import read_financial_document

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Financial Document Analyzer",
    description="AI-powered financial document analysis using CrewAI and Gemini",
    version="1.0.0"
)

def run_crew(query: str, document_text: str):
    """Run the CrewAI agent with document text"""
    
    logger.info(f"Starting analysis with query: {query[:50]}...")
    
    try:
        # Create crew with single agent
        financial_crew = Crew(
            agents=[financial_analyst],
            tasks=[analyze_financial_document],
            process=Process.sequential,
            verbose=True
        )
        
        # Run analysis with document text and query
        result = financial_crew.kickoff({
            'query': query,
            'document_text': document_text
        })
        
        logger.info("Analysis completed successfully")
        return result
        
    except Exception as e:
        logger.error(f"Error in run_crew: {str(e)}")
        traceback.print_exc()
        raise

@app.get("/")
async def root():
    """Root endpoint with API info"""
    return {
        "message": "Financial Document Analyzer API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "analyze": "/analyze (POST)"
        }
    }

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "api_key_configured": os.getenv("GOOGLE_API_KEY") is not None,
        "server_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

@app.post("/analyze")
async def analyze_document(
    file: UploadFile = File(...),
    query: str = Form("Analyze this financial document for investment insights")
):
    """Upload and analyze a financial document"""
    
    # Create unique file ID
    file_id = str(uuid.uuid4())
    file_extension = os.path.splitext(file.filename)[1]
    file_path = f"data/{file_id}{file_extension}"
    
    try:
        # Create data directory if it doesn't exist
        os.makedirs("data", exist_ok=True)
        
        # Save uploaded file
        logger.info(f"📤 Uploading file: {file.filename}")
        content = await file.read()
        file_size = len(content)
        
        with open(file_path, "wb") as f:
            f.write(content)
        
        logger.info(f"✅ File saved: {file_path} ({file_size} bytes)")
        
        # Read and extract text from document
        logger.info("📄 Extracting text from document...")
        document_text = read_financial_document(file_path)
        logger.info(f"✅ Text extracted: {len(document_text)} characters")
        
        # Run analysis
        logger.info("🤖 Running AI analysis...")
        response = run_crew(query, document_text)
        
        return {
            "status": "success",
            "filename": file.filename,
            "file_size": file_size,
            "query": query,
            "analysis": str(response),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Error: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        # Clean up uploaded file
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                logger.info(f"🧹 Cleaned up: {file_path}")
            except Exception as e:
                logger.warning(f"⚠️ Cleanup failed: {e}")

# Simple bonus endpoints (optional)
@app.post("/analyze/queue")
async def analyze_with_queue(
    file: UploadFile = File(...),
    query: str = Form("Analyze this financial document")
):
    """Queue document for background processing (bonus feature)"""
    return {
        "message": "Queue feature - simplified version",
        "status": "pending",
        "filename": file.filename,
        "query": query,
        "note": "This is a placeholder. Full queue implementation would use Celery + Redis."
    }

@app.get("/queue/status/{task_id}")
async def get_queue_status(task_id: str):
    """Check status of a queued task"""
    return {
        "task_id": task_id,
        "status": "pending",
        "message": "Queue status endpoint"
    }

@app.get("/queue/stats")
async def queue_stats():
    """Get queue statistics"""
    return {
        "message": "Queue stats",
        "active_workers": 0,
        "queued_tasks": 0,
        "note": "Full queue stats would show Celery worker information"
    }

@app.get("/results")
async def list_results():
    """List all analysis results"""
    return {
        "message": "Results feature",
        "total": 0,
        "results": [],
        "note": "Full results would show data from database"
    }

if __name__ == "__main__":
    import uvicorn
    print("\n" + "=" * 60)
    print("🚀 Financial Document Analyzer v1.0.0")
    print("=" * 60)
    print("📝 API Documentation: http://localhost:8000/docs")
    print("🏥 Health Check: http://localhost:8000/health")
    print("📊 Test Analysis: POST to http://localhost:8000/analyze")
    print("=" * 60 + "\n")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)