#!/usr/bin/env python3
"""
Startup script for The Empathy Engine
Handles environment setup and server startup
"""

import os
import sys
import subprocess
import logging
from pathlib import Path

def check_dependencies():
    """Check if all required dependencies are installed"""
    try:
        import fastapi
        import uvicorn
        import textblob
        import vaderSentiment
        import transformers
        import pyttsx3
        import gtts
        import pydub
        import numpy
        import scipy
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please install dependencies with: pip install -r requirements.txt")
        return False

def setup_environment():
    """Set up the environment for the application"""
    
    # Create necessary directories
    os.makedirs("temp_audio", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/empathy_engine.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    print("✅ Environment setup complete")

def main():
    """Main startup function"""
    
    print("🎙️ The Empathy Engine - Starting Up")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("main.py"):
        print("❌ Please run this script from the project root directory")
        print("   (The directory containing main.py)")
        sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Setup environment
    setup_environment()
    
    print("\n🚀 Starting The Empathy Engine server...")
    print("📍 Server will be available at: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🔍 Health Check: http://localhost:8000/health")
    print("\nPress Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        # Start the server
        subprocess.run([
            sys.executable, "main.py"
        ], check=True)
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Server failed to start: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

