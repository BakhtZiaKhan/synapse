import whisper
import tempfile
import os
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# Load the Whisper model
model = whisper.load_model("base")

app = FastAPI(title="Whisper API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        audio_data = await file.read()
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            tmp_file.write(audio_data)
            tmp_file_path = tmp_file.name
        result = model.transcribe(tmp_file_path)
        os.unlink(tmp_file_path)
        return JSONResponse({
            "data": [result["text"]],
            "is_generating": False,
            "duration": 0.0,
            "average_duration": 0.0
        })
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/")
async def root():
    return {"message": "Whisper API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860) 