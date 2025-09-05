// The Empathy Engine Frontend JavaScript

class EmpathyEngine {
    constructor() {
        this.apiBaseUrl = 'http://localhost:8000';
        this.audioPlayer = document.getElementById('audioPlayer');
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        // Generate button
        document.getElementById('generateBtn').addEventListener('click', () => {
            this.generateSpeech();
        });

        // Intensity slider
        const intensitySlider = document.getElementById('intensitySlider');
        const intensityValue = document.getElementById('intensityValue');
        
        intensitySlider.addEventListener('input', (e) => {
            intensityValue.textContent = e.target.value;
        });

        // Play button
        document.getElementById('playBtn').addEventListener('click', () => {
            this.playAudio();
        });

        // Download button
        document.getElementById('downloadBtn').addEventListener('click', () => {
            this.downloadAudio();
        });

        // Enter key in textarea
        document.getElementById('textInput').addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.key === 'Enter') {
                this.generateSpeech();
            }
        });
    }

    async generateSpeech() {
        const textInput = document.getElementById('textInput');
        const emotionSelect = document.getElementById('emotionSelect');
        const intensitySlider = document.getElementById('intensitySlider');
        const filenameInput = document.getElementById('filenameInput');

        // Validate input
        if (!textInput.value.trim()) {
            this.showError('Please enter some text to synthesize.');
            return;
        }

        // Show loading
        this.showLoading(true);
        this.hideError();
        this.hideOutput();

        try {
            // Prepare request data
            const requestData = {
                text: textInput.value.trim(),
                intensity: parseFloat(intensitySlider.value)
            };

            // Add emotion override if selected
            if (emotionSelect.value) {
                requestData.emotion_override = emotionSelect.value;
            }

            // Add custom filename if provided
            if (filenameInput.value.trim()) {
                requestData.filename = filenameInput.value.trim();
            }

            // Make API request
            const response = await fetch(`${this.apiBaseUrl}/synthesize`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestData)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
            }

            const result = await response.json();
            this.displayResult(result);

        } catch (error) {
            console.error('Error generating speech:', error);
            this.showError(`Failed to generate speech: ${error.message}`);
        } finally {
            this.showLoading(false);
        }
    }

    displayResult(result) {
        // Update UI with results
        document.getElementById('detectedEmotion').textContent = result.emotion_detected;
        document.getElementById('rateValue').textContent = result.vocal_parameters.rate.toFixed(2);
        document.getElementById('pitchValue').textContent = result.vocal_parameters.pitch.toFixed(2);
        document.getElementById('volumeValue').textContent = result.vocal_parameters.volume.toFixed(2);
        document.getElementById('audioFilename').textContent = result.audio_file_path;

        // Store audio file path for playback/download
        this.currentAudioFile = result.audio_file_path;

        // Show output section
        this.showOutput();
    }

    async playAudio() {
        if (!this.currentAudioFile) {
            this.showError('No audio file available to play.');
            return;
        }

        try {
            const audioUrl = `${this.apiBaseUrl}/audio/${this.currentAudioFile}`;
            this.audioPlayer.src = audioUrl;
            
            // Play the audio
            await this.audioPlayer.play();
            
            // Update play button
            const playBtn = document.getElementById('playBtn');
            const playIcon = playBtn.querySelector('i');
            playBtn.innerHTML = '<i class="fas fa-pause"></i> Pause Audio';
            
            // Listen for audio end
            this.audioPlayer.onended = () => {
                playBtn.innerHTML = '<i class="fas fa-play"></i> Play Audio';
            };

        } catch (error) {
            console.error('Error playing audio:', error);
            this.showError('Failed to play audio. Please try downloading the file instead.');
        }
    }

    downloadAudio() {
        if (!this.currentAudioFile) {
            this.showError('No audio file available to download.');
            return;
        }

        const audioUrl = `${this.apiBaseUrl}/audio/${this.currentAudioFile}`;
        const link = document.createElement('a');
        link.href = audioUrl;
        link.download = this.currentAudioFile;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }

    showLoading(show) {
        const loading = document.getElementById('loading');
        const generateBtn = document.getElementById('generateBtn');
        
        if (show) {
            loading.style.display = 'block';
            generateBtn.disabled = true;
            generateBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Generating...';
        } else {
            loading.style.display = 'none';
            generateBtn.disabled = false;
            generateBtn.innerHTML = '<i class="fas fa-play"></i> Generate Speech';
        }
    }

    showOutput() {
        document.getElementById('outputSection').style.display = 'block';
    }

    hideOutput() {
        document.getElementById('outputSection').style.display = 'none';
    }

    showError(message) {
        const errorDiv = document.getElementById('error');
        const errorMessage = document.getElementById('errorMessage');
        errorMessage.textContent = message;
        errorDiv.style.display = 'flex';
    }

    hideError() {
        document.getElementById('error').style.display = 'none';
    }

    // Check API health
    async checkApiHealth() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/health`);
            if (response.ok) {
                console.log('API is healthy');
                return true;
            } else {
                console.warn('API health check failed');
                return false;
            }
        } catch (error) {
            console.error('API health check error:', error);
            return false;
        }
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const app = new EmpathyEngine();
    
    // Check API health on load
    app.checkApiHealth().then(healthy => {
        if (!healthy) {
            app.showError('Unable to connect to the API server. Please make sure the server is running on localhost:8000');
        }
    });

    // Add some example text
    const textInput = document.getElementById('textInput');
    textInput.value = 'Hello, my name is Anuj. How are you today?';
});

// Add some helpful keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Ctrl+Enter to generate speech
    if (e.ctrlKey && e.key === 'Enter') {
        e.preventDefault();
        document.getElementById('generateBtn').click();
    }
    
    // Escape to clear error
    if (e.key === 'Escape') {
        document.getElementById('error').style.display = 'none';
    }
});
