#!/usr/bin/env python3
"""
Main script to detect corrupted drone photos.
Usage: python main.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pathlib import Path
from corruption_detector import CorruptionDetector
from PIL import Image
import numpy as np
import re

def parse_mrk(mrk_path):
    """
    Simple MRK parser for timestamps matching filenames.
    """
    markers = {}
    with open(mrk_path, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 3 and '[' in parts[2]:
                idx = parts[0]
                timestamp = parts[1]
                markers[idx] = timestamp
    return markers

def main():
    base_dir = Path(__file__).parent.parent  # g:/DCIM/TESTE_FOTO BUGADA
    analyzer_dir = Path(__file__).parent

    # Detect corruption
    detector = CorruptionDetector(base_dir)
    results = detector.save_report(str(analyzer_dir / 'detection_report.json'))

    # Parse MRK for anomalies (simple: check gaps)
    mrk_path = base_dir / 'DJI_202604061403_002_B01' / 'DJI_202604061403_002_B01_Timestamp.MRK'
    if mrk_path.exists():
        markers = parse_mrk(mrk_path)
        print("\nMRK Timestamps:")
        print(markers)
        # Simple anomaly: if timestamps far apart for consecutive photos
        times = sorted([float(t) for t in markers.values()])
        gaps = np.diff(times)
        print(f"Time gaps: {gaps}")
        if np.any(gaps > 10):  # >10s gap anomaly?
            print("Potential timestamp anomaly detected!")

    print("\nAnalysis complete. Check detection_report.json for full metrics.")

if __name__ == "__main__":
    main()
