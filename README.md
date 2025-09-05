# The Empathy Engine 🎙️

**AI-powered Text-to-Speech with Emotional Voice Modulation**

The Empathy Engine is a FastAPI-based service that dynamically modulates vocal characteristics of synthesized speech based on detected emotions in the input text. It bridges the gap between text-based sentiment and expressive, human-like audio output.

## 🌟 Features

### Core Functionality
- **Text Input Processing**: Accepts text input via REST API
- **Multi-Method Emotion Detection**: Uses VADER, TextBlob, and Hugging Face transformers
- **Vocal Parameter Modulation**: Adjusts rate, pitch, and volume based on emotions
- **Emotion-to-Voice Mapping**: Clear logic mapping emotions to vocal characteristics
- **Audio Output**: Generates playable WAV files

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

4. **Access the API**
   - API Documentation: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health
   - Available Emotions: http://localhost:8000/emotions

## 📖 API Usage

### Synthesize Speech
```bash
curl -X POST "http://localhost:8000/synthesize" \
     -H "Content-Type: application/json" \
     -d '{
       "text": "This is amazing news! I am so excited!",
       "intensity": 1.5
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
| GET | `/` | API information and available endpoints |
| GET | `/health` | Health check |
| GET | `/emotions` | List available emotions and parameters |
| POST | `/synthesize` | Convert text to emotionally modulated speech |
| GET | `/audio/{filename}` | Download generated audio files |

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
   - Request/response handling
   - CORS middleware

2. **Empathy Engine** (`empathy_engine.py`)
   - Emotion detection logic
   - Vocal parameter calculation
   - Audio synthesis and modulation

3. **Dependencies** (`requirements.txt`)
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

### Manual Testing
1. Start the server: `python main.py`
2. Visit http://localhost:8000/docs for interactive API documentation
3. Test different emotions with various text inputs

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
- **Web Interface**: Real-time demo with audio player
- **Voice Selection**: Multiple voice options for different personas
- **Real-time Streaming**: WebSocket support for live audio streaming
- **Emotion Intensity Learning**: ML-based intensity prediction
- **Multi-language Support**: Emotion detection in multiple languages

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **VADER Sentiment**: Social media sentiment analysis
- **TextBlob**: Natural language processing
- **Hugging Face**: Pre-trained emotion classification models
- **pyttsx3**: Cross-platform TTS engine
- **FastAPI**: Modern web framework for APIs

---

**The Empathy Engine** - Bringing human emotion to AI voice synthesis 🎙️✨

