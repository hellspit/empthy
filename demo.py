#!/usr/bin/env python3
"""
Demo script for The Empathy Engine
Shows how to use the API programmatically
"""

import requests
import json
import time

def demo_empathy_engine():
    """Demonstrate The Empathy Engine functionality"""
    
    # API base URL
    base_url = "http://localhost:8000"
    
    print("🎙️ The Empathy Engine - Demo")
    print("=" * 40)
    
    # Check if server is running
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code != 200:
            print("❌ Server is not running. Please start it with: python main.py")
            return
    except requests.exceptions.RequestException:
        print("❌ Cannot connect to server. Please start it with: python main.py")
        return
    
    print("✅ Server is running!")
    
    # Demo texts with different emotions
    demo_texts = [
        {
            "text": "Welcome to our amazing new product launch! This is going to revolutionize everything!",
            "emotion": "joy",
            "description": "Enthusiastic product announcement"
        },
        {
            "text": "I'm deeply sorry for the inconvenience this has caused you and your family.",
            "emotion": "sadness", 
            "description": "Apologetic customer service"
        },
        {
            "text": "This is completely unacceptable! I demand immediate action!",
            "emotion": "anger",
            "description": "Angry customer complaint"
        },
        {
            "text": "Oh my goodness! I can't believe what just happened!",
            "emotion": "surprise",
            "description": "Surprised reaction"
        },
        {
            "text": "I'm really concerned about the potential risks involved here.",
            "emotion": "fear",
            "description": "Concerned warning"
        },
        {
            "text": "The meeting is scheduled for 3 PM in conference room A.",
            "emotion": "neutral",
            "description": "Neutral information"
        }
    ]
    
    print(f"\n🎭 Processing {len(demo_texts)} different emotional contexts...")
    print("-" * 60)
    
    for i, demo in enumerate(demo_texts, 1):
        print(f"\n{i}. {demo['description'].upper()}")
        print(f"   Text: \"{demo['text']}\"")
        print(f"   Expected: {demo['emotion']}")
        
        try:
            # Synthesize speech
            response = requests.post(
                f"{base_url}/synthesize",
                json={
                    "text": demo["text"],
                    "intensity": 1.2  # Slightly higher intensity for demo
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                
                print(f"   ✅ Detected: {result['emotion_detected']}")
                print(f"   📊 Vocal Parameters:")
                print(f"      Rate: {result['vocal_parameters']['rate']:.2f}x")
                print(f"      Pitch: {result['vocal_parameters']['pitch']:.2f}x") 
                print(f"      Volume: {result['vocal_parameters']['volume']:.2f}")
                print(f"   🎵 Audio: {result['audio_file_path']}")
                
                # Check if detection matches expectation
                if result['emotion_detected'] == demo['emotion']:
                    print("   ✅ Emotion detection accurate!")
                else:
                    print(f"   ⚠️  Emotion mismatch (expected: {demo['emotion']})")
                    
            else:
                print(f"   ❌ Error: {response.status_code} - {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Request failed: {e}")
        
        # Small delay between requests
        time.sleep(1)
    
    print("\n" + "=" * 60)
    print("🎉 Demo completed!")
    print("\nGenerated audio files are available in the 'temp_audio' directory")
    print("You can also access them via the API at:")
    print("http://localhost:8000/audio/{filename}")

def demo_intensity_comparison():
    """Demonstrate intensity scaling with the same text"""
    
    print("\n📈 Intensity Scaling Demo")
    print("=" * 40)
    
    base_url = "http://localhost:8000"
    text = "This is absolutely incredible news!"
    intensities = [0.5, 1.0, 1.5, 2.0]
    
    print(f"Text: \"{text}\"")
    print("\nTesting different intensity levels:")
    print("-" * 50)
    
    for intensity in intensities:
        try:
            response = requests.post(
                f"{base_url}/synthesize",
                json={
                    "text": text,
                    "intensity": intensity
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                params = result['vocal_parameters']
                
                print(f"Intensity {intensity:3.1f}: "
                      f"Rate={params['rate']:4.2f}x, "
                      f"Pitch={params['pitch']:4.2f}x, "
                      f"Volume={params['volume']:4.2f}")
            else:
                print(f"Intensity {intensity}: ❌ Failed ({response.status_code})")
                
        except requests.exceptions.RequestException as e:
            print(f"Intensity {intensity}: ❌ Error - {e}")

def demo_emotion_override():
    """Demonstrate emotion override functionality"""
    
    print("\n🎭 Emotion Override Demo")
    print("=" * 40)
    
    base_url = "http://localhost:8000"
    text = "The weather is nice today."
    
    print(f"Text: \"{text}\"")
    print("(This would normally be detected as 'neutral')")
    print("\nForcing different emotions:")
    print("-" * 50)
    
    emotions_to_test = ["joy", "sadness", "anger", "fear", "surprise"]
    
    for emotion in emotions_to_test:
        try:
            response = requests.post(
                f"{base_url}/synthesize",
                json={
                    "text": text,
                    "emotion_override": emotion,
                    "intensity": 1.3
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                params = result['vocal_parameters']
                
                print(f"{emotion:8}: Rate={params['rate']:4.2f}x, "
                      f"Pitch={params['pitch']:4.2f}x, "
                      f"Volume={params['volume']:4.2f}")
            else:
                print(f"{emotion:8}: ❌ Failed ({response.status_code})")
                
        except requests.exceptions.RequestException as e:
            print(f"{emotion:8}: ❌ Error - {e}")

if __name__ == "__main__":
    print("Starting The Empathy Engine Demo...")
    print("Make sure the server is running: python main.py")
    print()
    
    # Run demos
    demo_empathy_engine()
    demo_intensity_comparison()
    demo_emotion_override()
    
    print("\n🎊 All demos completed!")
    print("\nNext steps:")
    print("1. Check the 'temp_audio' directory for generated files")
    print("2. Visit http://localhost:8000/docs for interactive API documentation")
    print("3. Try the test script: python test_empathy_engine.py")

