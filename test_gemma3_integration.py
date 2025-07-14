#!/usr/bin/env python3
"""
Test script for Gemma 3 integration with Synapse backend
"""

import asyncio
import sys
import os
import json

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from app.services.ollama_service import OllamaService

async def test_gemma3_integration():
    """Test Gemma 3 integration for meeting analysis"""
    print("🧪 Testing Gemma 3 Integration for Meeting Analysis")
    print("=" * 60)
    
    try:
        # Initialize Ollama service with Gemma 3
        ollama_service = OllamaService()
        ollama_service.model_name = "gemma3"  # Override to use Gemma 3
        
        print("✅ Ollama Service initialized")
        print(f"✅ Ollama URL: {ollama_service.ollama_url}")
        print(f"✅ Model: {ollama_service.model_name}")
        
        # Test connection
        print("\n🔗 Testing Ollama connection...")
        connection_ok = await ollama_service.test_connection()
        
        if connection_ok:
            print("✅ Ollama connection successful!")
            
            # Test with a realistic meeting transcript
            sample_transcript = """
            Meeting started at 10:00 AM. John discussed the new project timeline and mentioned we need to complete the frontend by next Friday. 
            Sarah mentioned we need to hire two developers by next month and suggested posting the job ads this week. 
            Mike agreed to review the budget proposal by Friday and will send feedback to the team. 
            The team decided to use React for the frontend and Node.js for the backend. 
            Lisa volunteered to create the project documentation by Wednesday. 
            Meeting ended at 11:00 AM.
            """
            
            print("\n📝 Testing meeting transcript analysis with Gemma 3...")
            analysis = await ollama_service.analyze_transcript(sample_transcript, "Project Planning Meeting")
            
            print("✅ Analysis completed successfully!")
            print(f"\n📋 Summary: {analysis.get('summary', 'N/A')}")
            print(f"\n📝 Action Items ({len(analysis.get('action_items', []))} items):")
            for i, item in enumerate(analysis.get('action_items', []), 1):
                print(f"   {i}. {item}")
            print(f"\n🎯 Key Decisions ({len(analysis.get('key_decisions', []))} decisions):")
            for i, decision in enumerate(analysis.get('key_decisions', []), 1):
                print(f"   {i}. {decision}")
            
        else:
            print("❌ Ollama connection failed!")
            print("\n📋 To fix this:")
            print("1. Make sure Ollama is running")
            print("2. Check if Gemma 3 is installed: ollama list")
            print("3. Install Gemma 3 if needed: ollama pull gemma3")
        
        # Clean up
        await ollama_service.close()
        
        if connection_ok:
            print("\n✅ Gemma 3 integration is working correctly!")
            print("\n🚀 You can now:")
            print("1. Start the backend server: python -m uvicorn app.main:app --reload")
            print("2. Upload audio/video files through the frontend")
            print("3. Get full analysis (transcription + summary + action items + key decisions)!")
            print("4. All processing happens locally with Gemma 3!")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    success = asyncio.run(test_gemma3_integration())
    sys.exit(0 if success else 1) 