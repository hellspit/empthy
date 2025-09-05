#!/usr/bin/env python3
"""
Installation script for The Empathy Engine
Handles dependency installation and environment setup
"""

import subprocess
import sys
import os
import platform

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    
    try:
        # Upgrade pip first
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], check=True)
        
        # Install requirements
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        
        print("✅ Dependencies installed successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def setup_directories():
    """Create necessary directories"""
    print("\n📁 Setting up directories...")
    
    directories = [
        "temp_audio",
        "logs"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created directory: {directory}")

def test_installation():
    """Test if the installation works"""
    print("\n🧪 Testing installation...")
    
    try:
        # Test imports
        import fastapi
        import uvicorn
        import textblob
        import vaderSentiment
        import pyttsx3
        import pydub
        import numpy
        import scipy
        
        print("✅ All core dependencies imported successfully")
        
        # Test TTS engine
        import pyttsx3
        engine = pyttsx3.init()
        engine.stop()
        print("✅ TTS engine initialized successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import test failed: {e}")
        return False
    except Exception as e:
        print(f"❌ TTS engine test failed: {e}")
        return False

def print_next_steps():
    """Print next steps for the user"""
    print("\n🎉 Installation completed successfully!")
    print("\nNext steps:")
    print("1. Start the server: python run.py")
    print("2. Or start manually: python main.py")
    print("3. Visit http://localhost:8000/docs for API documentation")
    print("4. Run the demo: python demo.py")
    print("5. Run tests: python test_empathy_engine.py")
    print("\n📚 Documentation:")
    print("- README.md: Complete setup and usage guide")
    print("- API docs: http://localhost:8000/docs (when server is running)")

def main():
    """Main installation function"""
    print("🎙️ The Empathy Engine - Installation Script")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Installation failed. Please check the error messages above.")
        sys.exit(1)
    
    # Setup directories
    setup_directories()
    
    # Test installation
    if not test_installation():
        print("\n⚠️  Installation completed but some tests failed.")
        print("The application may still work, but some features might not be available.")
    
    # Print next steps
    print_next_steps()

if __name__ == "__main__":
    main()
