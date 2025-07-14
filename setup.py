#!/usr/bin/env python3
"""
Synapse Setup Script
This script helps you set up the Synapse meeting assistant project.
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def print_banner():
    """Print the project banner"""
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                    🧠 SYNAPSE SETUP                          ║
    ║                                                              ║
    ║  Open-Source Meeting Assistant                               ║
    ║  Built with FastAPI, Next.js, and AI Models                 ║
    ╚══════════════════════════════════════════════════════════════╝
    """)

def check_prerequisites():
    """Check if required tools are installed"""
    print("🔍 Checking prerequisites...")
    
    # Check Python
    try:
        python_version = subprocess.check_output([sys.executable, "--version"], text=True)
        print(f"✅ Python: {python_version.strip()}")
    except:
        print("❌ Python not found. Please install Python 3.8+")
        return False
    
    # Check Node.js
    try:
        node_version = subprocess.check_output(["node", "--version"], text=True)
        print(f"✅ Node.js: {node_version.strip()}")
    except:
        print("❌ Node.js not found. Please install Node.js 16+")
        return False
    
    # Check npm (npm comes with Node.js, so if Node.js is installed, npm should be available)
    try:
        npm_version = subprocess.check_output(["npm", "--version"], text=True)
        print(f"✅ npm: {npm_version.strip()}")
    except:
        # Try alternative npm command or check if it's in PATH
        try:
            npm_version = subprocess.check_output(["npm.cmd", "--version"], text=True)
            print(f"✅ npm: {npm_version.strip()}")
        except:
            print("⚠️  npm not found in PATH, but Node.js is installed. npm should be available.")
            print("   If you encounter issues, try reinstalling Node.js or adding npm to PATH.")
            # Continue anyway since npm usually comes with Node.js
    
    return True

def setup_backend():
    """Set up the backend environment"""
    print("\n🐍 Setting up Python backend...")
    
    backend_dir = Path("backend")
    if not backend_dir.exists():
        print("❌ Backend directory not found")
        return False
    
    # Create virtual environment
    try:
        subprocess.run([sys.executable, "-m", "venv", "backend/venv"], check=True)
        print("✅ Virtual environment created")
    except subprocess.CalledProcessError:
        print("❌ Failed to create virtual environment")
        return False
    
    # Install dependencies
    pip_cmd = "backend/venv/bin/pip" if os.name != "nt" else "backend\\venv\\Scripts\\pip"
    try:
        subprocess.run([pip_cmd, "install", "-r", "backend/requirements.txt"], check=True)
        print("✅ Backend dependencies installed")
    except subprocess.CalledProcessError:
        print("❌ Failed to install backend dependencies")
        return False
    
    return True

def setup_frontend():
    """Set up the frontend environment"""
    print("\n⚛️  Setting up Next.js frontend...")
    
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print("❌ Frontend directory not found")
        return False
    
    # Install dependencies
    try:
        subprocess.run(["npm", "install"], cwd=frontend_dir, check=True)
        print("✅ Frontend dependencies installed")
    except subprocess.CalledProcessError:
        # Try with npm.cmd for Windows
        try:
            subprocess.run(["npm.cmd", "install"], cwd=frontend_dir, check=True)
            print("✅ Frontend dependencies installed")
        except subprocess.CalledProcessError:
            print("❌ Failed to install frontend dependencies")
            print("   Try running 'npm install' manually in the frontend directory")
            return False
    
    return True

def create_env_files():
    """Create example environment files"""
    print("\n📝 Creating environment files...")
    
    # Backend .env
    backend_env = """# Synapse Backend Environment Variables

# AI Model URLs (Update these after deploying to Hugging Face Spaces)
WHISPER_API_URL=https://your-whisper-space.hf.space
LLM_API_URL=https://your-llm-space.hf.space

# Database (Optional - Update with your Supabase credentials)
SUPABASE_URL=your-supabase-url
SUPABASE_ANON_KEY=your-supabase-anon-key

# Optional API Keys
WHISPER_API_KEY=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
LLM_API_KEY=your-llm-api-key
"""
    
    with open("backend/.env.example", "w") as f:
        f.write(backend_env)
    print("✅ Backend .env.example created")
    
    # Frontend .env.local
    frontend_env = """# Synapse Frontend Environment Variables

# Backend API URL (Update after deploying backend)
NEXT_PUBLIC_API_URL=http://localhost:8000
"""
    
    with open("frontend/.env.local.example", "w") as f:
        f.write(frontend_env)
    print("✅ Frontend .env.local.example created")

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")
    
    directories = [
        "backend/uploads",
        "backend/logs",
        "docs",
        "ai-models/whisper-api",
        "ai-models/llm-api"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created {directory}")

def print_next_steps():
    """Print next steps for the user"""
    print("""
    🎉 Setup complete! Here are your next steps:
    
    1. 📚 Read the documentation:
       - README.md - Project overview
       - docs/deployment.md - Deployment guide
    
    2. 🚀 Deploy AI Models to Hugging Face Spaces:
       - Upload ai-models/whisper-api/ to a new Hugging Face Space
       - Upload ai-models/llm-api/ to another Hugging Face Space
       - Note the URLs for environment variables
    
    3. 🗄️  Set up database (optional):
       - Create a Supabase project
       - Run the SQL commands from docs/deployment.md
    
    4. 🌐 Deploy to free hosting:
       - Backend: Deploy to Render
       - Frontend: Deploy to Vercel
    
    5. 🔧 Configure environment variables:
       - Copy .env.example to .env in backend/
       - Copy .env.local.example to .env.local in frontend/
       - Update with your actual URLs and keys
    
    6. 🧪 Test locally:
       - Backend: cd backend && python -m uvicorn app.main:app --reload
       - Frontend: cd frontend && npm run dev
    
    📖 For detailed instructions, see docs/deployment.md
    """)

def main():
    """Main setup function"""
    print_banner()
    
    if not check_prerequisites():
        print("\n❌ Prerequisites not met. Please install required tools.")
        sys.exit(1)
    
    create_directories()
    
    if not setup_backend():
        print("\n❌ Backend setup failed.")
        sys.exit(1)
    
    if not setup_frontend():
        print("\n❌ Frontend setup failed.")
        sys.exit(1)
    
    create_env_files()
    print_next_steps()

if __name__ == "__main__":
    main() 