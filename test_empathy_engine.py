#!/usr/bin/env python3
"""
Test script for The Empathy Engine
Demonstrates various emotions and vocal modulations
"""

import requests
import json
import time
import os

# API base URL
BASE_URL = "http://localhost:8000"

def test_emotion_detection():
    """Test emotion detection with various text samples"""
    
    test_cases = [
        {
            "text": "Congratulations! This is absolutely fantastic news! I'm so excited!",
            "expected_emotion": "joy",
            "intensity": 1.5
        },
        {
            "text": "I'm really sorry to hear about your loss. This must be very difficult for you.",
            "expected_emotion": "sadness",
            "intensity": 1.2
        },
        {
            "text": "This is completely unacceptable! I demand an explanation immediately!",
            "expected_emotion": "anger",
            "intensity": 1.8
        },
        {
            "text": "Oh my goodness! I can't believe what just happened!",
            "expected_emotion": "surprise",
            "intensity": 1.3
        },
        {
            "text": "I'm really worried about what might happen next. This is concerning.",
            "expected_emotion": "fear",
            "intensity": 1.1
        },
        {
            "text": "The weather today is partly cloudy with a chance of rain.",
            "expected_emotion": "neutral",
            "intensity": 1.0
        }
    ]
    
    print("🎙️ Testing The Empathy Engine")
    print("=" * 50)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test_case['expected_emotion'].upper()}")
        print(f"Text: \"{test_case['text']}\"")
        print(f"Expected: {test_case['expected_emotion']} (intensity: {test_case['intensity']})")
        
        try:
            # Make API request
            response = requests.post(
                f"{BASE_URL}/synthesize",
                json={
                    "text": test_case["text"],
                    "intensity": test_case["intensity"]
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                detected_emotion = result["emotion_detected"]
                vocal_params = result["vocal_parameters"]
                audio_file = result["audio_file_path"]
                
                print(f"✅ Detected: {detected_emotion}")
                print(f"📊 Vocal Parameters:")
                print(f"   Rate: {vocal_params['rate']:.2f}x")
                print(f"   Pitch: {vocal_params['pitch']:.2f}x")
                print(f"   Volume: {vocal_params['volume']:.2f}")
                print(f"🎵 Audio: {audio_file}")
                
                # Check if emotion matches expectation
                if detected_emotion == test_case['expected_emotion']:
                    print("✅ Emotion detection correct!")
                else:
                    print(f"⚠️  Emotion mismatch (expected: {test_case['expected_emotion']})")
                    
            else:
                print(f"❌ API Error: {response.status_code}")
                print(f"Response: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {e}")
        
        print("-" * 30)

def test_api_endpoints():
    """Test all API endpoints"""
    
    print("\n🔍 Testing API Endpoints")
    print("=" * 50)
    
    endpoints = [
        ("GET", "/", "Root endpoint"),
        ("GET", "/health", "Health check"),
        ("GET", "/emotions", "Available emotions"),
    ]
    
    for method, endpoint, description in endpoints:
        try:
            if method == "GET":
                response = requests.get(f"{BASE_URL}{endpoint}", timeout=10)
            
            if response.status_code == 200:
                print(f"✅ {method} {endpoint} - {description}")
                if endpoint == "/emotions":
                    data = response.json()
                    print(f"   Found {len(data['emotions'])} emotions")
            else:
                print(f"❌ {method} {endpoint} - Status: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ {method} {endpoint} - Error: {e}")

def test_intensity_scaling():
    """Test intensity scaling with the same text"""
    
    print("\n📈 Testing Intensity Scaling")
    print("=" * 50)
    
    text = "This is really good news!"
    intensities = [0.5, 1.0, 1.5, 2.0]
    
    for intensity in intensities:
        try:
            response = requests.post(
                f"{BASE_URL}/synthesize",
                json={
                    "text": text,
                    "intensity": intensity
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                vocal_params = result["vocal_parameters"]
                
                print(f"Intensity {intensity}: Rate={vocal_params['rate']:.2f}, "
                      f"Pitch={vocal_params['pitch']:.2f}, Volume={vocal_params['volume']:.2f}")
            else:
                print(f"❌ Intensity {intensity} failed: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Intensity {intensity} error: {e}")

def main():
    """Run all tests"""
    
    print("🚀 Starting Empathy Engine Tests")
    print("Make sure the server is running on http://localhost:8000")
    print("Start server with: python main.py")
    print()
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code != 200:
            print("❌ Server is not running or not responding")
            return
    except requests.exceptions.RequestException:
        print("❌ Cannot connect to server. Please start the server first:")
        print("   python main.py")
        return
    
    print("✅ Server is running!")
    
    # Run tests
    test_api_endpoints()
    test_emotion_detection()
    test_intensity_scaling()
    
    print("\n🎉 All tests completed!")
    print("\nTo listen to generated audio files:")
    print("1. Check the 'temp_audio' directory")
    print("2. Or access via API: http://localhost:8000/audio/{filename}")

if __name__ == "__main__":
    main()

