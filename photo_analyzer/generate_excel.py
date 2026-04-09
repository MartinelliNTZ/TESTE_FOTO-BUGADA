import json
import pandas as pd
from pathlib import Path
import numpy as np

def generate_excel(report_path):
    with open(report_path, 'r') as f:
        results = json.load(f)
    
    rows = []
    for fname, data in results.items():
        row = {
            'filename': fname,
            'corrupted': data['corrupted'],
            'size': f"{data['width']}x{data['height']}",
        }
        # 4 sectors
        for sector in ['top_left', 'top_right', 'bottom_left', 'bottom_right']:
            s = data[sector]
            prefix = f"{sector}_"
            row[f"{prefix}means_R"] = s.get('means_R', 0)
            row[f"{prefix}means_G"] = s.get('means_G', 0)
            row[f"{prefix}means_B"] = s.get('means_B', 0)
            row[f"{prefix}stds_R"] = s.get('stds_R', 0)
            row[f"{prefix}stds_G"] = s.get('stds_G', 0)
            row[f"{prefix}stds_B"] = s.get('stds_B', 0)
            row[f"{prefix}dominant"] = s.get('dominant', 'Unknown')
            row[f"{prefix}imbalance"] = round(s.get('imbalance', 0), 3)
            row[f"{prefix}green_ratio"] = round(s.get('green_ratio', 0), 3)
            row[f"{prefix}red_ratio"] = round(s.get('red_ratio', 0), 3)
            row[f"{prefix}blue_ratio"] = round(s.get('blue_ratio', 0), 3)
            row[f"{prefix}mean_std"] = round(s.get('mean_std', 0), 3)
            row[f"{prefix}var"] = round(s.get('var', 0), 3)
            row[f"{prefix}entropy"] = round(s.get('entropy', 0), 3)
        rows.append(row)
    
    df = pd.DataFrame(rows)
    xlsx_path = Path(report_path).parent / 'analysis_report.xlsx'
    df.to_excel(xlsx_path, index=False, float_format='%.3f')
    print(f"✅ Excel gerado: {xlsx_path}")
    print(df[['filename', 'corrupted', 'bottom_left_dominant', 'bottom_right_imbalance', 'bottom_left_var']].to_string(index=False))

if __name__ == '__main__':
    report_path = Path(__file__).parent / 'detection_report.json'
    if report_path.exists():
        generate_excel(report_path)
    else:
        print("Rode 'python main.py' primeiro!")

