import json
import numpy as np
import imagehash
from image_analyzer import ImageAnalyzer
from photo_sector import PhotoSector
from pathlib import Path

class CorruptionDetector:
    def __init__(self, images_dir: str, bugged_patterns=None):
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
        # Average bottom quadrants
        bl, br = metrics['bottom_left'], metrics['bottom_right']
        b_imbalance = (bl['channel_imbalance'] + br['channel_imbalance']) / 2
        b_var = (bl['laplacian_var'] + br['laplacian_var']) / 2
        b_ent = (bl['entropy'] + br['entropy']) / 2
        b_std_mean = (bl['mean_std'] + br['mean_std']) / 2
        
        # Average top quadrants
        tl, tr = metrics['top_left'], metrics['top_right']
        t_var = (tl['laplacian_var'] + tr['laplacian_var']) / 2
        
        # Thresholds
        imbalance_thresh = 4.0
        low_var_thresh = 50.0
        low_ent_thresh = 4.0
        low_std_thresh = 10.0
        quality_diff_thresh = 5.0
        
        # Check conditions
        imbalance_issue = b_imbalance > imbalance_thresh
        low_quality = b_var < low_var_thresh or b_ent < low_ent_thresh or b_std_mean < low_std_thresh
        quality_diff = t_var > b_var * quality_diff_thresh
        
        return imbalance_issue or low_quality or quality_diff

    def detect(self):
        self.load_images()
        results = {}
        for path, metrics in self.analyzers.items():
            is_bug = self.is_corrupted(metrics)
            filename = Path(path).name
            # Create PhotoSector for each region
            tl_sector = PhotoSector(metrics['top_left'])
            tr_sector = PhotoSector(metrics['top_right'])
            bl_sector = PhotoSector(metrics['bottom_left'])
            br_sector = PhotoSector(metrics['bottom_right'])
            
            results[filename] = {
                'corrupted': is_bug,
                'top_left': tl_sector.to_json(),
                'top_right': tr_sector.to_json(),
                'bottom_left': bl_sector.to_json(),
                'bottom_right': br_sector.to_json(),
                'path': metrics['path'],
                'exif': metrics['exif'],
                'height': metrics['height'],
                'width': metrics['width']
            }
        return results

    def save_report(self, filename='detection_report.json'):
        results = self.detect()
        report_path = self.dir / filename
        with open(report_path, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        print(f"Report saved: {report_path}")
        for fname, data in results.items():
            print(f"{fname}: corrupted={data['corrupted']}")
        return results
