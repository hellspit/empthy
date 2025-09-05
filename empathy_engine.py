import os
import tempfile
import logging
from typing import Dict, List, Optional, Tuple
import numpy as np
from datetime import datetime

# Emotion detection imports
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import pipeline

# TTS imports
import pyttsx3
from gtts import gTTS
from pydub import AudioSegment
from pydub.effects import speedup
import io

from config import config

logger = logging.getLogger(__name__)

class EmpathyEngine:
    """
    The Empathy Engine - AI-powered TTS with emotional voice modulation
    """
    
    def __init__(self):
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        
        # Initialize Hugging Face emotion classifier
        if config.USE_HUGGING_FACE:
            try:
                self.emotion_classifier = pipeline(
                    "text-classification",
                    model="j-hartmann/emotion-english-distilroberta-base",
                    return_all_scores=True
                )
                logger.info("Hugging Face emotion classifier loaded successfully")
            except Exception as e:
                logger.warning(f"Could not load Hugging Face emotion classifier: {e}")
                self.emotion_classifier = None
        else:
            self.emotion_classifier = None
            logger.info("Hugging Face emotion classifier disabled by configuration")
        
        # Initialize TTS engine
        self.tts_engine = pyttsx3.init()
        self._configure_tts_engine()
        
        # Emotion to vocal parameter mapping (from config)
        self.emotion_mappings = config.EMOTION_MAPPINGS
        
        # Create temp audio directory
        os.makedirs(config.TEMP_AUDIO_DIR, exist_ok=True)
    
    def _configure_tts_engine(self):
        """Configure the TTS engine with default settings"""
        voices = self.tts_engine.getProperty('voices')
        if voices:
            # Try to find a female voice (usually more expressive)
            for voice in voices:
                if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                    self.tts_engine.setProperty('voice', voice.id)
                    break
            else:
                # Use the first available voice
                self.tts_engine.setProperty('voice', voices[0].id)
        
        # Set default properties
        self.tts_engine.setProperty('rate', config.DEFAULT_RATE)  # Words per minute
        self.tts_engine.setProperty('volume', config.DEFAULT_VOLUME)
    
    def detect_emotion(self, text: str) -> Tuple[str, float]:
        """
        Detect emotion in text using multiple methods
        
        Returns:
            Tuple of (emotion, confidence)
        """
        # Method 1: VADER Sentiment Analysis
        vader_scores = self.sentiment_analyzer.polarity_scores(text)
        
        # Method 2: TextBlob Sentiment
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        
        # Method 3: Hugging Face Emotion Classification (if available)
        hf_emotion = None
        hf_confidence = 0.0
        
        if self.emotion_classifier:
            try:
                hf_results = self.emotion_classifier(text)
                if hf_results and len(hf_results) > 0:
                    # Get the highest scoring emotion
                    best_result = max(hf_results[0], key=lambda x: x['score'])
                    hf_emotion = best_result['label'].lower()
                    hf_confidence = best_result['score']
            except Exception as e:
                logger.warning(f"Hugging Face emotion detection failed: {e}")
        
        # Combine results for final emotion detection
        emotion, confidence = self._combine_emotion_results(
            vader_scores, polarity, subjectivity, hf_emotion, hf_confidence
        )
        
        logger.info(f"Detected emotion: {emotion} (confidence: {confidence:.2f})")
        return emotion, confidence
    
    def _combine_emotion_results(self, vader_scores: Dict, polarity: float, 
                                subjectivity: float, hf_emotion: Optional[str], 
                                hf_confidence: float) -> Tuple[str, float]:
        """Combine multiple emotion detection results"""
        
        # VADER-based emotion mapping
        if vader_scores['compound'] >= 0.05:
            vader_emotion = 'joy'
        elif vader_scores['compound'] <= -0.05:
            vader_emotion = 'sadness'
        else:
            vader_emotion = 'neutral'
        
        # TextBlob-based emotion mapping
        if polarity > 0.1:
            blob_emotion = 'joy'
        elif polarity < -0.1:
            blob_emotion = 'sadness'
        else:
            blob_emotion = 'neutral'
        
        # Weighted combination
        emotions = []
        confidences = []
        
        # VADER (weight: 0.4)
        emotions.append(vader_emotion)
        confidences.append(abs(vader_scores['compound']) * 0.4)
        
        # TextBlob (weight: 0.3)
        emotions.append(blob_emotion)
        confidences.append(abs(polarity) * 0.3)
        
        # Hugging Face (weight: 0.3)
        if hf_emotion:
            emotions.append(hf_emotion)
            confidences.append(hf_confidence * 0.3)
        
        # Find the most confident emotion
        if emotions:
            emotion_counts = {}
            for i, emotion in enumerate(emotions):
                if emotion in emotion_counts:
                    emotion_counts[emotion] += confidences[i]
                else:
                    emotion_counts[emotion] = confidences[i]
            
            final_emotion = max(emotion_counts, key=emotion_counts.get)
            final_confidence = emotion_counts[final_emotion]
        else:
            final_emotion = 'neutral'
            final_confidence = 0.5
        
        return final_emotion, final_confidence
    
    def get_vocal_parameters(self, emotion: str, intensity: float = 1.0) -> Dict:
        """
        Get vocal parameters for a given emotion with intensity scaling
        
        Args:
            emotion: The detected emotion
            intensity: Intensity multiplier (0.1-2.0)
        """
        # Clamp intensity to reasonable range using config validation
        intensity = config.validate_intensity(intensity)
        
        # Get base parameters for emotion using config method
        base_params = config.get_emotion_mapping(emotion)
        
        # Apply intensity scaling with validation - more human-like scaling
        # Rate: More conservative scaling to avoid too fast speech
        rate_multiplier = 0.7 + (0.3 * intensity)  # 0.7 to 1.0 range for intensity 0.1 to 2.0
        
        # Pitch: Moderate scaling for natural variation
        pitch_multiplier = 0.85 + (0.3 * intensity)  # 0.85 to 1.45 range for intensity 0.1 to 2.0
        
        # Volume: Linear scaling for clear intensity effect
        volume_multiplier = 0.6 + (0.4 * intensity)  # 0.6 to 1.4 range for intensity 0.1 to 2.0
        
        scaled_params = {
            "rate": config.validate_vocal_parameter("rate", base_params["rate"] * rate_multiplier),
            "pitch": config.validate_vocal_parameter("pitch", base_params["pitch"] * pitch_multiplier),
            "volume": config.validate_vocal_parameter("volume", base_params["volume"] * volume_multiplier),
            "description": base_params["description"]
        }
        
        return scaled_params
    
    def synthesize_with_emotion(self, text: str, emotion_override: Optional[str] = None, 
                               intensity: float = 1.0, custom_filename: Optional[str] = None) -> Dict:
        """
        Synthesize speech with emotional modulation
        
        Args:
            text: Text to synthesize
            emotion_override: Force specific emotion (skips detection)
            intensity: Emotion intensity (0.1-2.0)
            custom_filename: Optional custom filename (without extension)
        
        Returns:
            Dictionary with emotion, vocal parameters, and audio file path
        """
        # Detect emotion if not overridden
        if emotion_override:
            emotion = emotion_override.lower()
            confidence = 1.0
        else:
            emotion, confidence = self.detect_emotion(text)
        
        # Get vocal parameters
        vocal_params = self.get_vocal_parameters(emotion, intensity)
        
        # Generate audio file
        audio_file = self._generate_audio(text, vocal_params, custom_filename)
        
        return {
            "emotion": emotion,
            "confidence": confidence,
            "vocal_parameters": vocal_params,
            "audio_file": audio_file
        }
    
    def _generate_audio(self, text: str, vocal_params: Dict, custom_filename: Optional[str] = None) -> str:
        """Generate audio file with specified vocal parameters"""
        try:
            # Generate filename
            if custom_filename:
                # Clean the custom filename (remove invalid characters)
                import re
                clean_filename = re.sub(r'[<>:"/\\|?*]', '_', custom_filename)
                filename = f"{clean_filename}.{config.AUDIO_FORMAT}"
            else:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"empathy_audio_{timestamp}.{config.AUDIO_FORMAT}"
            
            filepath = os.path.join(config.TEMP_AUDIO_DIR, filename)
            
            # Generate base audio using pyttsx3
            self.tts_engine.setProperty('rate', int(config.DEFAULT_RATE * vocal_params['rate']))
            self.tts_engine.setProperty('volume', vocal_params['volume'])
            
            # Save to temporary file
            self.tts_engine.save_to_file(text, filepath)
            self.tts_engine.runAndWait()
            
            # Apply pitch modulation using pydub
            audio = AudioSegment.from_wav(filepath)
            
            # Apply pitch shift using simple speed adjustment
            # Note: This is a simplified approach - for better pitch shifting, 
            # you would need FFmpeg or a more advanced audio library
            pitch_factor = vocal_params['pitch']
            if abs(pitch_factor - 1.0) > 0.05:  # Only apply if significant change
                # Simple pitch adjustment by changing sample rate
                new_sample_rate = int(audio.frame_rate * pitch_factor)
                audio = audio._spawn(audio.raw_data, overrides={"frame_rate": new_sample_rate})
                audio = audio.set_frame_rate(audio.frame_rate)
            
            # Apply speed change
            if abs(vocal_params['rate'] - 1.0) > 0.05:  # Only apply if significant change
                audio = speedup(audio, playback_speed=vocal_params['rate'])
            
            # Export final audio
            audio.export(filepath, format=config.AUDIO_FORMAT)
            
            logger.info(f"Generated audio file: {filepath}")
            return filename
            
        except Exception as e:
            logger.error(f"Error generating audio: {e}")
            raise
    
    def get_available_emotions(self) -> List[Dict]:
        """Get list of available emotions and their descriptions"""
        return [
            {
                "emotion": emotion,
                "description": params["description"],
                "parameters": {
                    "rate": params["rate"],
                    "pitch": params["pitch"],
                    "volume": params["volume"]
                }
            }
            for emotion, params in self.emotion_mappings.items()
        ]
    
    def cleanup_old_audio_files(self, max_age_hours: int = None):
        """Clean up old audio files to prevent disk space issues"""
        import time
        current_time = time.time()
        max_age_hours = max_age_hours or config.AUDIO_CLEANUP_HOURS
        max_age_seconds = max_age_hours * 3600
        
        try:
            for filename in os.listdir(config.TEMP_AUDIO_DIR):
                if filename.startswith("empathy_audio_"):
                    filepath = os.path.join(config.TEMP_AUDIO_DIR, filename)
                    file_age = current_time - os.path.getctime(filepath)
                    
                    if file_age > max_age_seconds:
                        os.remove(filepath)
                        logger.info(f"Cleaned up old audio file: {filename}")
        except Exception as e:
            logger.warning(f"Error cleaning up audio files: {e}")

