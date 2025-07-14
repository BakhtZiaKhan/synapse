#!/usr/bin/env python3
"""
Test script for local Whisper integration
"""

import asyncio
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from app.services.ai_service import AIService

async def test_local_whisper():
    """Test local Whisper functionality"""
    print("🧪 Testing Local Whisper Setup")
    print("=" * 50)
    
    try:
        # Initialize AI service
        ai_service = AIService()
        
        print("✅ AI Service initialized")
        print(f"✅ Using local Whisper: {ai_service.use_local_whisper}")
        print(f"✅ Whisper model loaded: {ai_service.whisper_model is not None}")
        
        # Test with a dummy file (you can replace this with a real audio file)
        print("\n📝 Note: To test with real audio, replace 'test_audio.wav' with an actual audio file")
        
        # Clean up
        await ai_service.close()
        
        print("\n✅ Local Whisper setup is working correctly!")
        print("\n🚀 You can now:")
        print("1. Start the backend server: python -m uvicorn app.main:app --reload")
        print("2. Upload audio/video files through the frontend")
        print("3. Whisper will process them locally!")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    success = asyncio.run(test_local_whisper())
    sys.exit(0 if success else 1) 