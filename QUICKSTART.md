# The Empathy Engine - Quick Start Guide 🚀

## Installation & Setup

### Option 1: Automated Installation
```bash
python install.py
```

### Option 2: Manual Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Create directories
mkdir temp_audio logs

# Start the server
python main.py
```

## Quick Test

1. **Start the server:**
   ```bash
   python run.py
   ```

2. **Test the API:**
   ```bash
   # In another terminal
   python demo.py
   ```

3. **Access the API documentation:**
   - Open http://localhost:8000/docs in your browser

## Example Usage

### Using curl:
```bash
curl -X POST "http://localhost:8000/synthesize" \
     -H "Content-Type: application/json" \
     -d '{"text": "This is amazing news!", "intensity": 1.5}'
```

### Using Python:
```python
import requests

response = requests.post("http://localhost:8000/synthesize", json={
    "text": "Welcome to our amazing product!",
    "intensity": 1.2
})

result = response.json()
print(f"Emotion: {result['emotion_detected']}")
print(f"Audio: {result['audio_file_path']}")
```

## Available Emotions

- **joy**: Happy, enthusiastic
- **sadness**: Somber, melancholic  
- **anger**: Intense, forceful
- **fear**: Anxious, nervous
- **surprise**: Excited, astonished
- **disgust**: Contemptuous, dismissive
- **neutral**: Calm, professional

## API Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `GET /emotions` - Available emotions
- `POST /synthesize` - Convert text to speech
- `GET /audio/{filename}` - Download audio files

## Troubleshooting

### Common Issues:

1. **Import errors**: Run `python install.py` to install dependencies
2. **TTS not working**: Check if you have audio drivers installed
3. **Port already in use**: Change the port in `config.py` or kill the process using port 8000

### Getting Help:

- Check the full README.md for detailed documentation
- Visit http://localhost:8000/docs for interactive API documentation
- Run `python test_empathy_engine.py` to test all functionality

---

**The Empathy Engine** - Bringing human emotion to AI voice synthesis 🎙️✨
