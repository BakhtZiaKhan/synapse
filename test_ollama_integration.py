#!/usr/bin/env python3
"""
Test script for Ollama integration with Synapse backend
"""

import asyncio
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from app.services.ollama_service import OllamaService

async def test_ollama_integration():
    """Test Ollama integration"""
    print("🧪 Testing Ollama Integration")
    print("=" * 50)
    
    try:
        # Initialize Ollama service
        ollama_service = OllamaService()
        
        print("✅ Ollama Service initialized")
        print(f"✅ Ollama URL: {ollama_service.ollama_url}")
        print(f"✅ Model: {ollama_service.model_name}")
        
        # Test connection
        print("\n🔗 Testing Ollama connection...")
        connection_ok = await ollama_service.test_connection()
        
        if connection_ok:
            print("✅ Ollama connection successful!")
            
            # Test with a sample transcript
            sample_transcript = """
            Meeting started at 10:00 AM. John discussed the new project timeline. 
            Sarah mentioned we need to hire two developers by next month. 
            Mike agreed to review the budget proposal by Friday. 
            The team decided to use React for the frontend and Node.js for the backend.
            Meeting ended at 11:00 AM.
            """
            
            print("\n📝 Testing transcript analysis...")
            analysis = await ollama_service.analyze_transcript(sample_transcript, "Project Planning Meeting")
            
            print("✅ Analysis completed successfully!")
            print(f"📋 Summary: {analysis.get('summary', 'N/A')}")
            print(f"📝 Action Items: {len(analysis.get('action_items', []))} items")
            print(f"🎯 Key Decisions: {len(analysis.get('key_decisions', []))} decisions")
            
        else:
            print("❌ Ollama connection failed!")
            print("\n📋 To fix this:")
            print("1. Install Ollama: https://ollama.ai/download")
            print("2. Download a model: ollama pull mistral")
            print("3. Start Ollama service")
            print("4. Run this test again")
        
        # Clean up
        await ollama_service.close()
        
        if connection_ok:
            print("\n✅ Ollama integration is working correctly!")
            print("\n🚀 You can now:")
            print("1. Start the backend server: python -m uvicorn app.main:app --reload")
            print("2. Upload audio/video files through the frontend")
            print("3. Get full analysis (transcription + summary + action items + key decisions)!")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    success = asyncio.run(test_ollama_integration())
    sys.exit(0 if success else 1) 