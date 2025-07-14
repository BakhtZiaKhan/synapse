<<<<<<< HEAD
# Synapse - Open-Source Meeting Assistant

An intelligent web application that processes audio recordings of meetings to generate transcripts, summaries, action items, and key decisions using entirely free, open-source tools.

## 🎯 Core Features

- **Audio Processing**: Upload meeting recordings (Zoom, Teams, etc.)
- **Speech-to-Text**: Convert audio to transcript using OpenAI's Whisper
- **AI Analysis**: Generate meeting summaries, action items, and key decisions
- **Free & Open Source**: Built entirely with free tools and open-source models

## 🏗️ Architecture

### Backend & AI Pipeline (Python)
- **Hugging Face Spaces**: Host Whisper and LLM models as API endpoints
- **FastAPI Backend**: Process audio files and coordinate AI services
- **Render/Railway**: Free hosting for the backend server
- **Supabase**: Free PostgreSQL database for storing results

### Frontend (React/Next.js)
- **Modern UI**: Clean, intuitive interface for file uploads and results
- **Vercel/Netlify**: Free hosting for the web application

## 🛠️ Tech Stack

### AI Models
- **Speech-to-Text**: OpenAI Whisper (open-source)
- **Language Model**: Mistral 7B or Llama 3 8B (quantized)
- **Hosting**: Hugging Face Spaces (free tier)

### Backend
- **Framework**: FastAPI (Python)
- **Hosting**: Render/Railway (free tier)
- **Database**: Supabase (free tier)

### Frontend
- **Framework**: Next.js/React
- **Hosting**: Vercel (free tier)
- **Styling**: Tailwind CSS

## 📁 Project Structure

```
synapse/
├── backend/                 # FastAPI backend server
│   ├── app/
│   │   ├── main.py         # FastAPI application
│   │   ├── models.py       # Data models
│   │   ├── services/       # AI service integrations
│   │   └── utils/          # Utility functions
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile         # Container configuration
├── frontend/               # Next.js frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/         # Next.js pages
│   │   └── styles/        # CSS/Tailwind styles
│   ├── package.json       # Node.js dependencies
│   └── next.config.js     # Next.js configuration
├── ai-models/             # Hugging Face Spaces configurations
│   ├── whisper-api/       # Whisper model deployment
│   └── llm-api/          # LLM model deployment
└── docs/                  # Documentation
    ├── api.md            # API documentation
    └── deployment.md     # Deployment guides
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Node.js 16+
- Git

### Quick Start
1. Clone this repository
2. Set up the backend (see `backend/README.md`)
3. Set up the frontend (see `frontend/README.md`)
4. Deploy AI models to Hugging Face Spaces
5. Configure environment variables
6. Deploy to free hosting platforms

## 📋 Development Roadmap

### Week 1: AI Model Deployment
- [ ] Deploy Whisper model to Hugging Face Spaces
- [ ] Deploy LLM model to Hugging Face Spaces
- [ ] Test API endpoints

### Week 2: Backend Development
- [ ] Set up FastAPI backend
- [ ] Implement audio processing pipeline
- [ ] Integrate with AI models
- [ ] Add database integration

### Week 3: Frontend Development
- [ ] Create modern UI components
- [ ] Implement file upload functionality
- [ ] Display results in organized format
- [ ] Add responsive design

### Week 4: Integration & Deployment
- [ ] Connect frontend and backend
- [ ] Deploy to free hosting platforms
- [ ] Add error handling and validation
- [ ] Performance optimization

## 🤝 Contributing

This project is designed for collaborative development. Each team member can focus on their strengths:
- **Backend/AI Engineer**: Focus on the AI pipeline and server logic
- **Frontend Engineer**: Focus on user experience and interface design

## 📄 License

This project is open source and available under the MIT License. 
=======
# synapse
>>>>>>> a199808e6fb1831e12d60b3e43eb474dbc679965
