import numpy as np
import cv2
import imagehash
from PIL import Image
from hsv_util import HSVUtil

class ImageRGBUtil:
    @staticmethod
    def split_regions(image):
        h, w = image.shape[:2]
        h2, w2 = h // 2, w // 2
        tl = image[0:h2, 0:w2]
        tr = image[0:h2, w2:w]
        bl = image[h2:h, 0:w2]
        br = image[h2:h, w2:w]
        return {'top_left': tl, 'top_right': tr, 'bottom_left': bl, 'bottom_right': br}

    @staticmethod
    def analyze_color_region(region):
        if region.size == 0:
            return {}
        
        # RGB completo
        r_mean, g_mean, b_mean = np.mean(region, axis=(0,1))
        r_std, g_std, b_std = np.std(region, axis=(0,1))
        
        green_ratio = g_mean / max((r_mean + b_mean)/2, 1e-6)
        red_ratio = r_mean / max((g_mean + b_mean)/2, 1e-6)
        blue_ratio = b_mean / max((r_mean + g_mean)/2, 1e-6)
        
        gray = np.mean(region, axis=2).astype(np.uint8)
        hist = cv2.calcHist([gray], [0], None, [256], [0,256])
        hist = hist / hist.sum()
        entropy = -np.sum(hist * np.log2(hist + 1e-10))
        
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        
        pil_region = Image.fromarray(region.astype(np.uint8))
        phash = imagehash.phash(pil_region)
        
        means_list = np.array([r_mean, g_mean, b_mean])
        dominant_chan = np.argmax(means_list)
        chan_names = ['R', 'G', 'B']
        dominant_name = chan_names[dominant_chan]
        imbalance = means_list[dominant_chan] / max(np.sum(means_list) - means_list[dominant_chan], 1e-6)
        
        std_mean = np.mean([r_std, g_std, b_std])
        
        rgb_data = {
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
        
        # HSV
        hsv_data = HSVUtil.analyze_hsv_region(region)
        rgb_data.update(hsv_data)
        
        return rgb_data

    @staticmethod
    def get_full_metrics(image, path, exif, height, width):
        regions = ImageRGBUtil.split_regions(image)
        metrics = {
            'path': path,
            'exif': exif,
            'height': height,
            'width': width
        }
        
        for name, region in regions.items():
            metrics[name] = ImageRGBUtil.analyze_color_region(region)
        
        metrics['overall'] = ImageRGBUtil.analyze_color_region(image)
        return metrics
