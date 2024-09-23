Certainly. I'll translate the PDF content into English and format it in Markdown, ensuring that the technical content is clear and comprehensible. Here's the translation:

# MFCC Analysis-based Similar Audio Detection System using Python

## Overview

This tool consists of two Python scripts:

1. `mfcc_based_audio_similarity_analyzer.py`
   Performs similarity analysis based on the MFCC (Mel-frequency cepstral coefficients) of audio files.

2. `wav_volume_based_trimmer_dir.py`
   Trims WAV files based on volume.

## Terminology

- **Reference files**: Known audio files used as a basis for comparison. These are placed in the `reference_wav_files/original` directory.
- **Target files**: Audio files to be analyzed and compared against the reference files. These are placed in the `target_wav_files/original` directory.
- **MFCC**: Coefficients that represent the features of an audio signal, considering human auditory characteristics.

## Features

- Extract MFCC features from WAV files
- Reduce feature dimensions using Principal Component Analysis (PCA)
- Compare similarity between multiple audio files
- Trim WAV files based on volume
- Batch processing for directories

## Required Libraries

- numpy
- librosa
- scipy
- sklearn
- os
- base64

## Usage

1. Install the required libraries:

```bash
pip install numpy librosa scipy scikit-learn
```

2. Create the following directory structure:

```
.
├── reference_wav_files
│   ├── original    # Directory for reference files
│   └── trimmed     # Directory for trimmed files
├── target_wav_files
│   ├── original    # Directory for target files
│   └── trimmed     # Directory for trimmed files
├── mfcc_based_audio_similarity_analyzer.py
└── wav_volume_based_trimmer_dir.py
```

3. Place the WAV files you want to analyze in `reference_wav_files/original` and `target_wav_files/original`.

4. Run `mfcc_based_audio_similarity_analyzer.py`:

```bash
python mfcc_based_audio_similarity_analyzer.py
```

## Script Details

### 1. mfcc_based_audio_similarity_analyzer.py

This script plays a central role in the similarity analysis of audio files.

```python
import numpy as np
import librosa
import base64
from sklearn.decomposition import PCA
from scipy.spatial.distance import cosine
import os
import wav_volume_based_trimmer_dir

def create_mfcc_features(audio_file):
    y, sr = librosa.load(audio_file, offset=0, duration=1)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)
    return mfcc

def apply_pca(features, n_components=10):
    pca = PCA(n_components=n_components)
    pca_features = pca.fit_transform(features.T).T
    return pca_features

def features_to_feature_string(features):
    flattened = features.flatten()
    normalized = ((flattened - flattened.min()) / (flattened.max() - flattened.min())).astype(np.uint8)
    byte_data = normalized.tobytes()
    base64_str = base64.b64encode(byte_data).decode('utf-8')
    return base64_str

def audio_to_mfcc_pca_feature_string(audio_file):
    mfcc = create_mfcc_features(audio_file)
    pca_features = apply_pca(mfcc)
    feature_string = features_to_feature_string(pca_features)
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
    target_feature = audio_to_mfcc_pca_feature_string(target_file)
    max_similarity = -1
    most_similar_file = None
    for ref_file in reference_files:
        ref_feature = audio_to_mfcc_pca_feature_string(ref_file)
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
    results = batch_compare_with_reference_set(trimmed_reference_dir, trimmed_target_dir)
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

Key functions:
- `create_mfcc_features()`: Extracts MFCC features from an audio file.
- `apply_pca()`: Applies PCA to reduce feature dimensions.
- `features_to_feature_string()`: Converts features to a string format.
- `audio_to_mfcc_pca_feature_string()`: Extracts MFCC features from an audio file, applies PCA, and converts to a string format.
- `compare_audio_features()`: Calculates the similarity between two feature strings.

### 2. wav_volume_based_trimmer_dir.py

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

    # If stereo, take the average of the channels
    if len(data.shape) > 1:
        data = np.mean(data, axis=1)

    # Find the first index that exceeds the threshold
    threshold_indices = np.where(np.abs(data) > threshold)[0]
    if len(threshold_indices) == 0:
        print(f"Warning: No volume exceeding threshold {threshold} found. Overall maximum volume: {np.max(np.abs(data))}")
        return
    threshold_index = threshold_indices[0]

    # Extract data from the start position for the specified duration
    end_index = min(threshold_index + int(rate * duration), len(data))
    trimmed_data = data[threshold_index:end_index]

    # Save as a new WAV file
    trimmed_data = (trimmed_data * 32767).astype(np.int16)
    try:
        wavfile.write(output_file, rate, trimmed_data)
        print(f"Audio trimmed from '{input_file}' to '{output_file}'.")
        print(f"Trim start position: {threshold_index / rate:.2f} seconds")
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
```

## Processing Flow

1. `wav_volume_based_trimmer_dir.py` is called to trim reference and target files.
2. Trimmed files are saved in the `trimmed` subdirectory.
3. MFCC features are extracted from the trimmed files and dimensionality is reduced using PCA.
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

This tool has several parameters that can be adjusted to fine-tune performance and results:

1. Similarity judgment threshold (`threshold` in `compare_audio_features` function)
2. MFCC feature extraction parameters (`n_mfcc` in `create_mfcc_features` function)
3. PCA dimension number (`n_components` in `apply_pca` function)
4. Audio trimming parameters (`threshold` and `duration` in `trim_audio` function)

## Notes

- Input files must be in WAV format.
- Processing time varies depending on file size and number.
- Ensure sufficient disk space, as trimmed files will be generated additionally.
- PCA dimensionality reduction may lose some information. If very fine differences need to be detected, reconsider using PCA or adjust the `n_components` value.

This tool allows you to efficiently find similar audio files among a large number of files. MFCC analysis considers human auditory characteristics, enabling evaluation of audio similarity in a way close to human perception.

---
- Created: 2024-09-23
- Updated: 2024-09-23