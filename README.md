
# Synapse - Open-Source Meeting Assistant

An intelligent web application that processes audio recordings of meetings to generate transcripts, summaries, action items, and key decisions using entirely free, open-source tools.

##  Core Features

- **Audio Processing**: Upload meeting recordings (Zoom, Teams, etc.)
- **Speech-to-Text**: Convert audio to transcript using OpenAI's Whisper
- **AI Analysis**: Generate meeting summaries, action items, and key decisions
- **Free & Open Source**: Built entirely with free tools and open-source models

## Architecture

### Backend & AI Pipeline (Python)
- **Hugging Face Spaces**: Host Whisper and LLM models as API endpoints
- **FastAPI Backend**: Process audio files and coordinate AI services
- **Render/Railway**: Free hosting for the backend server

### Frontend (React/Next.js)
- **Modern UI**: Clean, intuitive interface for file uploads and results
- **Vercel/Netlify**: Free hosting for the web application

## Tech Stack

### AI Models
- **Speech-to-Text**: OpenAI Whisper (open-source)
- **Language Model**: Mistral 7B or Llama 3 8B 

### Backend
- **Framework**: FastAPI (Python)

### Frontend
- **Framework**: Next.js/React











