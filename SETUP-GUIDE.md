# Jarvis Assistant - Setup Guide

## Issues Fixed

1. **Database Creation**: Automatically creates `jarvis.db` on first run
2. **Cross-platform Compatibility**: Fixed Windows-specific paths and commands
3. **API Key Security**: Moved hardcoded API keys to environment variables
4. **Error Handling**: Added proper error handling for missing dependencies
5. **Deployment Ready**: Created deployment-specific requirements file

## Prerequisites

- Python 3.8 or higher
- Git
- Microphone (for voice input)
- Camera (optional, for face authentication)

## Installation Steps

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd <repo-directory>
```

### 2. Create Virtual Environment
```bash
python -m venv envJarvis
```

### 3. Activate Virtual Environment

**Windows:**
```bash
envJarvis\Scripts\activate
```

**Linux/Mac:**
```bash
source envJarvis/bin/activate
```

### 4. Install Dependencies

**For Development (with PyAudio):**
```bash
pip install -r requirements.txt
```

**For Deployment (without PyAudio):**
```bash
pip install -r requirements-deployment.txt
```

### 5. Set Up Environment Variables

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` and add your API keys:
   - `GEMINI_API_KEY`: Get from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - `PORCUPINE_ACCESS_KEY`: Get from [Picovoice Console](https://console.picovoice.ai/)

### 6. Initialize Database

The database will be created automatically on first run. To manually create it:
```bash
python -c "from backend.db import *"
```

## Running the Application

### Local Development
```bash
python app.py
```
Or with hotword detection:
```bash
python run.py
```

### Deployment
The application is configured for deployment on Railway, Render, or other platforms.
Set the `PORT` environment variable if needed (defaults to 8000).

## Troubleshooting

### PyAudio Installation Issues

**Windows:**
```bash
pip install pipwin
pipwin install pyaudio
```

**Linux:**
```bash
sudo apt-get install portaudio19-dev
pip install pyaudio
```

**Mac:**
```bash
brew install portaudio
pip install pyaudio
```

### Microphone Not Found
- Ensure microphone permissions are granted
- Check if microphone is properly connected
- The app will continue without voice input if microphone is unavailable

### Face Authentication Issues
- Ensure camera permissions are granted
- The app will skip face authentication if camera is unavailable

### API Key Issues
- Verify API keys are correctly set in `.env` file
- Ensure `.env` file is in the root directory
- Check API key validity and quotas

## Features

- Voice Commands
- Face Authentication
- Web/App Opening
- YouTube Playback
- WhatsApp Integration
- AI Chatbot (Gemini)
- Hotword Detection

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | Google Gemini API key for chatbot | Yes |
| `PORCUPINE_ACCESS_KEY` | Picovoice API key for hotword detection | Optional |
| `PORT` | Server port (default: 8000) | Optional |
| `RAILWAY_ENVIRONMENT` | Set by Railway for deployment | Auto |
| `RENDER` | Set by Render for deployment | Auto |

## Additional Notes

- The application uses Eel for the web-based UI
- Face recognition models are stored in `backend/auth/`
- Audio files are in `frontend/assets/audio/`
- The database stores system commands, web commands, and contacts

For more information, see the deployment guides in `README-DEPLOYMENT.md` and `DEPLOYMENT-GUIDE.md`.