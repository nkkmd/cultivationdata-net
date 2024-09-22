# File Size Changes When Converting Audio File Formats (MP3 / WAV / M4A)

**Important Note:** File size changes can vary significantly depending on factors such as the original file's bitrate, sampling rate, conversion settings, and audio complexity. The following explanations demonstrate general trends, and actual results may differ substantially.

## Table of Contents

1. MP3 -> WAV
2. WAV -> MP3
3. M4A -> WAV
4. WAV -> M4A
5. MP3 -> M4A
6. M4A -> MP3

### 1. MP3 -> WAV

- **Trend:** File size increases
- **Reason:** WAV is an uncompressed format, so expanding MP3's compressed data results in larger files
- **Range of change:** Varies greatly depending on the original MP3's bitrate
  - Example: 128 kbps MP3 -> WAV, about 5-7 times increase
  - Example: 320 kbps MP3 -> WAV, about 2-3 times increase

### 2. WAV -> MP3

- **Trend:** File size decreases
- **Reason:** MP3 is a compressed format, so WAV data is compressed
- **Range of change:** Heavily dependent on the set MP3 bitrate
  - Example: WAV -> 128 kbps MP3, reduces to about 1/10th of original size
  - Example: WAV -> 320 kbps MP3, reduces to about 1/4th of original size

### 3. M4A -> WAV

- **Trend:** File size increases
- **Reason:** M4A (AAC) is a compressed format, WAV is uncompressed
- **Range of change:** Varies greatly depending on the original M4A's bitrate
  - Example: 128 kbps AAC -> WAV, about 6-8 times increase
  - Example: 256 kbps AAC -> WAV, about 3-4 times increase

### 4. WAV -> M4A

- **Trend:** File size decreases
- **Reason:** M4A (AAC) uses a compressed format
- **Range of change:** Heavily dependent on the set AAC bitrate
  - Example: WAV -> 128 kbps AAC, reduces to about 1/8th of original size
  - Example: WAV -> 256 kbps AAC, reduces to about 1/4th of original size

### 5. MP3 -> M4A

- **Trend:** File size change heavily depends on settings
- **Reason:** Both are compressed formats but use different compression algorithms
- **Range of change:** Depends on the relationship between original MP3 and set AAC bitrates
  - Example: When converting at equivalent bitrates, about ±10% change
  - Example: Low bitrate MP3 to high bitrate AAC conversion results in an increase
  - Example: High bitrate MP3 to low bitrate AAC conversion results in a decrease

### 6. M4A -> MP3

- **Trend:** File size change heavily depends on settings
- **Reason:** Both are compressed formats but use different compression algorithms
- **Range of change:** Depends on the relationship between original AAC and set MP3 bitrates
  - Example: When converting at equivalent bitrates, about ±10% change
  - Example: Low bitrate AAC to high bitrate MP3 conversion results in an increase
  - Example: High bitrate AAC to low bitrate MP3 conversion results in a decrease

## Additional Considerations:

1. **Audio complexity:** Complex music or audio with many frequencies may have reduced compression efficiency, potentially resulting in larger file sizes than expected.

2. **Sampling rate:** Higher sampling rates (e.g., 44.1 kHz vs 22.05 kHz) increase file size.

3. **Number of channels:** Stereo (2 channels) is about twice the size of mono (1 channel).

4. **Encoder efficiency:** Different software or libraries may produce slightly different sizes even with the same settings.

The actual conversion results are determined by a combination of these factors. If you have specific requirements, it's recommended to perform conversion tests with a small sample.