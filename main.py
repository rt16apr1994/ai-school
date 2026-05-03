import os
import httpx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS configuration to allow your GitHub site to talk to Render
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY")

@app.get("/generate")
async def generate_content(topic: str, lang: str):
    if not OPENROUTER_KEY:
        return {"error": "API_KEY_MISSING"}

    headers = {
        "Authorization": f"Bearer {OPENROUTER_KEY}",
        "HTTP-Referer": "https://github.com/rajeshkumar1994", # Mandatory for OpenRouter
        "Content-Type": "application/json"
    }

    # Stable Model ID update
    payload = {
        "model": "meta-llama/llama-3.2-1b-instruct:free",
        "messages": [
            {
                "role": "user",
                "content": f"Create a 3-scene learning path for {topic} in {lang}. Output ONLY JSON: " + '{"scenes": [{"visual_prompt": "description", "narration_text": "text"}]}'
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
            return response.json()
        except Exception as e:
            return {"error": str(e)}
