import json
import numpy as np
import imagehash
from image_analyzer import ImageAnalyzer
from pathlib import Path

class CorruptionDetector:
    def __init__(self, images_dir: str, bugged_patterns: list = None):
        self.dir = Path(images_dir)
        self.bugged_patterns = bugged_patterns or ['0001_D']
        self.analyzers = {}

    def load_images(self):
        jpgs = list(self.dir.rglob('*.JPG'))
        for jpg in jpgs:
            try:
                analyzer = ImageAnalyzer(str(jpg))
                self.analyzers[str(jpg)] = analyzer.get_full_metrics()
            except Exception as e:
                print(f"Error loading {jpg}: {e}")

    def is_corrupted(self, metrics: dict) -> bool:
        bottom = metrics['bottom']
        top = metrics['top']
        # Generalized for any channel corruption (green/blue/pink/black/gray)
        imbalance_thresh = 4.0  # One channel >> others
        low_var_thresh = 50.0
        low_ent_thresh = 4.0
        low_std_thresh = 10.0
        quality_diff_thresh = 5.0  # top much sharper
        phash_diff_thresh = 10

        # Channel imbalance bottom
        b_imbalance = bottom['channel_imbalance']
        b_var = bottom['laplacian_var']
        b_ent = bottom['entropy']
        b_std_mean = bottom['mean_std']

        # Top-bottom quality diff
        t_var = top['laplacian_var']
        phash_t = imagehash.hex_to_hash(top['phash'])
        phash_b = imagehash.hex_to_hash(bottom['phash'])
        phash_dist = phash_t - phash_b

        # ANY of these = corrupted
        imbalance_issue = b_imbalance > imbalance_thresh
        low_quality = (b_var < low_var_thresh or b_ent < low_ent_thresh or b_std_mean < low_std_thresh)
        quality_diff = t_var > b_var * quality_diff_thresh
        hash_diff = phash_dist > phash_diff_thresh

        corrupted = imbalance_issue or low_quality or (quality_diff and hash_diff)
        return corrupted

    def detect(self):
        self.load_images()
        results = {}
        for path, metrics in self.analyzers.items():
            is_bug = self.is_corrupted(metrics)
            filename = Path(path).name
            results[filename] = {
                'corrupted': is_bug,
                **metrics
            }
        return results

    def save_report(self, filename='report.json'):
        results = self.detect()
        with open(self.dir / filename, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        print(f"Report saved: {self.dir / filename}")
        for fname, data in results.items():
            print(f"{fname}: corrupted={data['corrupted']}")
        return results
