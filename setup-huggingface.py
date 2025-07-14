#!/usr/bin/env python3
"""
Hugging Face Spaces Setup Script for Synapse
This script creates the necessary files for your Hugging Face Spaces.
"""

import os

def create_whisper_space_files():
    """Create files for the Whisper Space"""
    
    whisper_app_py = '''import gradio as gr
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
'''
    
    whisper_requirements = '''gradio>=4.0.0
transformers>=4.30.0
torch>=2.0.0
librosa>=0.10.0
numpy>=1.24.0
'''
    
    return {
        "app.py": whisper_app_py,
        "requirements.txt": whisper_requirements
    }

def create_llm_space_files():
    """Create files for the LLM Space"""
    
    llm_app_py = '''import gradio as gr
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
'''
    
    llm_requirements = '''gradio>=4.0.0
transformers>=4.30.0
torch>=2.0.0
'''
    
    return {
        "app.py": llm_app_py,
        "requirements.txt": llm_requirements
    }

def main():
    print("🚀 Synapse Hugging Face Spaces Setup")
    print("=" * 50)
    
    # Create directories
    os.makedirs("huggingface-spaces/whisper", exist_ok=True)
    os.makedirs("huggingface-spaces/llm", exist_ok=True)
    
    # Create Whisper Space files
    whisper_files = create_whisper_space_files()
    for filename, content in whisper_files.items():
        filepath = os.path.join("huggingface-spaces", "whisper", filename)
        with open(filepath, "w") as f:
            f.write(content)
        print(f"✅ Created: {filepath}")
    
    # Create LLM Space files
    llm_files = create_llm_space_files()
    for filename, content in llm_files.items():
        filepath = os.path.join("huggingface-spaces", "llm", filename)
        with open(filepath, "w") as f:
            f.write(content)
        print(f"✅ Created: {filepath}")
    
    print("\n📋 Next Steps:")
    print("1. Go to https://huggingface.co/spaces")
    print("2. Create two new Spaces:")
    print("   - Name: 'synapse-whisper' (Gradio SDK)")
    print("   - Name: 'synapse-llm' (Gradio SDK)")
    print("3. Upload the files from huggingface-spaces/whisper/ to your whisper space")
    print("4. Upload the files from huggingface-spaces/llm/ to your llm space")
    print("5. Wait for deployment and get the URLs")
    print("6. Update backend/.env with the URLs")
    
    print("\n🔗 Your Space URLs will be:")
    print("- Whisper: https://your-username-synapse-whisper.hf.space")
    print("- LLM: https://your-username-synapse-llm.hf.space")

if __name__ == "__main__":
    main() 