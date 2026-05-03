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

headers = {
    "Authorization": f"Bearer {OPENROUTER_KEY}",
    "HTTP-Referer": "https://github.com", # Ye line mandatory hai
    "X-Title": "Personalized Learning App",
    "Content-Type": "application/json"
}

@app.get("/generate")
async def generate_learning_content(topic: str, lang: str):
    prompt = f"Create a 3-scene video script for learning {topic} in {lang}. For each scene, provide a 'visual_prompt' for an image generator and 'narration_text'."
    
    async with httpx.AsyncClient() as client:
       response = await client.post(
    "[https://openrouter.ai/api/v1/chat/completions](https://openrouter.ai/api/v1/chat/completions)",
    headers={"Authorization": f"Bearer {OPENROUTER_KEY}"},
    json={
        "model": "google/gemini-2.0-flash-exp:free",
        "messages": [{
            "role": "user", 
            "content": f"Create a 3-scene learning path for {topic} in {lang}. Output ONLY a JSON object with a 'scenes' array containing 'visual_prompt' and 'narration_text' fields."
        }],
        "response_format": { "type": "json_object" } # Ye line important hai
    }
)
    return response.json()
