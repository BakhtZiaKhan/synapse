from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import datetime

class ProcessingStatus(str, Enum):
    """Status of meeting processing"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class MeetingRequest(BaseModel):
    """Request model for meeting processing"""
    meeting_title: Optional[str] = Field(None, description="Optional title for the meeting")
    
class MeetingResponse(BaseModel):
    """Response model for meeting processing"""
    job_id: str = Field(..., description="Unique identifier for the processing job")
    status: ProcessingStatus = Field(..., description="Current status of the processing")
    message: str = Field(..., description="Human-readable message about the status")

class MeetingAnalysis(BaseModel):
    """Model for meeting analysis results"""
    summary: str = Field(..., description="3-sentence summary of the meeting")
    action_items: List[str] = Field(..., description="List of specific action items")
    key_decisions: List[str] = Field(..., description="List of key decisions made")

class MeetingRecord(BaseModel):
    """Model for a complete meeting record"""
    id: str = Field(..., description="Unique meeting identifier")
    title: str = Field(..., description="Meeting title")
    filename: str = Field(..., description="Original uploaded filename")
    status: ProcessingStatus = Field(..., description="Processing status")
    transcript: Optional[str] = Field(None, description="Full meeting transcript")
    summary: Optional[str] = Field(None, description="Meeting summary")
    action_items: Optional[List[str]] = Field(None, description="Action items")
    key_decisions: Optional[List[str]] = Field(None, description="Key decisions")
    error_message: Optional[str] = Field(None, description="Error message if processing failed")
    created_at: str = Field(..., description="ISO timestamp of creation")
    updated_at: str = Field(..., description="ISO timestamp of last update")

class AIAnalysisRequest(BaseModel):
    """Request model for AI analysis"""
    transcript: str = Field(..., description="Meeting transcript to analyze")
    meeting_title: Optional[str] = Field(None, description="Optional meeting title for context")

class AIAnalysisResponse(BaseModel):
    """Response model for AI analysis"""
    summary: str = Field(..., description="Meeting summary")
    action_items: List[str] = Field(..., description="List of action items")
    key_decisions: List[str] = Field(..., description="List of key decisions")
    confidence_score: Optional[float] = Field(None, description="Confidence score of the analysis")

class HealthCheck(BaseModel):
    """Health check response model"""
    status: str = Field(..., description="Service status")
    timestamp: str = Field(..., description="Current timestamp")
    version: str = Field(..., description="API version") 