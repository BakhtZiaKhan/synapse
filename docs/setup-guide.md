# Synapse Setup Guide

This guide will help you set up all the missing components for your Synapse meeting assistant.

## 1. Environment Files ✅

Environment files have been created:
- `backend/.env` - Backend configuration
- `frontend/.env.local` - Frontend configuration

## 2. Hugging Face Spaces Setup

### Step 1: Create Whisper Space

1. Go to [Hugging Face Spaces](https://huggingface.co/spaces)
2. Click "Create new Space"
3. Choose "Gradio" as the SDK
4. Name it something like `synapse-whisper`
5. Set visibility to "Public" or "Private"

### Step 2: Configure Whisper Space

Create `app.py` in your Whisper Space:

```python
import gradio as gr
from transformers import WhisperProcessor, WhisperForConditionalGeneration
import torch
import librosa
import numpy as np

# Load model
model_name = "openai/whisper-base"
processor = WhisperProcessor.from_pretrained(model_name)
model = WhisperForConditionalGeneration.from_pretrained(model_name)

def transcribe_audio(audio):
    if audio is None:
        return "No audio provided"
    
    # Load and preprocess audio
    audio_array, sample_rate = librosa.load(audio, sr=16000)
    
    # Process with Whisper
    input_features = processor(audio_array, sampling_rate=sample_rate, return_tensors="pt").input_features
    
    # Generate token ids
    predicted_ids = model.generate(input_features)
    
    # Decode
    transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]
    
    return transcription

# Create Gradio interface
iface = gr.Interface(
    fn=transcribe_audio,
    inputs=gr.Audio(type="filepath"),
    outputs=gr.Textbox(label="Transcription"),
    title="Synapse Whisper Transcription",
    description="Upload an audio file to get transcription"
)

iface.launch()
```

### Step 3: Create LLM Space

1. Create another Space named `synapse-llm`
2. Use "Gradio" SDK
3. Create `app.py`:

```python
import gradio as gr
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import json

# Load model (choose one)
model_name = "microsoft/DialoGPT-medium"  # or "microsoft/DialoGPT-large"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

def analyze_transcript(transcript, output_format="json", temperature=0.7, max_tokens=512):
    prompt = f"""You are an expert meeting assistant. Analyze the following meeting transcript and provide a structured analysis.

Meeting Transcript:
{transcript}

Your response must be a single, valid JSON object with these exact keys:
- "summary": A 3-sentence overview of the meeting
- "action_items": A list of strings, where each string is a specific task assigned to someone
- "key_decisions": A list of strings describing any decisions made during the meeting

Focus on:
1. Clear, actionable items with assignees when possible
2. Important decisions and their implications
3. Key topics discussed and outcomes

Return only the JSON object, no additional text:"""

    # Generate response
    inputs = tokenizer.encode(prompt, return_tensors="pt", max_length=1024, truncation=True)
    
    with torch.no_grad():
        outputs = model.generate(
            inputs,
            max_length=max_tokens,
            temperature=temperature,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )
    
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Extract the generated part (after the prompt)
    generated_text = response[len(prompt):].strip()
    
    try:
        # Try to parse as JSON
        analysis = json.loads(generated_text)
        return json.dumps(analysis, indent=2)
    except:
        # Fallback
        return json.dumps({
            "summary": "Analysis completed",
            "action_items": [],
            "key_decisions": []
        }, indent=2)

# Create Gradio interface
iface = gr.Interface(
    fn=analyze_transcript,
    inputs=[
        gr.Textbox(label="Meeting Transcript", lines=10),
        gr.Dropdown(choices=["json"], value="json", label="Output Format"),
        gr.Slider(minimum=0.1, maximum=1.0, value=0.7, label="Temperature"),
        gr.Slider(minimum=100, maximum=1000, value=512, label="Max Tokens")
    ],
    outputs=gr.Textbox(label="Analysis Result", lines=10),
    title="Synapse Meeting Analysis",
    description="Analyze meeting transcripts for summary, action items, and key decisions"
)

iface.launch()
```

### Step 4: Get Space URLs

1. After deploying both spaces, get their URLs:
   - Whisper: `https://your-username-synapse-whisper.hf.space`
   - LLM: `https://your-username-synapse-llm.hf.space`

2. Update `backend/.env`:
```bash
WHISPER_API_URL=https://your-username-synapse-whisper.hf.space
LLM_API_URL=https://your-username-synapse-llm.hf.space
```

## 3. Supabase Database Setup

### Step 1: Create Supabase Project

1. Go to [Supabase](https://supabase.com)
2. Create a new project
3. Note your project URL and anon key

### Step 2: Create Database Table

In your Supabase SQL editor, run:

```sql
-- Create meetings table
CREATE TABLE meetings (
    id UUID PRIMARY KEY,
    title TEXT NOT NULL,
    filename TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending',
    transcript TEXT,
    summary TEXT,
    action_items JSONB DEFAULT '[]',
    key_decisions JSONB DEFAULT '[]',
    error_message TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX idx_meetings_created_at ON meetings(created_at DESC);
CREATE INDEX idx_meetings_status ON meetings(status);

-- Enable Row Level Security (optional)
ALTER TABLE meetings ENABLE ROW LEVEL SECURITY;
```

### Step 3: Update Environment Variables

Update `backend/.env` with your Supabase credentials:

```bash
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_ANON_KEY=your_supabase_anon_key_here
```

## 4. Testing Your Setup

### Step 1: Start Backend Server

```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Step 2: Test API Endpoints

1. Health check: `GET http://localhost:8000/`
2. Upload file: `POST http://localhost:8000/api/process-meeting`
3. Check status: `GET http://localhost:8000/api/meeting-status/{job_id}`

### Step 3: Start Frontend

```bash
cd frontend
npm run dev
```

## 5. Troubleshooting

### Common Issues:

1. **CORS Errors**: Backend CORS is configured to allow all origins for development
2. **File Upload Issues**: Check file size limits and supported formats
3. **AI Model Errors**: Verify Hugging Face Space URLs and API keys
4. **Database Errors**: Check Supabase credentials and table structure

### Environment Variables Checklist:

- [ ] `WHISPER_API_URL` - Your Whisper Hugging Face Space URL
- [ ] `LLM_API_URL` - Your LLM Hugging Face Space URL
- [ ] `SUPABASE_URL` - Your Supabase project URL
- [ ] `SUPABASE_ANON_KEY` - Your Supabase anon key
- [ ] `NEXT_PUBLIC_API_URL` - Backend API URL (usually http://localhost:8000)

## 6. Next Steps

1. Test with a small audio file
2. Monitor logs for any errors
3. Adjust AI model parameters as needed
4. Deploy to production when ready

Need help with any specific step? Let me know! 