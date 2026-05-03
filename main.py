from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY")

@app.get("/generate")
async def generate_learning_content(topic: str, lang: str):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_KEY}",
        "HTTP-Referer": "https://github.com",
        "Content-Type": "application/json"
    }
    
    prompt = f"Create a 3-scene learning path for {topic} in {lang}. Return ONLY a JSON object with a 'scenes' array. Each scene has 'visual_prompt' and 'narration_text'."
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json={
                    "model": "google/gemini-2.0-flash-exp:free", # Faster & Stable
                    "messages": [{"role": "user", "content": prompt}]
                },
                timeout=30.0
            )
            return response.json()
        except Exception as e:
            return {"error": str(e)}
