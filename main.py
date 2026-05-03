from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os

app = FastAPI()

# Ye section GitHub Pages se aane wali requests ko allow karega
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For testing, allows all. Later you can put your github link.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY")

@app.get("/generate")
async def generate_learning_content(topic: str, lang: str):
    prompt = f"Create a 3-scene video script for learning {topic} in {lang}. For each scene, provide a 'visual_prompt' for an image generator and 'narration_text'."
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {OPENROUTER_KEY}"},
            json={
                "model": "meta-llama/llama-3.3-70b-instruct:free",
                "messages": [{"role": "user", "content": prompt}],
                "response_format": { "type": "json_object" } # Requesting JSON
            }
        )
    return response.json()
