from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import httpx
import os
import json
import re

router = APIRouter(prefix="/api/v1/profile", tags=["profile"])

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "ollama")
OLLAMA_PORT = os.getenv("OLLAMA_PORT", "11434")
OLLAMA_URL = f"http://{OLLAMA_HOST}:{OLLAMA_PORT}"

# Log configuration for debugging
import logging
logger = logging.getLogger(__name__)


class ProfileRequest(BaseModel):
    name: str
    age: int
    profession: str
    interests: list[str]
    education: str = ""
    location: str = ""
    bio: str = ""


class ArticleResponse(BaseModel):
    article: str
    topics: list[dict]


def extract_links_from_text(text: str) -> list[dict]:
    """Extract topics and potential links from the generated article"""
    topics = []
    
    # Look for markdown-style links [text](url)
    markdown_links = re.findall(r'\[([^\]]+)\]\(([^\)]+)\)', text)
    for link_text, url in markdown_links:
        topics.append({
            "title": link_text,
            "url": url,
            "type": "external"
        })
    
    # If no markdown links, extract key topics/phrases
    if not topics:
        # Look for capitalized phrases that might be topics
        potential_topics = re.findall(r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b', text)
        for topic in set(potential_topics[:5]):  # Limit to 5 unique topics
            if len(topic) > 3:  # Filter out short words
                topics.append({
                    "title": topic,
                    "url": f"https://www.google.com/search?q={topic.replace(' ', '+')}",
                    "type": "search"
                })
    
    return topics


@router.get("/warmup")
async def warmup_model():
    """Pre-load the Mistral model into memory to speed up first request"""
    try:
        print("Warming up Mistral model...")
        async with httpx.AsyncClient(timeout=180.0) as client:
            response = await client.post(
                f"{OLLAMA_URL}/api/generate",
                json={
                    "model": "mistral",
                    "prompt": "Hello",
                    "stream": False,
                    "options": {"num_predict": 10}
                }
            )
            if response.status_code == 200:
                return {"status": "success", "message": "Model warmed up and ready"}
            else:
                return {"status": "error", "message": f"Failed to warm up model: {response.text[:200]}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@router.post("/analyze", response_model=ArticleResponse)
async def analyze_profile(profile: ProfileRequest):
    """Analyze user profile and generate personalized article with topic links"""
    try:
        print(f"Received profile analysis request for: {profile.name}")
        print(f"Ollama URL: {OLLAMA_URL}")
        
        # Build a concise prompt for faster generation
        interests_str = ", ".join(profile.interests)
        prompt = f"""Write a personalized 200-word article for {profile.name}, a {profile.age}-year-old {profile.profession}. 

Profile: {profile.education or 'Education not specified'}, {profile.location or 'Location not specified'}. Interests: {interests_str}. {profile.bio or ''}

Include 3-5 topics with markdown links: [Topic Name](https://example.com/topic). Keep it engaging and professional."""

        # Call Ollama API
        # Reduced num_predict for faster generation while still getting good results
        ollama_data = {
            "model": "mistral",
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.8,
                "top_p": 0.9,
                "num_predict": 400  # Reduced from 500 for faster generation
            }
        }
        
        print(f"Calling Ollama at {OLLAMA_URL}/api/generate")
        
        # Use a longer timeout for model generation (5 minutes)
        # First request can take time to load the model into memory
        async with httpx.AsyncClient(timeout=300.0) as client:
            try:
                response = await client.post(
                    f"{OLLAMA_URL}/api/generate",
                    json=ollama_data
                )
                
                print(f"Ollama response status: {response.status_code}")
                
                if response.status_code == 200:
                    result = response.json()
                    article_text = result.get("response", "")
                    
                    if not article_text:
                        raise HTTPException(
                            status_code=500,
                            detail="Ollama returned empty response. Make sure the 'mistral' model is installed: docker exec ollama-mistral ollama pull mistral"
                        )
                    
                    # Extract topics and links from the article
                    topics = extract_links_from_text(article_text)
                    
                    print(f"Successfully generated article with {len(topics)} topics")
                    
                    return ArticleResponse(
                        article=article_text,
                        topics=topics
                    )
                else:
                    error_text = response.text[:500] if hasattr(response, 'text') else "Unknown error"
                    print(f"Ollama error: {error_text}")
                    raise HTTPException(
                        status_code=response.status_code,
                        detail=f"Ollama API error (status {response.status_code}): {error_text}"
                    )
            except httpx.ConnectError as e:
                print(f"Connection error to Ollama: {str(e)}")
                raise HTTPException(
                    status_code=503,
                    detail=f"Cannot connect to Ollama at {OLLAMA_URL}. Please ensure Ollama is running and the 'mistral' model is installed. Run: docker exec ollama-mistral ollama pull mistral"
                )
            except httpx.TimeoutException:
                print("Ollama request timeout")
                raise HTTPException(
                    status_code=504,
                    detail="Request timeout - The model is taking too long to respond. This can happen on the first request as the model loads into memory (can take 1-2 minutes). Please wait a moment and try again. Subsequent requests should be faster."
                )
                
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )
