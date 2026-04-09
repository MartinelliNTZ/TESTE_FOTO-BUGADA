import json
import pandas as pd
from pathlib import Path
import numpy as np

def generate_excel(report_path):
    with open(report_path, 'r') as f:
        results = json.load(f)
    
    rows = []
    for fname, data in results.items():
        top = data['top']
        bottom = data['bottom']
        row = {
            'filename': fname,
            'corrupted': data['corrupted'],
            'size': f"{data['width']}x{data['height']}",
            'top_means_R': top['means'][0],
            'top_means_G': top['means'][1],
            'top_means_B': top['means'][2],
            'top_stds_R': top['stds'][0],
            'top_stds_G': top['stds'][1],
            'top_stds_B': top['stds'][2],
            'top_dominant': top['dominant_channel'],
            'top_imbalance': round(top['channel_imbalance'], 3),
            'top_mean_std': round(top['mean_std'], 3),
            'top_var': round(top['laplacian_var'], 3),
            'top_entropy': round(float(top['entropy']), 3),
            'bottom_means_R': bottom['means'][0],
            'bottom_means_G': bottom['means'][1],
            'bottom_means_B': bottom['means'][2],
            'bottom_stds_R': bottom['stds'][0],
            'bottom_stds_G': bottom['stds'][1],
            'bottom_stds_B': bottom['stds'][2],
            'bottom_dominant': bottom['dominant_channel'],
            'bottom_imbalance': round(bottom['channel_imbalance'], 3),
            'bottom_mean_std': round(bottom['mean_std'], 3),
            'bottom_var': round(bottom['laplacian_var'], 3),
            'bottom_entropy': round(float(bottom['entropy']), 3),
            'bottom_green_ratio': round(bottom['green_ratio'], 3),
            'quality_diff_ratio': round(top['laplacian_var'] / max(bottom['laplacian_var'], 1), 3),
            'brightness_diff': round(sum(top['means']) - sum(bottom['means']), 3)
        }
        rows.append(row)
    
    df = pd.DataFrame(rows)
    xlsx_path = Path(report_path).parent / 'analysis_report.xlsx'
    df.to_excel(xlsx_path, index=False, float_format='%.3f')
    print(f"✅ Excel gerado: {xlsx_path}")
    print(df[['filename', 'corrupted', 'bottom_dominant', 'bottom_imbalance', 'bottom_mean_std', 'bottom_var']].to_string())

if __name__ == '__main__':
    generate_excel('detection_report.json')
