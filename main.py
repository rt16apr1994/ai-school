import os
import httpx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY")

@app.get("/generate")
async def generate_content(topic: str, lang: str):
    # Agar key load nahi hui toh error message bhejien
    if not OPENROUTER_KEY:
        return {"error": "KEY_NOT_FOUND_IN_RENDER"}

    headers = {
        "Authorization": f"Bearer {OPENROUTER_KEY}",
        "HTTP-Referer": "https://github.com/rajeshkumar1994", # Mandatory for OpenRouter free
        "Content-Type": "application/json"
    }

    payload = {
        "model": "meta-llama/llama-3.1-8b-instruct:free", # Change to 3.1 8B (very stable)
        "messages": [
            {
                "role": "user",
                "content": f"Return ONLY a JSON object with 'scenes' array for topic {topic} in {lang}. Each scene has 'visual_prompt' and 'narration_text'."
            }
        ],
        "response_format": {"type": "json_object"}
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=60.0
            )
            # Response ko debug karne ke liye print karein (Render logs mein dikhega)
            print(f"OpenRouter Raw Response: {response.text}")
            return response.json()
        except Exception as e:
            return {"error": "CONNECTION_FAILED", "details": str(e)}
