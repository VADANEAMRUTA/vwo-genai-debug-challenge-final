from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class DocumentModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    filename: str
    file_size: int
    upload_date: datetime = Field(default_factory=datetime.now)
    user_id: Optional[str] = None
    status: str = "pending"  # pending, processing, completed, failed
    queue_position: Optional[int] = None
    
    class Config:
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "filename": "annual_report.pdf",
                "file_size": 1048576,
                "status": "completed"
            }
        }

class AnalysisResultModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    document_id: str
    query: str
    verification_result: Dict[str, Any]
    financial_analysis: str
    risk_assessment: Optional[str] = None
    investment_advice: Optional[str] = None
    processing_time: float
    created_at: datetime = Field(default_factory=datetime.now)
    model_used: str = "gemini-2.5-flash"
    
    class Config:
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "document_id": "507f1f77bcf86cd799439011",
                "query": "Analyze financial health",
                "processing_time": 15.5
            }
        }

class UserModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    email: str
    name: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    total_analyses: int = 0
    api_calls: int = 0
    
    class Config:
        json_encoders = {ObjectId: str}