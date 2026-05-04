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

# OpenRouter ke current active free models (updated slugs)
MODELS_TO_TRY = [
    "meta-llama/llama-3.2-1b-instruct", # Removed :free as OpenRouter auto-routes
    "meta-llama/llama-3.1-8b-instruct",
    "mistralai/mistral-7b-instruct-v0.1",
    "google/gemini-flash-1.5-8b"
]

@app.get("/generate")
async def generate_content(topic: str, lang: str):
    if not OPENROUTER_KEY:
        return {"error": "KEY_NOT_FOUND"}
    
    print(f"DEBUG: Attempting request for {topic} with key ending in ...{OPENROUTER_KEY[-4:]}")    
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_KEY}",
        "HTTP-Referer": "https://rt16apr1994.github.io", 
        "X-Title": "AI School App",
        "Content-Type": "application/json"
    }

    prompt = (
        f"Create a 3-scene learning path for {topic} in {lang}. "
        "Output ONLY a JSON object: "
        '{"scenes": [{"visual_prompt": "detailed description", "narration_text": "explanation"}]}'
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
                        "messages": [{"role": "user", "content": prompt}],
                        # 'response_format' ko hataya kyunki kuch free models ise support nahi karte
                    },
                    timeout=35.0
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

        return {"error": "ALL_MODELS_FAILED", "message": "Model IDs not found. Please check OpenRouter documentation."}
