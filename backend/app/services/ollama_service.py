import httpx
import json
import os
from typing import Dict, Any, Optional
import logging
import asyncio
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)

class OllamaService:
    """Service for handling Ollama LLM interactions"""
    
    def __init__(self):
        # Ollama configuration
        self.ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434")
        self.model_name = os.getenv("OLLAMA_MODEL", "gemma3")
        
        # HTTP client for Ollama API
        self.client = httpx.AsyncClient(timeout=300.0)  # 5 minutes timeout
        
        # Thread pool for running Ollama in background
        self.executor = ThreadPoolExecutor(max_workers=2)
    
    async def analyze_transcript(self, transcript: str, meeting_title: Optional[str] = None) -> Dict[str, Any]:
        """
        Analyze transcript using Ollama LLM
        
        Args:
            transcript: The meeting transcript to analyze
            meeting_title: Optional meeting title for context
            
        Returns:
            Dict containing summary, action_items, and key_decisions
        """
        try:
            logger.info(f"Starting transcript analysis with Ollama. Length: {len(transcript)} characters")
            
            # Construct the prompt for the LLM
            prompt = self._build_analysis_prompt(transcript, meeting_title)
            
            # Prepare the request payload for Ollama
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "num_predict": 512
                }
            }
            
            # Make request to Ollama API
            response = await self.client.post(
                f"{self.ollama_url}/api/generate",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code != 200:
                raise Exception(f"Ollama API error: {response.status_code} - {response.text}")
            
            result = response.json()
            
            # Extract the generated text
            analysis_text = result.get("response", "")
            
            if not analysis_text:
                raise Exception("No analysis received from Ollama")
            
            # Parse the JSON response from the LLM
            analysis = self._parse_analysis_response(analysis_text)
            
            logger.info("Transcript analysis completed successfully with Ollama")
            return analysis
            
        except Exception as e:
            logger.error(f"Error in Ollama transcript analysis: {str(e)}")
            raise Exception(f"Ollama analysis failed: {str(e)}")
    
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
    
    async def test_connection(self) -> bool:
        """
        Test connection to Ollama service
        
        Returns:
            bool: True if connection successful
        """
        try:
            response = await self.client.get(f"{self.ollama_url}/api/tags")
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Ollama connection test failed: {str(e)}")
            return False
    
    async def close(self):
        """Close the HTTP client and thread pool"""
        await self.client.aclose()
        self.executor.shutdown(wait=True) 