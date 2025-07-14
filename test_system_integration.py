#!/usr/bin/env python3
"""
Test script to verify system integration
"""

import asyncio
import httpx
import json
import os

async def test_backend_health():
    """Test if backend is running"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:8000/")
            if response.status_code == 200:
                print("✅ Backend is running")
                return True
            else:
                print(f"❌ Backend health check failed: {response.status_code}")
                return False
    except Exception as e:
        print(f"❌ Backend connection failed: {e}")
        return False

async def test_ollama_connection():
    """Test if Ollama is running and has the correct model"""
    try:
        async with httpx.AsyncClient() as client:
            # Test Ollama connection
            response = await client.get("http://localhost:11434/api/tags")
            if response.status_code == 200:
                models = response.json().get("models", [])
                gemma_models = [m for m in models if "gemma" in m.get("name", "").lower()]
                if gemma_models:
                    print(f"✅ Ollama is running with models: {[m['name'] for m in gemma_models]}")
                    return True
                else:
                    print("❌ Ollama is running but no Gemma models found")
                    return False
            else:
                print(f"❌ Ollama connection failed: {response.status_code}")
                return False
    except Exception as e:
        print(f"❌ Ollama connection failed: {e}")
        return False

async def test_ollama_model():
    """Test if the Gemma model can generate a response"""
    try:
        async with httpx.AsyncClient() as client:
            payload = {
                "model": "gemma3",
                "prompt": "Hello, can you respond with 'Test successful'?",
                "stream": False
            }
            
            response = await client.post(
                "http://localhost:11434/api/generate",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                if "response" in result:
                    print("✅ Ollama Gemma model is working")
                    return True
                else:
                    print("❌ Ollama model test failed - no response")
                    return False
            else:
                print(f"❌ Ollama model test failed: {response.status_code} - {response.text}")
                return False
    except Exception as e:
        print(f"❌ Ollama model test failed: {e}")
        return False

async def test_backend_upload_endpoint():
    """Test if backend upload endpoint is accessible"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:8000/api/process-meeting")
            # Should return 405 Method Not Allowed for GET, but endpoint exists
            if response.status_code in [405, 200]:
                print("✅ Backend upload endpoint is accessible")
                return True
            else:
                print(f"❌ Backend upload endpoint test failed: {response.status_code}")
                return False
    except Exception as e:
        print(f"❌ Backend upload endpoint test failed: {e}")
        return False

async def main():
    """Run all tests"""
    print("🔍 Testing Synapse Meeting Assistant Integration...")
    print("=" * 50)
    
    tests = [
        ("Backend Health", test_backend_health),
        ("Ollama Connection", test_ollama_connection),
        ("Ollama Model", test_ollama_model),
        ("Backend Upload Endpoint", test_backend_upload_endpoint),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🧪 Testing {test_name}...")
        result = await test_func()
        results.append((test_name, result))
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    print("=" * 50)
    
    all_passed = True
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All tests passed! System is ready for use.")
        print("\n📝 Next steps:")
        print("1. Open http://localhost:3001 in your browser")
        print("2. Upload an MP3 or MP4 file")
        print("3. Wait for processing to complete")
        print("4. View the transcript and analysis results")
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    asyncio.run(main()) 