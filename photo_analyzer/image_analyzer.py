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

    def split_regions(self):
        h, w = self.image.shape[:2]
        h2, w2 = h // 2, w // 2
        tl = self.image[0:h2, 0:w2]  # top_left
        tr = self.image[0:h2, w2:w]  # top_right
        bl = self.image[h2:h, 0:w2]  # bottom_left
        br = self.image[h2:h, w2:w]  # bottom_right
        return {'top_left': tl, 'top_right': tr, 'bottom_left': bl, 'bottom_right': br}

    def analyze_region(self, region):
        if region.size == 0:
            return {}
        r_mean, g_mean, b_mean = np.mean(region, axis=(0,1))
        r_std, g_std, b_std = np.std(region, axis=(0,1))
        # Ratios
        green_ratio = g_mean / max((r_mean + b_mean)/2, 1e-6)
        red_ratio = r_mean / max((g_mean + b_mean)/2, 1e-6)
        blue_ratio = b_mean / max((r_mean + g_mean)/2, 1e-6)
        # Entropy
        gray = np.mean(region, axis=2).astype(np.uint8)
        hist = cv2.calcHist([gray], [0], None, [256], [0,256])
        hist = hist / hist.sum()
        entropy = -np.sum(hist * np.log2(hist + 1e-10))
        # Laplacian var
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        # Phash
        pil_region = Image.fromarray(region.astype(np.uint8))
        phash = imagehash.phash(pil_region)
        # Dominant
        means_list = np.array([r_mean, g_mean, b_mean])
        dominant_chan = np.argmax(means_list)
        chan_names = ['R', 'G', 'B']
        dominant_name = chan_names[dominant_chan]
        imbalance = means_list[dominant_chan] / max(np.sum(means_list) - means_list[dominant_chan], 1e-6)
        std_mean = np.mean([r_std, g_std, b_std])
        return {
            'means': (float(r_mean), float(g_mean), float(b_mean)),
            'stds': (float(r_std), float(g_std), float(b_std)),
            'dominant_channel': dominant_name,
            'channel_imbalance': float(imbalance),
            'green_ratio': float(green_ratio),
            'red_ratio': float(red_ratio),
            'blue_ratio': float(blue_ratio),
            'mean_std': float(std_mean),
            'entropy': float(entropy),
            'laplacian_var': float(laplacian_var),
            'phash': str(phash)
        }

    def get_full_metrics(self):
        regions = self.split_regions()
        metrics = {
            'path': self.path,
            'exif': self.exif,
            'height': self.image.shape[0],
            'width': self.image.shape[1]
        }
        for name, region in regions.items():
            metrics[name] = self.analyze_region(region)
        
        # Overall image analysis
        overall = self.analyze_region(self.image)
        metrics['overall'] = overall
        return metrics
