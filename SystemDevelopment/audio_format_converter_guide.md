# Python Script for Converting Audio Files Between MP3, WAV, and M4A

## Overview

This Python script is a tool for converting audio files between MP3, WAV, and M4A formats. It uses the Pydub library and ffmpeg to achieve efficient and high-quality conversions.

For information on file size changes during conversion, refer to "[File Size Changes When Converting Audio File Formats (MP3 / WAV / M4A)](https://www.cultivationdata.net/md-to-web.html?md=SystemDevelopment/audio_format_conversion_file_size_changes.md&bc=system-development)".

## Prerequisites

To run this script, you need the following software and libraries:

1. Python
2. Pydub library (a Python audio processing library that simplifies working with audio files)
3. ffmpeg (a powerful multimedia framework for handling audio and video files)

### Installing ffmpeg

- Windows: `choco install ffmpeg` (using Chocolatey) or download from [the official website](https://www.ffmpeg.org/download.html)
- macOS: `brew install ffmpeg` (using Homebrew)
- Linux: `sudo apt-get install ffmpeg` (for Ubuntu/Debian-based systems)

Ensure that ffmpeg is added to your system PATH after installation.

### Installing Pydub

```
pip install pydub
```

## Script Content

```python
from pydub import AudioSegment

def convert_audio(input_file, output_file, input_format, output_format):
    """
    Function to convert audio files between specified formats
    Parameters:
    input_file (str): Path to the input audio file
    output_file (str): Path for the output audio file
    input_format (str): Format of the input file ('mp3', 'wav', 'm4a')
    output_format (str): Format for the output file ('mp3', 'wav', 'm4a')
    """
    try:
        # Load the input file
        audio = AudioSegment.from_file(input_file, format=input_format)
        
        # Export the audio in the specified output format
        audio.export(output_file, format=output_format)
        print(f"Conversion completed: {input_file} ({input_format}) -> {output_file} ({output_format})")
    except Exception as e:
        print(f"An error occurred: {e}")

# Usage examples
if __name__ == "__main__":
    # mp3 -> wav
    convert_audio("input.mp3", "output.wav", "mp3", "wav")
    # wav -> m4a
    convert_audio("input.wav", "output.m4a", "wav", "m4a")
    # m4a -> mp3
    convert_audio("input.m4a", "output.mp3", "m4a", "mp3")
```

## Detailed Functionality

1. Import: The script imports the AudioSegment class from the Pydub library.
2. Conversion Function: `convert_audio(input_file, output_file, input_format, output_format)`
   - Arguments:
     - `input_file`: Path to the source file
     - `output_file`: Path for saving the converted file
     - `input_format`: Format of the source file (mp3, wav, m4a)
     - `output_format`: Format for the converted file (mp3, wav, m4a)
3. Conversion Process:
   - Reads the source file using `AudioSegment.from_file()`
   - Converts and saves using the `export()` method
   - Displays a success message or catches and displays any errors
4. Usage Examples: Provided in the 'if __name__ == "__main__":' block of the script.

## Important Notes

- Both the Pydub library and ffmpeg are required.
- ffmpeg must be correctly added to the system PATH.
- File size may change during conversion.
- Conversion time depends on the file size and length.

## Troubleshooting

1. FileNotFoundError: [Errno 2] No such file or directory: 'ffprobe'
   - Solution: Verify ffmpeg installation and PATH settings
2. Input file not found error
   - Solution: Check if the input file path is correct
3. Output file not generated
   - Solution: Check write permissions for the output directory

## Conclusion

This script is a useful tool for easily converting between MP3, WAV, and M4A file formats. It's particularly helpful in audio processing or speech recognition projects where input format uniformity is required. Combined with ffmpeg, it enables high-quality and efficient audio conversion.

## Bonus: Converting an Entire Directory

For converting multiple files, it's convenient to convert all files in a directory at once. Here's the code for that:

```python
import os
from pydub import AudioSegment

def convert_audio(input_file, output_file, input_format, output_format):
    # ... (same as before)

def convert_directory(input_dir, output_dir, input_format, output_format):
    """
    Function to convert all audio files in a specified directory to a specified format
    This function automates the process of batch converting multiple audio files.
    
    Parameters:
    input_dir (str): Path to the directory containing input audio files
    output_dir (str): Path to the directory for saving output audio files
    input_format (str): Format of the input files ('mp3', 'wav', 'm4a')
    output_format (str): Format for the output files ('mp3', 'wav', 'm4a')
    """
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Check all files in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith(f".{input_format}"):
            input_path = os.path.join(input_dir, filename)
            output_filename = os.path.splitext(filename)[0] + f".{output_format}"
            output_path = os.path.join(output_dir, output_filename)
            convert_audio(input_path, output_path, input_format, output_format)

if __name__ == "__main__":
    input_directory = "./input_audio"  # Specify input directory path
    output_directory = "./output_audio"  # Specify output directory path
    input_format = "m4a"  # Specify input format
    output_format = "wav"  # Specify output format
    convert_directory(input_directory, output_directory, input_format, output_format)
```

This enhanced script provides a more comprehensive solution for batch converting audio files in a specified directory, automating the process for multiple files at once.