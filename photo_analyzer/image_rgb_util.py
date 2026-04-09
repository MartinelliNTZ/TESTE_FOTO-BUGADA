import numpy as np
import cv2
import imagehash
from PIL import Image

class ImageRGBUtil:
    @staticmethod
    def analyze_color_region(region):
        if region.size == 0:
            return {}
        
        # RGB stats
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
        
        # Laplacian variance (sharpness)
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        
        # Perceptual hash
        pil_region = Image.fromarray(region.astype(np.uint8))
        phash = imagehash.phash(pil_region)
        
        # Dominant channel
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
