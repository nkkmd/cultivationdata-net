# Summary of Image Comparison Techniques

1. Histogram Comparison
2. SSIM (Structural Similarity Index)
3. MSE (Mean Squared Error)
4. PSNR (Peak Signal-to-Noise Ratio)
5. FSIM (Feature Similarity Index)
6. LPIPS (Learned Perceptual Image Patch Similarity)
7. Cosine Similarity
8. Perceptual Hash
9. Feature Point Matching (SIFT, SURF, ORB)

## 1. Histogram Comparison

**Overview:** A method to compare color distribution in images

**Characteristics:**
- Fast computation and simple implementation
- Invariant to rotation and scale changes
- Ignores spatial information, thus disregarding image structure

**Suitable for comparing:**
- Images of the same scene with different exposures
- Pre and post color correction images

**Python Implementation:** Feasible
- Easily implemented using the OpenCV library
- Utilizes the `cv2.compareHist()` function

## 2. SSIM (Structural Similarity Index)

**Overview:** Evaluates image similarity considering luminance, contrast, and structure

**Characteristics:**
- Provides evaluation close to human perception
- Relatively robust against noise

**Suitable for:**
- Evaluating image compression quality
- Assessing performance of image processing algorithms

**Python Implementation:** Feasible
- Uses the `skimage.metrics.structural_similarity` function from the scikit-image library

## 3. MSE (Mean Squared Error)

**Overview:** Calculates the average of squared differences between pixels

**Characteristics:**
- Extremely simple to implement
- Fast computation

**Suitable for:**
- Evaluating noise levels
- Detecting subtle changes in images

**Python Implementation:** Feasible
- Easily implemented using NumPy
- Can be computed with `np.mean((image1 - image2) ** 2)`

## 4. PSNR (Peak Signal-to-Noise Ratio)

**Overview:** Signal-to-noise ratio based on MSE

**Characteristics:**
- Widely used for objective quality assessment of images

**Suitable for:**
- Evaluating compression quality of images and videos
- Assessing performance of image restoration algorithms

**Python Implementation:** Feasible
- Uses the `skimage.metrics.peak_signal_noise_ratio` function from the scikit-image library
- Can also be directly calculated from MSE using NumPy

## 5. FSIM (Feature Similarity Index)

**Overview:** Calculates similarity considering phase congruency and gradient magnitude

**Characteristics:**
- Emphasizes edges and distinctive structures
- Can be more accurate than SSIM in some cases

**Suitable for:**
- Comparing images rich in texture
- Evaluating quality of medical images

**Python Implementation:** Partially feasible
- No implementation in standard libraries, but open-source implementations available on GitHub
- Can be custom-implemented using NumPy and SciPy

## 6. LPIPS (Learned Perceptual Image Patch Similarity)

**Overview:** Calculates perceptual similarity using deep learning

**Characteristics:**
- Evaluation very close to human perception
- Depends on training data

**Suitable for:**
- Evaluating quality of generated images
- Assessing image editing tasks

**Python Implementation:** Feasible
- Uses the official Python package "lpips"
- PyTorch-based implementation

## 7. Cosine Similarity

**Overview:** Compares the angle between vectorized images

**Characteristics:**
- Not affected by vector magnitude
- Suitable for high-dimensional data comparison

**Suitable for:**
- Similarity calculation in image retrieval systems
- Similarity calculation in facial recognition systems

**Python Implementation:** Feasible
- Easily implemented using NumPy or SciPy
- Uses the `scipy.spatial.distance.cosine()` function

## 8. Perceptual Hash

**Overview:** Compares images by hashing their features

**Characteristics:**
- Enables fast comparison
- Robust against changes in scale and aspect ratio

**Suitable for:**
- Detecting duplicates in large image databases
- Detecting copyright infringement

**Python Implementation:** Feasible
- Uses the ImageHash library
- Utilizes functions like `imagehash.average_hash()`, `imagehash.phash()`, `imagehash.dhash()`

## 9. Feature Point Matching (SIFT, SURF, ORB)

**Overview:** Extracts and matches local features from images

**Characteristics:**
- Robust against rotation, scale, and viewpoint changes
- Capable of detecting partial matches

**Suitable for:**
- Generating panoramic images
- Object recognition and tracking

**Python Implementation:** Feasible
- Uses the OpenCV library
  - SIFT: `cv2.SIFT_create()`
  - SURF: `cv2.xfeatures2d.SURF_create()` in OpenCV 3.x, removed in latest versions due to patent issues
  - ORB: `cv2.ORB_create()`

---
- Created: 2024-09-12
- Updated: 2024-09-12