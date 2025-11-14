#!/usr/bin/env python3
"""Quick script to check if Ollama is accessible and Mistral model is available"""
import httpx
import os
import sys

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "ollama")
OLLAMA_PORT = os.getenv("OLLAMA_PORT", "11434")
OLLAMA_URL = f"http://{OLLAMA_HOST}:{OLLAMA_PORT}"

async def check_ollama():
    print(f"Checking Ollama at: {OLLAMA_URL}")
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            # Check if Ollama is running
            print("1. Checking if Ollama is running...")
            try:
                response = await client.get(f"{OLLAMA_URL}/api/tags")
                if response.status_code == 200:
                    print("   ✓ Ollama is running")
                else:
                    print(f"   ✗ Ollama returned status {response.status_code}")
                    return False
            except httpx.ConnectError:
                print(f"   ✗ Cannot connect to Ollama at {OLLAMA_URL}")
                print(f"   Make sure Ollama container is running: docker ps")
                return False
            
            # Check available models
            print("2. Checking available models...")
            models_data = response.json()
            models = models_data.get("models", [])
            
            if not models:
                print("   ✗ No models found. Pull mistral model:")
                print("   docker exec ollama-mistral ollama pull mistral")
                return False
            
            print(f"   ✓ Found {len(models)} model(s):")
            for model in models:
                name = model.get("name", "unknown")
                print(f"     - {name}")
            
            # Check if mistral is available
            has_mistral = any("mistral" in model.get("name", "").lower() for model in models)
            if not has_mistral:
                print("   ✗ Mistral model not found. Pull it with:")
                print("   docker exec ollama-mistral ollama pull mistral")
                return False
            
            print("   ✓ Mistral model is available")
            
            # Test a simple generation
            print("3. Testing model generation...")
            test_response = await client.post(
                f"{OLLAMA_URL}/api/generate",
                json={
                    "model": "mistral",
                    "prompt": "Say hello",
                    "stream": False
                },
                timeout=30.0
            )
            
            if test_response.status_code == 200:
                print("   ✓ Model generation works")
                return True
            else:
                print(f"   ✗ Generation failed with status {test_response.status_code}")
                print(f"   Response: {test_response.text[:200]}")
                return False
                
    except Exception as e:
        print(f"   ✗ Error: {str(e)}")
        return False

if __name__ == "__main__":
    import asyncio
    success = asyncio.run(check_ollama())
    sys.exit(0 if success else 1)

