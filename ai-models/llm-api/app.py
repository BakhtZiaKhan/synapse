import requests
import re
import json
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalysisRequest(BaseModel):
    data: list

def extract_json(text):
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            return None
    return None

@app.post("/predict")
async def predict(request: AnalysisRequest):
    transcript = request.data[0] if len(request.data) > 0 else ""
    prompt = f"""
You are an expert meeting assistant. Analyze the following meeting transcript and provide a structured analysis.

Meeting Transcript:
{transcript}

Your response must be a single, valid JSON object with these exact keys:
- \"summary\": A 3-sentence overview of the meeting
- \"action_items\": A list of strings, where each string is a specific task assigned to someone
- \"key_decisions\": A list of strings describing any decisions made during the meeting

Respond ONLY with a single valid JSON object, no extra text or explanation.
"""
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "gemma3",  # or your chosen model
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )
        response.raise_for_status()
        result = response.json()
        text = result.get("response", "")
        parsed = extract_json(text)
        if not parsed:
            parsed = {
                "summary": "Could not parse LLM response",
                "action_items": [],
                "key_decisions": [],
                "raw_output": text
            }
        return JSONResponse({
            "data": [json.dumps(parsed)],
            "is_generating": False,
            "duration": 0.0,
            "average_duration": 0.0
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "LLM Analysis API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7861) 