from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import os
import tempfile
from typing import Optional
import logging

from empathy_engine import EmpathyEngine
from config import config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=config.API_TITLE,
    description=config.API_DESCRIPTION,
    version=config.API_VERSION
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=config.CORS_METHODS,
    allow_headers=config.CORS_HEADERS,
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize the Empathy Engine
empathy_engine = EmpathyEngine()

class TextInput(BaseModel):
    text: str
    emotion_override: Optional[str] = None
    intensity: Optional[float] = 1.0
    filename: Optional[str] = None

class AudioResponse(BaseModel):
    message: str
    emotion_detected: str
    vocal_parameters: dict
    audio_file_path: str

@app.get("/")
async def root():
    """Serve the main web interface"""
    return FileResponse("static/index.html")

@app.get("/demo")
async def demo():
    """Serve the emotion demo page"""
    return FileResponse("static/demo.html")

@app.get("/api")
async def api_info():
    """API information endpoint"""
    return {
        "message": "Welcome to The Empathy Engine!",
        "description": "AI-powered TTS with emotional voice modulation",
        "endpoints": {
            "POST /synthesize": "Convert text to emotionally modulated speech",
            "GET /emotions": "Get available emotion categories",
            "GET /health": "Health check endpoint"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "empathy-engine"}

@app.get("/emotions")
async def get_emotions():
    """Get available emotion categories and their vocal parameters"""
    return {
        "emotions": empathy_engine.get_available_emotions(),
        "vocal_parameters": {
            "rate": "Speech rate (words per minute)",
            "pitch": "Voice pitch (Hz)",
            "volume": "Voice volume (0.0-1.0)"
        }
    }

@app.post("/synthesize", response_model=AudioResponse)
async def synthesize_speech(input_data: TextInput):
    """
    Convert text to emotionally modulated speech
    
    - **text**: The text to convert to speech
    - **emotion_override**: Optional emotion to force (skips detection)
    - **intensity**: Emotion intensity multiplier (0.1-2.0, default 1.0)
    - **filename**: Optional custom filename (without extension)
    """
    try:
        logger.info(f"Synthesizing speech for text: {input_data.text[:50]}...")
        
        # Generate emotionally modulated speech
        result = empathy_engine.synthesize_with_emotion(
            text=input_data.text,
            emotion_override=input_data.emotion_override,
            intensity=input_data.intensity,
            custom_filename=input_data.filename
        )
        
        return AudioResponse(
            message="Speech synthesized successfully",
            emotion_detected=result["emotion"],
            vocal_parameters=result["vocal_parameters"],
            audio_file_path=result["audio_file"]
        )
        
    except Exception as e:
        logger.error(f"Error synthesizing speech: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Speech synthesis failed: {str(e)}")

@app.get("/audio/{filename}")
async def get_audio_file(filename: str):
    """Serve generated audio files"""
    audio_path = os.path.join("temp_audio", filename)
    if not os.path.exists(audio_path):
        raise HTTPException(status_code=404, detail="Audio file not found")
    
    return FileResponse(
        audio_path,
        media_type="audio/wav",
        filename=filename
    )

if __name__ == "__main__":
    # Create temp audio directory
    os.makedirs(config.TEMP_AUDIO_DIR, exist_ok=True)
    
    uvicorn.run(
        "main:app",
        host=config.HOST,
        port=config.PORT,
        reload=config.DEBUG,
        log_level=config.LOG_LEVEL.lower()
    )
