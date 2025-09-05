# The Empathy Engine 🎙️

**AI-powered Text-to-Speech with Emotional Voice Modulation**

The Empathy Engine is a complete web application that dynamically modulates vocal characteristics of synthesized speech based on detected emotions in the input text. It features both a REST API backend and a modern web frontend, bridging the gap between text-based sentiment and expressive, human-like audio output.

## 🌟 Features

### Core Functionality
- **Web Interface**: Modern, responsive web UI for easy interaction
- **REST API**: Complete API for programmatic access
- **Text Input Processing**: Accepts text input via web form or API
- **Multi-Method Emotion Detection**: Uses VADER, TextBlob, and Hugging Face transformers
- **Vocal Parameter Modulation**: Adjusts rate, pitch, and volume based on emotions
- **Emotion-to-Voice Mapping**: Clear logic mapping emotions to vocal characteristics
- **Audio Output**: Generates playable WAV files with real-time playback
- **Emotion Demo**: Interactive demo page showcasing all emotions

### Supported Emotions
- **Joy**: Faster speech, higher pitch, enthusiastic tone
- **Sadness**: Slower speech, lower pitch, melancholic tone
- **Anger**: Intense, forceful delivery
- **Fear**: Fast, nervous, higher pitch
- **Surprise**: Excited, astonished delivery
- **Disgust**: Contemptuous, dismissive tone
- **Neutral**: Calm, professional delivery

### Bonus Features
- **Intensity Scaling**: Emotion intensity affects degree of modulation (0.1-2.0x)
- **Granular Emotions**: 7 distinct emotional states beyond basic positive/negative/neutral
- **Confidence Scoring**: Provides confidence levels for emotion detection
- **RESTful API**: Clean, documented API endpoints
- **Audio File Management**: Automatic cleanup of old audio files
- **Real-time Playback**: Instant audio playback in the browser
- **Custom Filenames**: Save audio files with custom names
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Keyboard Shortcuts**: Ctrl+Enter to generate, Escape to clear errors

## 📁 Project Structure

```
empathy-engine/
├── static/                 # Web frontend files
│   ├── index.html         # Main web interface
│   ├── demo.html          # Emotion demo page
│   ├── style.css          # Modern CSS styling
│   └── script.js          # Interactive JavaScript
├── main.py                # FastAPI application
├── empathy_engine.py      # Core emotion detection and TTS logic
├── config.py              # Configuration and settings
├── requirements.txt       # Python dependencies
├── install.py            # Automated installation script
├── demo.py               # CLI demo script
├── temp_audio/           # Generated audio files (auto-created)
├── logs/                 # Application logs (auto-created)
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd empathy-engine
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

4. **Access the application**
   - **Web Interface**: http://localhost:8000/
   - **Emotion Demo**: http://localhost:8000/demo
   - **API Documentation**: http://localhost:8000/docs
   - **Health Check**: http://localhost:8000/health
   - **Available Emotions**: http://localhost:8000/emotions

## 🌐 Web Interface

### Main Interface
The web interface provides an intuitive way to interact with The Empathy Engine:

1. **Text Input**: Enter your text in the textarea
2. **Emotion Selection**: Choose a specific emotion or let it auto-detect
3. **Intensity Control**: Adjust emotion intensity with the slider (0.1x - 2.0x)
4. **Custom Filename**: Optionally specify a custom filename for the audio
5. **Generate Speech**: Click the button or press Ctrl+Enter
6. **Play Audio**: Listen to the generated speech instantly
7. **Download**: Save the audio file to your device

### Emotion Demo Page
Visit `/demo` to experience all emotions with sample text:
- Interactive emotion cards with visual icons
- One-click generation for each emotion
- Normal and intense intensity options
- Side-by-side comparison of different emotional states

## 📖 API Usage

### Synthesize Speech
```bash
curl -X POST "http://localhost:8000/synthesize" \
     -H "Content-Type: application/json" \
     -d '{
       "text": "This is amazing news! I am so excited!",
       "intensity": 1.5,
       "emotion_override": "joy",
       "filename": "my_audio"
     }'
```

### Response Format
```json
{
  "message": "Speech synthesized successfully",
  "emotion_detected": "joy",
  "vocal_parameters": {
    "rate": 1.2,
    "pitch": 1.1,
    "volume": 0.9,
    "description": "Happy, enthusiastic"
  },
  "audio_file_path": "empathy_audio_20231201_143022.wav"
}
```

### Available Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Main web interface |
| GET | `/demo` | Emotion demo page |
| GET | `/api` | API information and available endpoints |
| GET | `/health` | Health check |
| GET | `/emotions` | List available emotions and parameters |
| POST | `/synthesize` | Convert text to emotionally modulated speech |
| GET | `/audio/{filename}` | Download generated audio files |
| GET | `/docs` | Interactive API documentation (Swagger UI) |

## 🧠 How It Works

### Emotion Detection Pipeline

1. **VADER Sentiment Analysis**: Analyzes text for positive/negative sentiment
2. **TextBlob Sentiment**: Provides polarity and subjectivity scores
3. **Hugging Face Transformers**: Uses pre-trained emotion classification model
4. **Weighted Combination**: Combines results with confidence weighting

### Vocal Parameter Mapping

The system maps detected emotions to specific vocal characteristics:

```python
emotion_mappings = {
    "joy": {
        "rate": 1.2,    # 20% faster speech
        "pitch": 1.1,   # 10% higher pitch
        "volume": 0.9,  # Slightly louder
    },
    "sadness": {
        "rate": 0.8,    # 20% slower speech
        "pitch": 0.9,   # 10% lower pitch
        "volume": 0.7,  # Quieter
    },
    # ... more emotions
}
```

### Intensity Scaling

Emotion intensity affects the degree of vocal modulation:
- **Low intensity (0.1-0.5)**: Subtle changes
- **Normal intensity (1.0)**: Standard emotion mapping
- **High intensity (1.5-2.0)**: Exaggerated changes

## 🛠️ Technical Architecture

### Core Components

1. **FastAPI Application** (`main.py`)
   - REST API endpoints
   - Static file serving
   - Request/response handling
   - CORS middleware

2. **Empathy Engine** (`empathy_engine.py`)
   - Emotion detection logic
   - Vocal parameter calculation
   - Audio synthesis and modulation

3. **Web Frontend** (`static/`)
   - `index.html` - Main web interface
   - `demo.html` - Emotion demo page
   - `style.css` - Modern CSS styling
   - `script.js` - Interactive JavaScript

4. **Configuration** (`config.py`)
   - Centralized settings
   - Emotion mappings
   - Vocal parameters

5. **Dependencies** (`requirements.txt`)
   - FastAPI for web framework
   - pyttsx3 for TTS engine
   - pydub for audio processing
   - transformers for emotion classification

### Design Choices

#### Emotion Detection
- **Multi-method approach**: Combines VADER, TextBlob, and Hugging Face for robustness
- **Confidence weighting**: Higher confidence methods get more influence
- **Fallback handling**: Graceful degradation if models fail to load

#### Vocal Modulation
- **Rate**: Speech speed in words per minute
- **Pitch**: Tonal height using semitone shifts
- **Volume**: Amplitude control (0.0-1.0)

#### Audio Processing
- **pyttsx3**: Offline TTS engine for reliability
- **pydub**: Audio manipulation for pitch and speed changes
- **WAV format**: High-quality, uncompressed audio output

#### Frontend Design
- **Responsive Design**: Mobile-first approach with CSS Grid and Flexbox
- **Modern UI**: Glassmorphism effects, smooth animations, and intuitive controls
- **Real-time Feedback**: Loading states, error handling, and success indicators
- **Accessibility**: Keyboard shortcuts, clear labels, and semantic HTML

## 🔧 Configuration

### Environment Variables
```bash
# Optional: Set log level
export LOG_LEVEL=INFO

# Optional: Set audio cleanup interval
export AUDIO_CLEANUP_HOURS=24
```

### Customization

You can customize emotion mappings by modifying the `emotion_mappings` dictionary in `empathy_engine.py`:

```python
self.emotion_mappings = {
    "custom_emotion": {
        "rate": 1.1,
        "pitch": 1.05,
        "volume": 0.85,
        "description": "Custom emotional state"
    }
}
```

## 🧪 Testing

### Web Interface Testing
1. Start the server: `python main.py`
2. Visit http://localhost:8000/ for the main interface
3. Visit http://localhost:8000/demo for the emotion demo
4. Test different emotions, intensities, and text inputs
5. Verify audio playback and download functionality

### API Testing
1. Visit http://localhost:8000/docs for interactive API documentation
2. Use the Swagger UI to test endpoints directly
3. Test different emotions with various text inputs via API calls

### Example Test Cases
```python
# Joy
"Congratulations! This is fantastic news!"

# Sadness  
"I'm really sorry to hear about your loss."

# Anger
"This is completely unacceptable behavior!"

# Fear
"I'm terrified about what might happen next."

# Surprise
"Oh my goodness! I can't believe it!"

# Neutral
"The weather today is partly cloudy."
```

## 📊 Performance Considerations

- **Audio File Cleanup**: Old files are automatically cleaned up after 24 hours
- **Memory Usage**: Hugging Face models are loaded once at startup
- **Response Time**: Typical synthesis takes 2-5 seconds depending on text length
- **Storage**: Audio files are stored temporarily in `temp_audio/` directory

## 🚀 Future Enhancements

- **SSML Support**: Speech Synthesis Markup Language for advanced control
- **Voice Selection**: Multiple voice options for different personas
- **Real-time Streaming**: WebSocket support for live audio streaming
- **Emotion Intensity Learning**: ML-based intensity prediction
- **Multi-language Support**: Emotion detection in multiple languages
- **Voice Cloning**: Custom voice training and synthesis
- **Batch Processing**: Multiple text inputs in a single request
- **Audio Effects**: Additional audio processing options (echo, reverb, etc.)
- **User Accounts**: Save and manage generated audio files
- **API Rate Limiting**: Production-ready rate limiting and authentication

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 🚀 Deployment

### Local Development
```bash
# Start the development server
python main.py

# Or use uvicorn directly
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Production Deployment
```bash
# Install production dependencies
pip install -r requirements.txt

# Run with production settings
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Docker Deployment (Optional)
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Variables
```bash
# Optional configuration
export LOG_LEVEL=INFO
export TEMP_AUDIO_DIR=./temp_audio
export HOST=0.0.0.0
export PORT=8000
export DEBUG=False
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **VADER Sentiment**: Social media sentiment analysis
- **TextBlob**: Natural language processing
- **Hugging Face**: Pre-trained emotion classification models
- **pyttsx3**: Cross-platform TTS engine
- **FastAPI**: Modern web framework for APIs
- **Font Awesome**: Beautiful icons for the web interface
- **CSS Grid & Flexbox**: Modern responsive layout techniques
- **HTML5 Audio API**: Real-time audio playback functionality

---

**The Empathy Engine** - Bringing human emotion to AI voice synthesis 🎙️✨

