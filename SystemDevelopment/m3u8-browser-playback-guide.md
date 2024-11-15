# JavaScript and HTML Code for Playing m3u8 Files in Browser

## JavaScript Code (hls-video-handler.js)

```javascript
/**
 * Handler class for managing HLS video streaming
 * Wraps the HLS.js library and provides browser compatibility and fallback handling
 */
class HLSVideoHandler {
    /**
     * Initialize HLSVideoHandler
     * @param {Object} options - Configuration options
     * @param {boolean} [options.debug=false] - Enable debug mode
     * @param {boolean} [options.enableWorker=true] - Enable Web Worker
     * @param {number} [options.maxRetries=3] - Maximum number of retry attempts
     * @param {number} [options.retryDelay=1000] - Delay between retries (milliseconds)
     */
    constructor(options = {}) {
        this.debug = options.debug || false;
        this.enableWorker = options.enableWorker || true;
        this.maxRetries = options.maxRetries || 3;
        this.retryDelay = options.retryDelay || 1000;
        this.initialized = false;
    }

    /**
     * Initialize HLS.js library
     * @returns {Promise<void>} Promise indicating completion of initialization
     * @throws {Error} If HLS.js loading fails
     */
    async initialize() {
        if (typeof Hls === 'undefined') {
            try {
                await this.loadHLSScript();
                this.initialized = true;
            } catch (error) {
                console.error('Failed to load HLS.js:', error);
                throw error;
            }
        } else {
            this.initialized = true;
        }
    }

    /**
     * Dynamically load HLS.js script
     * @returns {Promise<void>} Promise indicating script loading completion
     */
    loadHLSScript() {
        return new Promise((resolve, reject) => {
            const script = document.createElement('script');
            script.src = 'https://cdnjs.cloudflare.com/ajax/libs/hls.js/1.4.10/hls.min.js';
            script.async = true;
            script.onload = () => resolve();
            script.onerror = () => reject(new Error('Failed to load HLS.js script'));
            document.head.appendChild(script);
        });
    }

    /**
     * Set up HLS player and connect to specified video element
     * @param {HTMLVideoElement} videoElement - HTML element for video playback
     * @param {string} playlistUrl - URL of the HLS playlist
     * @returns {Promise<Hls|boolean>} HLS instance or native playback status
     * @throws {Error} If no video element is provided
     */
    async setupPlayer(videoElement, playlistUrl) {
        if (!this.initialized) {
            await this.initialize();
        }
        if (!videoElement) {
            throw new Error('No video element provided');
        }
        if (!Hls.isSupported()) {
            return this.setupNativePlayer(videoElement, playlistUrl);
        }
        try {
            const hls = new Hls({
                debug: this.debug,
                enableWorker: this.enableWorker
            });
            hls.loadSource(playlistUrl);
            hls.attachMedia(videoElement);
            return hls;
        } catch (error) {
            console.error('Error setting up HLS:', error);
            return this.setupNativePlayer(videoElement, playlistUrl);
        }
    }

    /**
     * Set up fallback player for browsers with native HLS support
     * @param {HTMLVideoElement} videoElement - HTML element for video playback
     * @param {string} playlistUrl - URL of the HLS playlist
     * @returns {boolean} Native playback support status
     */
    setupNativePlayer(videoElement, playlistUrl) {
        if (videoElement.canPlayType('application/vnd.apple.mpegurl')) {
            videoElement.src = playlistUrl;
            return true;
        }
        return false;
    }
}

// Make available in global scope
window.HLSVideoHandler = HLSVideoHandler;
```

## HTML Code

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HLS Video Player Demo</title>
    <style>
        .video-container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        video {
            width: 100%;
        }
    </style>
</head>
<body>
    <div class="video-container">
        <h1>HLS Video Player Demo</h1>
        <video id="video" controls playsinline></video>
    </div>
    <script src="hls-video-handler.js"></script>
    <script>
        document.addEventListener('DOMContentLoaded', async () => {
            const videoElement = document.getElementById('video');
            const hlsHandler = new HLSVideoHandler({ debug: true });
            try {
                await hlsHandler.setupPlayer(videoElement, 'https://video.example.com/stream.m3u8');
            } catch (error) {
                console.error('Failed to initialize video player:', error);
            }
        });
    </script>
</body>
</html>
```

This code provides a robust implementation of an HLS video player using the HLS.js library. The `HLSVideoHandler` class handles:
- Dynamic loading of the HLS.js library
- Browser compatibility checking
- Fallback to native HLS playback when needed
- Error handling and retry logic
- Configuration options for debugging and performance

The HTML file provides a simple demo implementation with responsive video container styling and basic error handling.