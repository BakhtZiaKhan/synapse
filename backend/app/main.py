from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import uuid
import logging
from datetime import datetime
from typing import Optional
import httpx
import json

logger = logging.getLogger(__name__)

from .models import MeetingRequest, MeetingResponse, ProcessingStatus
from .services.ai_service import AIService
from .services.database_service import DatabaseService
from .utils.audio_utils import validate_audio_file, save_upload_file
from .utils.video_utils import extract_audio_from_video, is_video_file, cleanup_temp_audio

app = FastAPI(
    title="Synapse Meeting Assistant API",
    description="AI-powered meeting analysis and transcription service",
    version="1.0.0"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
ai_service = AIService()
db_service = DatabaseService()

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Synapse Meeting Assistant API", "status": "healthy"}

@app.post("/api/process-meeting", response_model=MeetingResponse)
async def process_meeting(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    meeting_title: Optional[str] = None
):
    """
    Process an uploaded meeting audio file and generate analysis
    """
    try:
        # Validate the uploaded file
        if not validate_audio_file(file):
            raise HTTPException(
                status_code=400, 
                detail="Invalid file format. Please upload an audio file (mp3, wav, m4a, etc.)"
            )
        
        # Generate unique ID for this processing job
        job_id = str(uuid.uuid4())
        
        # Save the uploaded file temporarily
        file_path = await save_upload_file(file, job_id)
        
        # Create initial database record
        meeting_data = {
            "id": job_id,
            "title": meeting_title or f"Meeting {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "filename": file.filename,
            "status": ProcessingStatus.PROCESSING,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        await db_service.create_meeting(meeting_data)
        
        # Start background processing
        background_tasks.add_task(
            process_meeting_background,
            job_id,
            file_path,
            meeting_title
        )
        
        return MeetingResponse(
            job_id=job_id,
            status=ProcessingStatus.PROCESSING,
            message="Meeting processing started. Check status with the job_id."
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing meeting: {str(e)}")

@app.get("/api/meeting-status/{job_id}")
async def get_meeting_status(job_id: str):
    """
    Get the status and results of a meeting processing job
    """
    try:
        meeting = await db_service.get_meeting(job_id)
        if not meeting:
            raise HTTPException(status_code=404, detail="Meeting not found")
        
        return meeting
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving meeting status: {str(e)}")

@app.get("/api/meetings")
async def get_meetings(limit: int = 10, offset: int = 0):
    """
    Get list of processed meetings
    """
    try:
        meetings = await db_service.get_meetings(limit, offset)
        return {"meetings": meetings, "total": len(meetings)}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving meetings: {str(e)}")

async def process_meeting_background(job_id: str, file_path: str, meeting_title: Optional[str]):
    """
    Background task to process the meeting audio or video file
    """
    temp_audio_path = None
    try:
        # Update status to processing
        await db_service.update_meeting_status(job_id, ProcessingStatus.PROCESSING)
        
        # Step 1: Handle video files by extracting audio
        processing_path = file_path
        if is_video_file(file_path):
            logger.info(f"Processing video file: {file_path}")
            temp_audio_path = extract_audio_from_video(file_path)
            processing_path = temp_audio_path
        
        # Step 2: Transcribe audio using Whisper
        transcript = await ai_service.transcribe_audio(processing_path)
        
        # Step 3: Analyze transcript using LLM
        analysis = await ai_service.analyze_transcript(transcript)
        
        # Step 4: Save results to database
        results = {
            "transcript": transcript,
            "summary": analysis.get("summary", ""),
            "action_items": analysis.get("action_items", []),
            "key_decisions": analysis.get("key_decisions", []),
            "status": ProcessingStatus.COMPLETED,
            "updated_at": datetime.now().isoformat()
        }
        
        await db_service.update_meeting_results(job_id, results)
        
        # Clean up temporary files
        if os.path.exists(file_path):
            os.remove(file_path)
        if temp_audio_path and os.path.exists(temp_audio_path):
            cleanup_temp_audio(temp_audio_path)
            
    except Exception as e:
        # Update status to failed
        await db_service.update_meeting_status(job_id, ProcessingStatus.FAILED, str(e))
        
        # Clean up temporary files
        if os.path.exists(file_path):
            os.remove(file_path)
        if temp_audio_path and os.path.exists(temp_audio_path):
            cleanup_temp_audio(temp_audio_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 