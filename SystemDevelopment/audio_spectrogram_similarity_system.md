# Audio Spectrogram Analysis-based Similar Sound Detection System using Python

## Overview

This tool consists of two Python scripts:

1. `spectrogram-based_audio_similarity_analyzer.py`
   - Performs similarity analysis based on audio file spectrograms.
2. `wav_volume_based_trimmer_dir.py`
   - Trims WAV files based on volume.

## Terminology

- Reference files: Known audio files used as a basis for comparison. These are placed in the `reference_wav_files/original` directory.
- Target files: Audio files to be analyzed and compared with reference files. These are placed in the `target_wav_files/original` directory.

## Features

- Generate spectrograms from WAV files and extract features
- Compare similarity between multiple audio files
- Trim WAV files based on volume
- Batch processing at directory level

## Required Libraries

- numpy
- librosa
- scipy
- os

## Usage

1. Install the required libraries:
   ```
   pip install numpy librosa scipy
   ```

2. Create the following directory structure:
   ```
   .
   ├── reference_wav_files
   │   ├── original  # Directory for reference files
   │   └── trimmed   # Directory for trimmed files
   ├── target_wav_files
   │   ├── original  # Directory for target files
   │   └── trimmed   # Directory for trimmed files
   ├── spectrogram-based_audio_similarity_analyzer.py
   └── wav_volume_based_trimmer_dir.py
   ```

3. Place WAV files for analysis in `reference_wav_files/original` and `target_wav_files/original`.

4. Run `spectrogram-based_audio_similarity_analyzer.py`:
   ```
   python spectrogram-based_audio_similarity_analyzer.py
   ```

## Script Details

1. spectrogram-based_audio_similarity_analyzer.py

This script plays a central role in the similarity analysis of audio files.

```python
import numpy as np
import librosa
import base64
from scipy.spatial.distance import cosine
import os
import wav_volume_based_trimmer_dir

def create_spectrogram_features(audio_file, n_mels=128, n_fft=2048, hop_length=512):
    y, sr = librosa.load(audio_file, offset=0, duration=1)
    spectrogram = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=n_mels, n_fft=n_fft, hop_length=hop_length)
    spectrogram_db = librosa.power_to_db(spectrogram, ref=np.max)
    return spectrogram_db

def features_to_feature_string(features):
    flattened = features.flatten()
    normalized = ((flattened - flattened.min()) / (flattened.max() - flattened.min()) * 255).astype(np.uint8)
    byte_data = normalized.tobytes()
    base64_str = base64.b64encode(byte_data).decode('utf-8')
    return base64_str

def audio_to_spectrogram_feature_string(audio_file):
    spectrogram = create_spectrogram_features(audio_file)
    feature_string = features_to_feature_string(spectrogram)
    return feature_string

def feature_string_to_features(feature_string):
    byte_data = base64.b64decode(feature_string)
    normalized = np.frombuffer(byte_data, dtype=np.uint8)
    features = normalized.astype(float) / 255
    return features

def compare_audio_features(feature_string1, feature_string2, threshold=0.1):
    features1 = feature_string_to_features(feature_string1)
    features2 = feature_string_to_features(feature_string2)
    similarity = 1 - cosine(features1, features2)
    return similarity >= 1 - threshold, similarity

def compare_with_reference_set(reference_files, target_file, threshold=0.1):
    target_feature = audio_to_spectrogram_feature_string(target_file)
    max_similarity = -1
    most_similar_file = None
    for ref_file in reference_files:
        ref_feature = audio_to_spectrogram_feature_string(ref_file)
        is_similar, similarity = compare_audio_features(ref_feature, target_feature, threshold)
        if similarity > max_similarity:
            max_similarity = similarity
            most_similar_file = ref_file
    is_similar = max_similarity >= (1 - threshold)
    return most_similar_file, max_similarity, is_similar

def batch_compare_with_reference_set(reference_dir, target_dir, threshold=0.1):
    reference_files = [os.path.join(reference_dir, f) for f in os.listdir(reference_dir) if f.lower().endswith('.wav')]
    target_files = [os.path.join(target_dir, f) for f in os.listdir(target_dir) if f.lower().endswith('.wav')]
    results = []
    for target_file in target_files:
        most_similar, similarity, is_similar = compare_with_reference_set(reference_files, target_file, threshold)
        results.append({
            'target_file': target_file,
            'most_similar_reference': most_similar,
            'similarity': similarity,
            'is_similar': is_similar
        })
    return results

if __name__ == "__main__":
    reference_dir = "./reference_wav_files"
    target_dir = "./target_wav_files"
    wav_volume_based_trimmer_dir.main(reference_dir)
    wav_volume_based_trimmer_dir.main(target_dir)
    trimmed_reference_dir = f"{reference_dir}/trimmed"
    trimmed_target_dir = f"{target_dir}/trimmed"
    results = batch_compare_with_reference_set(trimmed_reference_dir, trimmed_target_dir, threshold=0.1)

    if not results:
        print("---")
        print("No comparisons were made. Please check if there are valid .wav files in both directories.")
    else:
        for result in results:
            print("---")
            print(f"Target file: {result['target_file']}")
            print(f"Most similar reference file: {result['most_similar_reference']}")
            print(f"Similarity: {result['similarity']:.4f}")
            print(f"Similarity judgment: {'Similar' if result['is_similar'] else 'Not similar'}")
```

2. wav_volume_based_trimmer_dir.py

This script provides functionality to trim WAV files based on volume.

```python
import os
import wave
import numpy as np
from scipy.io import wavfile

def trim_audio(input_file, output_file, threshold=0.1, duration=1.0):
    # Read the WAV file
    try:
        rate, data = wavfile.read(input_file)
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        return
    except:
        print(f"Error: Problem occurred while reading input file '{input_file}'.")
        return

    # Convert data to float32 type and normalize
    data = data.astype(np.float32) / np.iinfo(data.dtype).max

    # If stereo, take the average of channels
    if len(data.shape) > 1:
        data = np.mean(data, axis=1)

    # Find the first index exceeding the threshold
    threshold_indices = np.where(np.abs(data) > threshold)[0]
    if len(threshold_indices) == 0:
        print(f"Warning: No volume exceeding threshold {threshold} was found. Maximum volume of the entire audio: {np.max(np.abs(data))}")
        return
    threshold_index = threshold_indices[0]

    # Extract data for the specified duration from the start position
    end_index = min(threshold_index + int(rate * duration), len(data))
    trimmed_data = data[threshold_index:end_index]

    # Save as a new WAV file
    trimmed_data = (trimmed_data * 32767).astype(np.int16)
    try:
        wavfile.write(output_file, rate, trimmed_data)
        print(f"Audio trimmed from '{input_file}' to '{output_file}'.")
        print(f"Trimming start position: {threshold_index / rate:.2f} seconds")
    except:
        print(f"Error: Problem occurred while writing output file '{output_file}'.")

def process_directory(input_dir, output_dir, threshold=0.1, duration=1.0):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Process all WAV files in the input directory
    for filename in os.listdir(input_dir):
        if filename.lower().endswith('.wav'):
            input_path = os.path.join(input_dir, filename)
            output_filename = f"trimmed_{filename}"
            output_path = os.path.join(output_dir, output_filename)
            print(f"Processing: {filename}")
            trim_audio(input_path, output_path, threshold, duration)

def main(dir):
    input_directory = f"{dir}/original"
    output_directory = f"{dir}/trimmed"
    process_directory(input_directory, output_directory, threshold=0.1, duration=1.0)

if __name__ == "__main__":
    main("./reference_wav_files")
    main("./target_wav_files")
```

## Process Flow

1. `wav_volume_based_trimmer_dir.py` is called to trim reference and target files.
2. Trimmed files are saved in the `trimmed` subdirectory.
3. Similarity analysis is performed using the trimmed files.
4. For each target file, the most similar reference file, similarity score, and similarity judgment are output.

## Output Example

```
---
Target file: ./target_wav_files/trimmed/trimmed_target1.wav
Most similar reference file: ./reference_wav_files/trimmed/trimmed_ref2.wav
Similarity: 0.9876
Similarity judgment: Similar
```

## Customization

This tool has several parameters that can be adjusted to fine-tune performance and results. Here are the main customizable parameters and their effects:

1. Similarity judgment threshold (threshold)
   - In the `compare_audio_features` function:
     ```python
     def compare_audio_features(feature_string1, feature_string2, threshold=0.1):
     ```
   - Purpose: Determines the minimum similarity for two audio files to be considered "similar".
   - Adjustment:
     - Decrease (e.g., 0.05) for stricter similarity judgment.
     - Increase (e.g., 0.2) for more lenient similarity judgment.
   - Impact: Balances false positives and false negatives in similarity detection.

2. Spectrogram generation parameters
   - In the `create_spectrogram_features` function:
     ```python
     def create_spectrogram_features(audio_file, n_mels=128, n_fft=2048, hop_length=512):
     ```
   - `n_mels`: Number of Mel filter banks
     - Purpose: Controls frequency resolution of the spectrogram.
     - Adjustment: Increase (e.g., 256) for more detailed frequency information, decrease (e.g., 64) for coarser information.
     - Impact: Higher values allow more detailed analysis but increase computational cost.

   - `n_fft`: Size of the FFT window
     - Purpose: Controls the trade-off between time and frequency resolution.
     - Adjustment: Increase (e.g., 4096) for better frequency resolution, decrease (e.g., 1024) for better time resolution.
     - Impact:
       - Larger values are suitable for capturing detailed frequency differences. This is useful for analyzing subtle differences in speakers' voices, environmental sounds, or acoustically complex signals.
       - Smaller values are better for accurately capturing temporal changes. This is useful for detecting sudden sound changes, short voice commands, or precise onset/offset times of sounds.
     - Use cases:
       - Speaker identification: Use larger values to analyze individual speaker characteristics in more detail.
       - Environmental sound classification: Use moderate values to capture features of various environmental sounds equally.
       - Voice command recognition: Use smaller values to accurately capture temporal features of short voice commands.

   - `hop_length`: Frame advance step
     - Purpose: Controls time resolution of the spectrogram.
     - Adjustment: Decrease (e.g., 256) for finer time resolution, increase (e.g., 1024) for coarser resolution.
     - Impact: Smaller values capture more detailed temporal information but increase computational cost and feature size.

3. Audio trimming parameters
   - In the `trim_audio` function:
     ```python
     def trim_audio(input_file, output_file, threshold=0.1, duration=1.0):
     ```
   - `threshold`: Volume threshold for determining trimming start point
     - Purpose: Controls sensitivity when removing silent parts.
     - Adjustment: Decrease (e.g., 0.05) to consider softer sounds as start points, increase (e.g., 0.2) to only consider louder sounds.
     - Impact: Choose larger values for audio with background noise, smaller values for quiet environments.

   - `duration`: Length of trimmed audio (in seconds)
     - Purpose: Determines the length of audio used for analysis.
     - Adjustment: Increase (e.g., 2.0) to analyze longer audio, decrease (e.g., 0.5) for shorter audio.
     - Impact: Longer values include more information but increase computational cost. Choose smaller values to capture features of short sounds.

By adjusting these parameters, you can optimize the tool's behavior for various types of audio data and analysis purposes. The optimal values depend on the nature of your audio data and the desired accuracy of results, so experimental adjustment is recommended.

## Notes

- Input files must be in WAV format.
- Processing time varies depending on file size and number.
- Ensure sufficient disk space, as trimmed files will be generated in addition to original files.

This tool allows efficient identification of similar audio files among a large number of audio files.

---
- Created: 2024-09-23
- Updated: 2024-09-23