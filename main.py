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

# Priority wise models - Agar pehla busy ho toh dusra try karega
MODELS_TO_TRY = [
    "meta-llama/llama-3.2-1b-instruct:free",
    "meta-llama/llama-3.1-8b-instruct:free",
    "google/gemini-2.0-flash-exp:free",
    "mistralai/mistral-7b-instruct:free"
]

@app.get("/generate")
async def generate_content(topic: str, lang: str):
    if not OPENROUTER_KEY:
        return {"error": "KEY_NOT_FOUND", "details": "Render Environment Variable check karein."}

    headers = {
        "Authorization": f"Bearer {OPENROUTER_KEY}",
        "HTTP-Referer": "https://github.com/rajeshkumar1994", # Mandatory for free tier
        "X-Title": "AI School App",
        "Content-Type": "application/json"
    }

    prompt = (
        f"Create a 3-scene learning path for {topic} in {lang}. "
        "Output ONLY a JSON object: "
        '{"scenes": [{"visual_prompt": "detailed description for image gen", "narration_text": "explanation"}]}'
    )

    async with httpx.AsyncClient() as client:
        for model_id in MODELS_TO_TRY:
            try:
                # Debugging ke liye Render logs mein dikhega
                print(f"Trying model: {model_id}") 
                
                response = await client.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    json={
                        "model": model_id,
                        "messages": [{"role": "user", "content": prompt}],
                        "response_format": {"type": "json_object"}
                    },
                    timeout=35.0
                )
                
                res_data = response.json()
                
                # Success Check
                if "choices" in res_data and len(res_data["choices"]) > 0:
                    print(f"Success with: {model_id}")
                    return res_data
                
                print(f"Failed {model_id}: {res_data.get('error', 'Unknown Error')}")
                continue # Next model par switch karein
                
            except Exception as e:
                print(f"Exception with {model_id}: {str(e)}")
                continue

        return {"error": "ALL_MODELS_FAILED", "message": "Koi bhi free model response nahi de raha. OpenRouter Activity dashboard check karein."}
