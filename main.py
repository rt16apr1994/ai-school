from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY")

@app.get("/generate")
async def generate_learning_content(topic: str, lang: str):
    # OpenRouter free models ke liye Referer header mandatory hota hai
    headers = {
        "Authorization": f"Bearer {OPENROUTER_KEY}",
        "HTTP-Referer": "https://github.com/rajeshkumar1994", # Aapka GitHub profile link
        "X-Title": "AI School App",
        "Content-Type": "application/json"
    }
    
    # Prompt ko force karein ki wo strictly JSON bhejey
    prompt = (
        f"Create a 3-scene learning path for {topic} in {lang}. "
        "Return ONLY a JSON object. Format: "
        '{"scenes": [{"visual_prompt": "description", "narration_text": "text"}]}'
    )
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json={
                    "model": "google/gemini-2.0-flash-exp:free", 
                    "messages": [{"role": "user", "content": prompt}],
                    "response_format": { "type": "json_object" }
                },
                timeout=45.0
            )
            
            res_data = response.json()
            
            # Debugging ke liye Render logs mein print karein
            print(f"OpenRouter Response: {res_data}")
            
            return res_data
            
        except Exception as e:
            return {"error": str(e)}
