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
