import numpy as np
import cv2

class HSVUtil:
    @staticmethod
    def analyze_hsv_region(region):
        if region.size == 0:
            return {}
        
        # Convert RGB to HSV
        hsv = cv2.cvtColor(region.astype(np.uint8), cv2.COLOR_RGB2HSV)
        
        # HSV means and stds
        h_mean, s_mean, v_mean = np.mean(hsv, axis=(0,1))
        h_std, s_std, v_std = np.std(hsv, axis=(0,1))
        
        # HSV ratios (similar to RGB)
        s_ratio = s_mean / max((h_mean + v_mean)/2, 1e-6)
        v_ratio = v_mean / max((h_mean + s_mean)/2, 1e-6)
        h_ratio = h_mean / max((s_mean + v_mean)/2, 1e-6)
        
        # Dominant HSV channel
        means_list = np.array([h_mean, s_mean, v_mean])
        dominant_chan = np.argmax(means_list)
        chan_names = ['H', 'S', 'V']
        dominant_name = chan_names[dominant_chan]
        imbalance = means_list[dominant_chan] / max(np.sum(means_list) - means_list[dominant_chan], 1e-6)
        
        std_mean = np.mean([h_std, s_std, v_std])
        
        # Entropy on V channel (value/grayscale equivalent)
        v_gray = hsv[:,:,2].astype(np.uint8)
        hist = cv2.calcHist([v_gray], [0], None, [256], [0,256])
        hist = hist / hist.sum()
        entropy = -np.sum(hist * np.log2(hist + 1e-10))
        
        # Laplacian on V for sharpness
        laplacian_var = cv2.Laplacian(v_gray, cv2.CV_64F).var()
        
        return {
            'hsv_means': (float(h_mean), float(s_mean), float(v_mean)),
            'hsv_stds': (float(h_std), float(s_std), float(v_std)),
            'hsv_dominant': dominant_name,
            'hsv_imbalance': float(imbalance),
            'hsv_s_ratio': float(s_ratio),
            'hsv_v_ratio': float(v_ratio),
            'hsv_h_ratio': float(h_ratio),
            'hsv_mean_std': float(std_mean),
            'hsv_entropy': float(entropy),
            'hsv_var': float(laplacian_var)
        }
