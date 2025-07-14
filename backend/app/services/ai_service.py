import httpx
import json
import os
from typing import Dict, Any, Optional
import logging
import whisper
import asyncio
from concurrent.futures import ThreadPoolExecutor

# Import Ollama service
from .ollama_service import OllamaService

logger = logging.getLogger(__name__)

class AIService:
    """Service for handling AI model interactions"""
    
    def __init__(self):
        # Configuration for local vs remote processing
        self.use_local_whisper = os.getenv("USE_LOCAL_WHISPER", "true").lower() == "true"
        
        # Hugging Face Spaces URLs - these will be configured via environment variables
        self.whisper_api_url = os.getenv("WHISPER_API_URL", "https://your-whisper-space.hf.space")
        self.llm_api_url = os.getenv("LLM_API_URL", "https://your-llm-space.hf.space")
        
        # API keys for Hugging Face Spaces (if required)
        self.whisper_api_key = os.getenv("WHISPER_API_KEY")
        self.llm_api_key = os.getenv("LLM_API_KEY")
        
        # HTTP client with timeout
        self.client = httpx.AsyncClient(timeout=300.0)  # 5 minutes timeout for processing
        
        # Thread pool for running Whisper in background
        self.executor = ThreadPoolExecutor(max_workers=2)
        
        # Load Whisper model if using local processing
        self.whisper_model = None
        if self.use_local_whisper:
            logger.info("Loading local Whisper model...")
            self.whisper_model = whisper.load_model("base")
            logger.info("Whisper model loaded successfully")
        
        # Initialize Ollama service
        self.ollama_service = OllamaService()
    
    async def transcribe_audio(self, file_path: str) -> str:
        """
        Transcribe audio file using Whisper model (local or remote)
        
        Args:
            file_path: Path to the audio file
            
        Returns:
            str: Transcribed text
        """
        try:
            logger.info(f"Starting transcription for file: {file_path}")
            
            if self.use_local_whisper and self.whisper_model:
                # Use local Whisper model
                logger.info("Using local Whisper model for transcription")
                
                # Run Whisper in a thread pool to avoid blocking
                loop = asyncio.get_event_loop()
                transcript = await loop.run_in_executor(
                    self.executor,
                    self._transcribe_with_local_whisper,
                    file_path
                )
                
                logger.info(f"Local transcription completed successfully. Length: {len(transcript)} characters")
                return transcript
            else:
                # Use remote Hugging Face API
                logger.info("Using remote Whisper API for transcription")
                
                # Prepare the file for upload
                with open(file_path, "rb") as audio_file:
                    files = {"file": ("audio.wav", audio_file, "audio/wav")}
                    
                    headers = {}
                    if self.whisper_api_key:
                        headers["Authorization"] = f"Bearer {self.whisper_api_key}"
                    
                    # Make request to Whisper API
                    response = await self.client.post(
                        f"{self.whisper_api_url}/predict",
                        files=files,
                        headers=headers
                    )
                    
                    if response.status_code != 200:
                        raise Exception(f"Whisper API error: {response.status_code} - {response.text}")
                    
                    result = response.json()
                    
                    # Extract transcript from response
                    # The exact structure depends on your Hugging Face Space configuration
                    transcript = result.get("data", [""])[0] if isinstance(result.get("data"), list) else result.get("text", "")
                    
                    if not transcript:
                        raise Exception("No transcript received from Whisper API")
                    
                    logger.info(f"Remote transcription completed successfully. Length: {len(transcript)} characters")
                    return transcript
                
        except Exception as e:
            logger.error(f"Error in transcription: {str(e)}")
            raise Exception(f"Transcription failed: {str(e)}")
    
    def _transcribe_with_local_whisper(self, file_path: str) -> str:
        """
        Transcribe audio using local Whisper model (runs in thread pool)
        
        Args:
            file_path: Path to the audio file
            
        Returns:
            str: Transcribed text
        """
        try:
            # Use Whisper to transcribe the audio
            result = self.whisper_model.transcribe(file_path)
            return result["text"]
        except Exception as e:
            logger.error(f"Error in local Whisper transcription: {str(e)}")
            raise Exception(f"Local Whisper transcription failed: {str(e)}")
    
    async def analyze_transcript(self, transcript: str, meeting_title: Optional[str] = None) -> Dict[str, Any]:
        """
        Analyze transcript using Ollama LLM (local) or Hugging Face API (fallback)
        
        Args:
            transcript: The meeting transcript to analyze
            meeting_title: Optional meeting title for context
            
        Returns:
            Dict containing summary, action_items, and key_decisions
        """
        try:
            logger.info(f"Starting transcript analysis. Length: {len(transcript)} characters")
            
            # Try Ollama first (local)
            try:
                # Test if Ollama is available
                if await self.ollama_service.test_connection():
                    logger.info("Using Ollama for transcript analysis")
                    return await self.ollama_service.analyze_transcript(transcript, meeting_title)
                else:
                    logger.warning("Ollama not available, falling back to Hugging Face API")
            except Exception as e:
                logger.warning(f"Ollama analysis failed, falling back to Hugging Face API: {str(e)}")
            
            # Fallback to Hugging Face API
            logger.info("Using Hugging Face API for transcript analysis")
            
            # Construct the prompt for the LLM
            prompt = self._build_analysis_prompt(transcript, meeting_title)
            
            # Prepare the request payload
            payload = {
                "data": [
                    prompt,  # The prompt text
                    "json",  # Expected output format
                    0.7,     # Temperature for creativity
                    512,     # Max tokens
                ]
            }
            
            headers = {"Content-Type": "application/json"}
            if self.llm_api_key:
                headers["Authorization"] = f"Bearer {self.llm_api_key}"
            
            # Make request to LLM API
            response = await self.client.post(
                f"{self.llm_api_url}/predict",
                json=payload,
                headers=headers
            )
            
            if response.status_code != 200:
                raise Exception(f"LLM API error: {response.status_code} - {response.text}")
            
            result = response.json()
            
            # Extract the analysis from response
            # The exact structure depends on your Hugging Face Space configuration
            analysis_text = result.get("data", [""])[0] if isinstance(result.get("data"), list) else result.get("text", "")
            
            if not analysis_text:
                raise Exception("No analysis received from LLM API")
            
            # Parse the JSON response from the LLM
            analysis = self._parse_analysis_response(analysis_text)
            
            logger.info("Transcript analysis completed successfully")
            return analysis
            
        except Exception as e:
            logger.error(f"Error in transcript analysis: {str(e)}")
            raise Exception(f"Analysis failed: {str(e)}")
    
    def _build_analysis_prompt(self, transcript: str, meeting_title: Optional[str] = None) -> str:
        """
        Build the prompt for LLM analysis
        """
        title_context = f"Meeting Title: {meeting_title}\n\n" if meeting_title else ""
        
        prompt = f"""You are an expert meeting assistant. Analyze the following meeting transcript and provide a structured analysis.

{title_context}Meeting Transcript:
{transcript}

Your response must be a single, valid JSON object with these exact keys:
- "summary": A 3-sentence overview of the meeting
- "action_items": A list of strings, where each string is a specific task assigned to someone
- "key_decisions": A list of strings describing any decisions made during the meeting

Focus on:
1. Clear, actionable items with assignees when possible
2. Important decisions and their implications
3. Key topics discussed and outcomes

Return only the JSON object, no additional text:"""
        
        return prompt
    
    def _parse_analysis_response(self, response_text: str) -> Dict[str, Any]:
        """
        Parse the LLM response and extract structured data
        """
        try:
            # Clean the response text
            cleaned_text = response_text.strip()
            
            # Try to find JSON in the response
            if cleaned_text.startswith("{"):
                json_str = cleaned_text
            else:
                # Look for JSON between backticks or other markers
                import re
                json_match = re.search(r'\{.*\}', cleaned_text, re.DOTALL)
                if json_match:
                    json_str = json_match.group(0)
                else:
                    raise Exception("No valid JSON found in response")
            
            # Parse the JSON
            analysis = json.loads(json_str)
            
            # Validate required fields
            required_fields = ["summary", "action_items", "key_decisions"]
            for field in required_fields:
                if field not in analysis:
                    analysis[field] = [] if field in ["action_items", "key_decisions"] else ""
            
            return analysis
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {str(e)}")
            # Fallback: return basic structure
            return {
                "summary": "Analysis could not be parsed properly.",
                "action_items": [],
                "key_decisions": []
            }
        except Exception as e:
            logger.error(f"Error parsing analysis response: {str(e)}")
            return {
                "summary": "Analysis failed to process properly.",
                "action_items": [],
                "key_decisions": []
            }
    
    async def close(self):
        """Close the HTTP client, thread pool, and Ollama service"""
        await self.client.aclose()
        self.executor.shutdown(wait=True)
        await self.ollama_service.close() 