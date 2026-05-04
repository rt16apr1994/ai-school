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

# 1. Models ki list priority wise (Sabse stable pehle)
MODELS_TO_TRY = [
    "meta-llama/llama-3.2-1b-instruct:free",
    "meta-llama/llama-3.1-8b-instruct:free",
    "google/gemini-2.0-flash-exp:free",
    "mistralai/mistral-7b-instruct:free"
]

@app.get("/generate")
async def generate_content(topic: str, lang: str):
    if not OPENROUTER_KEY:
        return {"error": "KEY_NOT_FOUND"}

    headers = {
        "Authorization": f"Bearer {OPENROUTER_KEY}",
        "HTTP-Referer": "https://github.com/rajeshkumar1994",
        "Content-Type": "application/json"
    }

    prompt = f"Create a 3-scene learning path for {topic} in {lang}. Output strictly JSON: " + '{"scenes": [{"visual_prompt": "description", "narration_text": "text"}]}'

    async with httpx.AsyncClient() as client:
        # 2. Loop jo har model ko try karega jab tak success na mile
        for model_id in MODELS_TO_TRY:
            try:
                print(f"Trying model: {model_id}") # Render logs mein dikhega
                
                response = await client.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    json={
                        "model": model_id,
                        "messages": [{"role": "user", "content": prompt}],
                        "response_format": {"type": "json_object"}
                    },
                    timeout=30.0
                )
                
                res_data = response.json()
                
                # Agar "choices" mil gayi, toh result return kar do
                if "choices" in res_data and len(res_data["choices"]) > 0:
                    print(f"Success with model: {model_id}")
                    return res_data
                else:
                    print(f"Model {model_id} failed, error: {res_data.get('error')}")
                    continue # Agla model try karein
                    
            except Exception as e:
                print(f"Exception with {model_id}: {str(e)}")
                continue

        # Agar saare models fail ho gaye
        return {"error": "ALL_MODELS_FAILED", "message": "Koi bhi model abhi available nahi hai. Please try again later."}
