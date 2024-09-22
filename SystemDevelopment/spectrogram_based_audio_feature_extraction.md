# Python Script for Extracting Spectrogram-Based Features as Strings in Audio Processing

## Overview

This document explains a Python program that processes audio files to extract spectrogram-based features. The program consists of two main scripts:

1. `spectrogram_based_audio_to_text.py`: Extracts spectrogram-based features
2. `wav_volume_based_trimmer.py`: Trims audio based on volume

## 1. Spectrogram-Based Feature Extraction (spectrogram_based_audio_to_text.py)

### About Spectrogram-Based Feature Extraction

A spectrogram is a time-frequency representation of an audio signal. It's a powerful tool for simultaneously visualizing temporal changes and frequency components in audio.

#### Characteristics
- The horizontal axis represents time, and the vertical axis represents frequency.
- Signal intensity (amplitude) is represented by color or shading.
- Allows simultaneous observation of temporal changes and frequency characteristics in audio.

#### Advantages
1. Integration of time and frequency information
2. Rich information content
3. Flexibility
4. Noise resistance
5. Compatibility with pattern recognition

#### Disadvantages
1. High-dimensional data
2. Loss of phase information
3. Time-frequency resolution trade-off
4. Impact of background noise
5. Complexity of interpretation

### Main Functions

- Generate mel spectrograms from audio files
- Apply Principal Component Analysis (PCA) to reduce feature dimensionality
- Convert features to strings (Base64 encoded)

### Key Functions

1. `create_spectrogram_features(audio_file, n_mels=128, n_fft=2048, hop_length=512)`
   Generates a mel spectrogram from an audio file.

2. `apply_pca(features, n_components=10)`
   Applies PCA to reduce feature dimensionality.

3. `features_to_feature_string(features)`
   Converts features to a Base64 encoded string.

4. `audio_to_spectrogram_pca_feature_string(audio_file)`
   Main function that processes audio files to generate feature strings.

### Configurable Parameters

1. Parameters for `create_spectrogram_features` function:
   - `n_mels` (default: 128): Number of mel filter banks
   - `n_fft` (default: 2048): FFT window size
   - `hop_length` (default: 512): Number of samples between successive frames

2. Parameters for `apply_pca` function:
   - `n_components` (default: 10): Number of principal components to retain

3. Main processing section:
   - `audio_file` (default: "input_audio.wav"): Path to the input audio file
   - `threshold` (argument for wav_volume_based_trimmer, default: 0.1): Threshold for audio trimming
   - `duration` (argument for wav_volume_based_trimmer, default: 1.0): Duration of audio to trim (in seconds)

### Script

```python
import numpy as np
import librosa
import base64
from pydub import AudioSegment
from sklearn.decomposition import PCA
import wav_volume_based_trimmer
import os

def create_spectrogram_features(audio_file, n_mels=128, n_fft=2048, hop_length=512):
    try:
        # Load the audio file (1 second)
        y, sr = librosa.load(audio_file, offset=0, duration=1)
    except FileNotFoundError:
        print(f"Error: Audio file '{audio_file}' not found.")
        return None
    except Exception as e:
        print(f"Error: A problem occurred while loading the audio file: {str(e)}")
        return None

    # Calculate mel spectrogram
    spectrogram = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=n_mels, n_fft=n_fft, hop_length=hop_length)
    # Convert to decibel scale
    spectrogram_db = librosa.power_to_db(spectrogram, ref=np.max)
    return spectrogram_db

def apply_pca(features, n_components=10):
    # Apply PCA
    pca = PCA(n_components=n_components)
    pca_features = pca.fit_transform(features.T).T
    return pca_features

def features_to_feature_string(features):
    # Convert features to a 1D array
    flattened = features.flatten()
    # Normalize values to 0-255 range
    normalized = ((flattened - flattened.min()) / (flattened.max() - flattened.min()) * 255).astype(np.uint8)
    # Convert to bytes
    byte_data = normalized.tobytes()
    # Base64 encode
    base64_str = base64.b64encode(byte_data).decode('utf-8')
    return base64_str

def audio_to_spectrogram_pca_feature_string(audio_file):
    # Extract spectrogram features
    spectrogram = create_spectrogram_features(audio_file)
    if spectrogram is None:
        return None
    # Apply PCA for dimensionality reduction
    pca_features = apply_pca(spectrogram)
    # Convert features to string
    feature_string = features_to_feature_string(pca_features)
    return feature_string

if __name__ == "__main__":
    audio_file = "input_audio.wav"  # Input audio file
    if not os.path.exists(audio_file):
        print(f"Error: Input audio file '{audio_file}' not found.")
    else:
        try:
            wav_volume_based_trimmer.main(audio_file)
        except Exception as e:
            print(f"Error: A problem occurred during audio trimming: {str(e)}")
        else:
            trimmed_file = f"trimmed_{audio_file}"
            if not os.path.exists(trimmed_file):
                print(f"Warning: Trimmed file '{trimmed_file}' not found. Using original file.")
                trimmed_file = audio_file
            result = audio_to_spectrogram_pca_feature_string(trimmed_file)
            if result:
                print("Spectrogram-PCA feature string:")
                print(result[:100] + "...")  # Display only the first 100 characters
                print(f"Feature string length: {len(result)}")
                print("Conversion process completed.")
            else:
                print("Conversion process failed.")
```

## 2. Volume-Based Audio Trimming (wav_volume_based_trimmer.py)

### Main Functions

- Read audio data from WAV files
- Find the first position exceeding a specified threshold
- Cut out audio of specified length from that position

### Key Functions

1. `trim_audio(input_file, output_file, threshold=0.1, duration=1.0)`
   Main function for trimming audio files.

2. `main(audio_file)`
   Main function to execute the trimming process.

### Configurable Parameters

1. Parameters for `trim_audio` function:
   - `input_file`: Path to the input audio file
   - `output_file`: Path to the output (trimmed) audio file
   - `threshold` (default: 0.1): Volume threshold
   - `duration` (default: 1.0): Duration of audio to trim (in seconds)

2. Parameters for `main` function:
   - `file`: Path to the audio file to process

### Script

```python
import wave
import numpy as np
from scipy.io import wavfile

def trim_audio(input_file, output_file, threshold=0.1, duration=1.0):
    # Load the WAV file
    try:
        rate, data = wavfile.read(input_file)
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        return
    except:
        print(f"Error: A problem occurred while reading the input file '{input_file}'.")
        return

    # Convert data to float32 type and normalize
    data = data.astype(np.float32) / np.iinfo(data.dtype).max

    # If stereo, take the average of the channels
    if len(data.shape) > 1:
        data = np.mean(data, axis=1)

    # Find the first index exceeding the threshold
    threshold_indices = np.where(np.abs(data) > threshold)[0]
    if len(threshold_indices) == 0:
        print(f"Warning: No volume exceeding the threshold {threshold} was found. Maximum volume of the entire audio: {np.max(np.abs(data))}")
        return
    threshold_index = threshold_indices[0]

    # Extract data from the start position for the specified duration
    end_index = min(threshold_index + int(rate * duration), len(data))
    trimmed_data = data[threshold_index:end_index]

    # Save as a new WAV file
    trimmed_data = (trimmed_data * 32767).astype(np.int16)
    try:
        wavfile.write(output_file, rate, trimmed_data)
        print(f"Audio cut from '{input_file}' to '{output_file}'.")
        print(f"Cut start position: {threshold_index / rate:.2f} seconds")
    except:
        print(f"Error: A problem occurred while writing the output file '{output_file}'.")

def main(audio_file):
    input_file = audio_file
    output_file = f"trimmed_{audio_file}"
    trim_audio(input_file, output_file, threshold=0.1, duration=1.0)
```

## Usage

1. Install the required libraries:
   ```
   pip install numpy librosa scipy pydub scikit-learn
   ```

2. Prepare the input audio file (e.g., input_audio.wav).

3. Run the script:
   ```
   python spectrogram_based_audio_to_text.py
   ```

## Execution Results

```
Audio cut from 'input_audio.wav' to 'trimmed_input_audio.wav'.
Cut start position: 0.97 seconds
Spectrogram-PCA feature string:
ka/Xz6tcLBgKAAcfQnqov/D/+/GtZyEXJRkREiVLg6zI5+3dm1U2IAsLMD/fsjYML1hvd5nEyM7Ap6SnpIxT
Feature string length: 588
Conversion process completed.
```

## Notes

1. Ensure the input audio file exists.
2. Processing time and result quality may vary with parameter adjustments.
3. Be mindful of hardware resources when processing large amounts of audio data.
4. Complete reconstruction of original audio from spectrograms is difficult due to phase information loss.
5. Noise reduction preprocessing may be effective for recordings in noisy environments.

## Error Handling

Both scripts provide error messages for file not found cases or issues during processing.

## Summary

This script set is an audio processing tool centered on spectrogram-based feature extraction. It leverages the advantages of spectrograms (rich information content, integration of time-frequency information) while improving computational efficiency through PCA-based dimensionality reduction. It can be used as preprocessing for various audio analysis tasks such as speech recognition, speaker identification, and music genre classification. However, care must be taken regarding phase information loss and the impact of background noise. The flexibility to handle various audio inputs and purposes can be achieved by appropriately adjusting parameters.