import json
import numpy as np
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
        # Thresholds tuned for green corruption bottom-heavy
        green_dom_thresh = 1.8  # G > 1.8 * (R+B)/2
        low_var_thresh = 500.0  # Low laplacian var (blurry/corrupt)
        low_entropy_thresh = 5.0
        high_green_thresh = 150  # Absolute high green mean

        b_gr = bottom['green_ratio']
        b_var = bottom['laplacian_var']
        b_ent = bottom['entropy']
        b_gmean = bottom['means'][1]

        # Bottom corrupted if green heavy, low quality, vs top normal
        t_var = top['laplacian_var']
        bottom_corrupt = (
            b_gr > green_dom_thresh and
            b_var < low_var_thresh and
            b_ent < low_entropy_thresh and
            b_gmean > high_green_thresh and
            t_var > b_var * 1.2  # Top sharper
        )
        return bottom_corrupt

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
