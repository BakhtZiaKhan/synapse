import os
import aiofiles
from fastapi import UploadFile
from typing import List
import logging

logger = logging.getLogger(__name__)

# Supported audio and video formats
SUPPORTED_AUDIO_FORMATS = {
    '.mp3', '.wav', '.m4a', '.aac', '.ogg', '.flac', '.wma', '.aiff'
}

SUPPORTED_VIDEO_FORMATS = {
    '.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm'
}

SUPPORTED_FORMATS = SUPPORTED_AUDIO_FORMATS.union(SUPPORTED_VIDEO_FORMATS)

def validate_audio_file(file: UploadFile) -> bool:
    """
    Validate if the uploaded file is a supported audio or video format
    
    Args:
        file: Uploaded file object
        
    Returns:
        bool: True if file is valid, False otherwise
    """
    try:
        # Check if file has a name
        if not file.filename:
            logger.warning("File has no filename")
            return False
        
        # Get file extension
        file_extension = os.path.splitext(file.filename.lower())[1]
        
        # Check if extension is supported
        if file_extension not in SUPPORTED_FORMATS:
            logger.warning(f"Unsupported file format: {file_extension}")
            return False
        
        # Check content type (basic validation)
        content_type = file.content_type or ""
        if not (content_type.startswith("audio/") or content_type.startswith("video/")):
            logger.warning(f"Invalid content type: {content_type}")
            return False
        
        return True
        
    except Exception as e:
        logger.error(f"Error validating file: {str(e)}")
        return False

async def save_upload_file(file: UploadFile, job_id: str) -> str:
    """
    Save uploaded file to temporary storage
    
    Args:
        file: Uploaded file object
        job_id: Unique identifier for the processing job
        
    Returns:
        str: Path to the saved file
    """
    try:
        # Create uploads directory if it doesn't exist
        upload_dir = "uploads"
        os.makedirs(upload_dir, exist_ok=True)
        
        # Generate filename with job_id
        file_extension = os.path.splitext(file.filename)[1]
        filename = f"{job_id}{file_extension}"
        file_path = os.path.join(upload_dir, filename)
        
        # Save file
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        logger.info(f"File saved successfully: {file_path}")
        return file_path
        
    except Exception as e:
        logger.error(f"Error saving uploaded file: {str(e)}")
        raise Exception(f"Failed to save uploaded file: {str(e)}")

def get_file_size_mb(file_path: str) -> float:
    """
    Get file size in megabytes
    
    Args:
        file_path: Path to the file
        
    Returns:
        float: File size in MB
    """
    try:
        size_bytes = os.path.getsize(file_path)
        return size_bytes / (1024 * 1024)
    except Exception as e:
        logger.error(f"Error getting file size: {str(e)}")
        return 0.0

def is_file_too_large(file_path: str, max_size_mb: float = 100.0) -> bool:
    """
    Check if file is too large for processing
    
    Args:
        file_path: Path to the file
        max_size_mb: Maximum allowed size in MB
        
    Returns:
        bool: True if file is too large
    """
    file_size_mb = get_file_size_mb(file_path)
    return file_size_mb > max_size_mb

def cleanup_temp_file(file_path: str) -> bool:
    """
    Clean up temporary file
    
    Args:
        file_path: Path to the file to delete
        
    Returns:
        bool: True if file was deleted successfully
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"Temporary file cleaned up: {file_path}")
            return True
        return False
    except Exception as e:
        logger.error(f"Error cleaning up temporary file: {str(e)}")
        return False

def get_supported_formats() -> List[str]:
    """
    Get list of supported audio and video formats
    
    Returns:
        List[str]: List of supported file extensions
    """
    return list(SUPPORTED_FORMATS) 