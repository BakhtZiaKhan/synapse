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
