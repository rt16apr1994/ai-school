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

# In IDs se 404 error nahi aayega
MODELS_TO_TRY = [
    "meta-llama/llama-3.2-3b-instruct",
    "google/gemini-2.0-flash-001",
    "mistralai/mistral-7b-instruct",
    "google/gemini-flash-1.5-8b"
]

@app.get("/generate")
async def generate_content(topic: str, lang: str):
    if not OPENROUTER_KEY:
        return {"error": "KEY_NOT_FOUND"}
    
    # Aapki key (ending in 9c6e) sahi load ho rahi hai
    print(f"DEBUG: Attempting request for {topic}")    
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_KEY}",
        "HTTP-Referer": "https://rt16apr1994.github.io", 
        "X-Title": "AI School App",
        "Content-Type": "application/json"
    }

    prompt = (
        f"Create a 3-scene learning path for {topic} in {lang}. "
        "Return ONLY a valid JSON object. No intro text. "
        'Structure: {"scenes": [{"visual_prompt": "description", "narration_text": "text"}]}'
    )

    async with httpx.AsyncClient() as client:
        for model_id in MODELS_TO_TRY:
            try:
                print(f"Trying model: {model_id}") 
                
                response = await client.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    json={
                        "model": model_id,
                        "messages": [{"role": "user", "content": prompt}]
                    },
                    timeout=40.0
                )
                
                res_data = response.json()
                
                if "choices" in res_data and len(res_data["choices"]) > 0:
                    print(f"Success with: {model_id}")
                    return res_data
                
                print(f"Failed {model_id}: {res_data}")
                continue 
                
            except Exception as e:
                print(f"Exception with {model_id}: {str(e)}")
                continue

        return {"error": "ALL_MODELS_FAILED", "message": "Check OpenRouter dashboard for credit status."}
