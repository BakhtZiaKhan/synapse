import os
import tempfile
from moviepy.editor import VideoFileClip
import logging

logger = logging.getLogger(__name__)

def extract_audio_from_video(video_path: str) -> str:
    """
    Extract audio from video file and save as temporary WAV file
    
    Args:
        video_path: Path to the video file
        
    Returns:
        str: Path to the extracted audio file
    """
    try:
        logger.info(f"Extracting audio from video: {video_path}")
        
        # Create temporary file for audio
        temp_audio = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
        temp_audio_path = temp_audio.name
        temp_audio.close()
        
        # Load video and extract audio
        video = VideoFileClip(video_path)
        audio = video.audio
        
        if audio is None:
            raise Exception("No audio track found in video file")
        
        # Write audio to temporary file
        audio.write_audiofile(temp_audio_path, verbose=False, logger=None)
        
        # Close video to free up resources
        video.close()
        
        logger.info(f"Audio extracted successfully to: {temp_audio_path}")
        return temp_audio_path
        
    except Exception as e:
        logger.error(f"Error extracting audio from video: {str(e)}")
        raise Exception(f"Failed to extract audio from video: {str(e)}")

def cleanup_temp_audio(audio_path: str) -> bool:
    """
    Clean up temporary audio file
    
    Args:
        audio_path: Path to the temporary audio file
        
    Returns:
        bool: True if file was deleted successfully
    """
    try:
        if os.path.exists(audio_path):
            os.remove(audio_path)
            logger.info(f"Temporary audio file cleaned up: {audio_path}")
            return True
        return False
    except Exception as e:
        logger.error(f"Error cleaning up temporary audio file: {str(e)}")
        return False

def is_video_file(file_path: str) -> bool:
    """
    Check if file is a video file based on extension
    
    Args:
        file_path: Path to the file
        
    Returns:
        bool: True if file is a video
    """
    video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm'}
    file_extension = os.path.splitext(file_path.lower())[1]
    return file_extension in video_extensions 