# Image Similarity Comparison using Python

## Overview
This Python script compares two image files and calculates their similarity using two methods: histogram comparison and Structural Similarity Index (SSIM).

## Prerequisites
- Python 3.x
- Required Python libraries:
  - OpenCV (cv2)
  - NumPy
  - scikit-image

You can install these libraries using the following command:
```
pip install opencv-python numpy scikit-image
```

## Script Contents
The script provides the following main functionalities:
1. Load two image files
2. Resize images
3. Convert images to grayscale
4. Calculate histograms and compare them
5. Calculate SSIM (Structural Similarity Index)

```python
import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim

def compare_images(image1_path, image2_path):
    # Load images
    img1 = cv2.imread(image1_path)
    img2 = cv2.imread(image2_path)

    # Resize images to match
    height = min(img1.shape[0], img2.shape[0])
    width = min(img1.shape[1], img2.shape[1])
    img1 = cv2.resize(img1, (width, height))
    img2 = cv2.resize(img2, (width, height))

    # Convert to grayscale
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # Calculate histograms
    hist1 = cv2.calcHist([gray1], [0], None, [256], [0, 256])
    hist2 = cv2.calcHist([gray2], [0], None, [256], [0, 256])

    # Normalize histograms
    cv2.normalize(hist1, hist1, 0, 1, cv2.NORM_MINMAX)
    cv2.normalize(hist2, hist2, 0, 1, cv2.NORM_MINMAX)

    # Compare histograms
    similarity = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)

    # Calculate SSIM (Structural Similarity)
    ssim_score = ssim(gray1, gray2)

    return similarity, ssim_score

# Usage example
image1_path = 'path/to/image1.jpg'
image2_path = 'path/to/image2.jpg'
hist_similarity, ssim_score = compare_images(image1_path, image2_path)
print(f"Histogram similarity: {hist_similarity:.2f}")
print(f"SSIM score: {ssim_score:.2f}")
```

## Histogram Comparison
Histogram comparison measures the similarity of brightness distribution in images. The current implementation uses the correlation coefficient method (cv2.HISTCMP_CORREL).

- Value range: -1 to 1
- Interpretation:
  - Close to 1: High similarity (strong positive correlation)
  - Close to 0: No correlation (low similarity)
  - Close to -1: Strong inverse correlation (opposite trend)
- Features:
  - Compares overall brightness distribution, ignoring fine structural differences
  - Relatively fast computation
  - Somewhat robust against image rotation and small deformations

## SSIM (Structural Similarity)
SSIM measures the structural similarity of images. It considers three elements: luminance, contrast, and structure.

- Value range: -1 to 1
- Interpretation:
  - Close to 1: High similarity (almost identical images)
  - Close to 0: Low similarity
  - Close to -1: Inverse structure (rare in practice)
- Features:
  - Similarity measurement based on the human visual system
  - Can detect local structural differences
  - Evaluates the impact of noise, blur, compression artifacts, etc.

## Usage
1. Create a script file (e.g., `image_similarity_comparison.py`) and paste the provided code.
2. Set the `image1_path` and `image2_path` variables in the script to the paths of the images you want to compare.
3. Run the script from the command line:
```
python image_similarity_comparison.py
```
4. The results will be displayed, showing the histogram similarity and SSIM score.

## Process Flow
1. Load two image files
2. Resize images to match the smaller size
3. Convert images to grayscale
4. Calculate histogram for each image
5. Normalize histograms
6. Perform histogram comparison
7. Calculate SSIM (Structural Similarity)
8. Return results

## Cautions
- Ensure that image file paths are correctly set.
- Processing large images may increase memory usage.
- Additional libraries may be required depending on the image format.

## Troubleshooting
1. Error: ImportError: No module named 'cv2'
   - Solution: Run `pip install opencv-python` to install OpenCV.
   - Explanation: This error occurs when the OpenCV library is not installed in your Python environment.

2. Error: ImportError: No module named 'skimage'
   - Solution: Run `pip install scikit-image` to install scikit-image.
   - Explanation: This error appears when the scikit-image library, which is required for SSIM calculation, is missing.

3. Error: FileNotFoundError: [Errno 2] No such file or directory: 'image1.jpg'
   - Solution: Verify that the image file path is correct and use absolute paths if necessary.
   - Explanation: This error occurs when Python cannot find the specified image file at the given path.

## Additional Feature: Processing Image Data Retrieved with requests.get
This section demonstrates how to modify the script to process images retrieved from URLs using the `requests` library. It allows for comparison of images directly from web sources without downloading them first.

```python
import cv2
import numpy as np
import requests
from skimage.metrics import structural_similarity as ssim

def compare_images_from_urls(image1_url, image2_url):
    # Fetch image from URL
    def get_image_from_url(url):
        response = requests.get(url)
        image_array = np.frombuffer(response.content, np.uint8)
        return cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    img1 = get_image_from_url(image1_url)
    img2 = get_image_from_url(image2_url)

    # Resize images to match
    height = min(img1.shape[0], img2.shape[0])
    width = min(img1.shape[1], img2.shape[1])
    img1 = cv2.resize(img1, (width, height))
    img2 = cv2.resize(img2, (width, height))

    # Convert to grayscale
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # Calculate histograms
    hist1 = cv2.calcHist([gray1], [0], None, [256], [0, 256])
    hist2 = cv2.calcHist([gray2], [0], None, [256], [0, 256])

    # Normalize histograms
    cv2.normalize(hist1, hist1, 0, 1, cv2.NORM_MINMAX)
    cv2.normalize(hist2, hist2, 0, 1, cv2.NORM_MINMAX)

    # Compare histograms
    similarity = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)

    # Calculate SSIM (Structural Similarity)
    ssim_score = ssim(gray1, gray2)

    return similarity, ssim_score

# Usage example
image1_url = 'https://example.com/image1.jpg'
image2_url = 'https://example.com/image2.jpg'
hist_similarity, ssim_score = compare_images_from_urls(image1_url, image2_url)
print(f"Histogram similarity: {hist_similarity:.2f}")
print(f"SSIM score: {ssim_score:.2f}")
```

---
- Created: 2024-9-23
- Updated: 2024-9-23