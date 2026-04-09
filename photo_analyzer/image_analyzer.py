import os
from PIL import Image, ExifTags
import numpy as np
import cv2
from skimage import measure
import imagehash
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

class ImageAnalyzer:
    def __init__(self, image_path: str):
        self.path = image_path
        self.image = None
        self.exif = {}
        self._load_image()
        self._extract_exif()

    def _load_image(self):
        self.image = cv2.imread(self.path)
        if self.image is None:
            raise ValueError(f"Could not load image: {self.path}")
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)

    def _extract_exif(self):
        pil_image = Image.open(self.path)
        exifdata = pil_image.getexif()
        for tag_id, value in exifdata.items():
            tag = ExifTags.TAGS.get(tag_id, tag_id)
            self.exif[tag] = value

    def split_regions(self, top_ratio=0.3):
        h, w = self.image.shape[:2]
        top_h = int(h * top_ratio)
        top = self.image[:top_h, :]
        bottom = self.image[top_h:, :]
        return top, bottom

    def analyze_region(self, region):
        if region.size == 0:
            return {}
        # Channel stats
        r_mean, g_mean, b_mean = np.mean(region, axis=(0,1))
        r_std, g_std, b_std = np.std(region, axis=(0,1))
        # Green dominance
        green_ratio = g_mean / max((r_mean + b_mean)/2, 1e-6)
        # Entropy (grayscale)
        gray = np.mean(region, axis=2)
        hist = cv2.calcHist([gray.astype(np.uint8)], [0], None, [256], [0,256])
        hist = hist / hist.sum()
        entropy = -np.sum(hist * np.log2(hist + 1e-10))
        # Laplacian variance (sharpness/blur)
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        # Perceptual hash
        pil_region = Image.fromarray(region.astype(np.uint8))
        phash = imagehash.phash(pil_region)
        return {
            'means': (r_mean, g_mean, b_mean),
            'stds': (r_std, g_std, b_std),
            'green_ratio': green_ratio,
            'entropy': entropy,
            'laplacian_var': laplacian_var,
            'phash': str(phash)
        }

    def get_full_metrics(self):
        top, bottom = self.split_regions()
        return {
            'path': self.path,
            'exif': self.exif,
            'top': self.analyze_region(top),
            'bottom': self.analyze_region(bottom),
            'height': self.image.shape[0],
            'width': self.image.shape[1]
        }
