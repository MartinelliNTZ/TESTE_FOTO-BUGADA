import json

class PhotoSector:
    def __init__(self, json_data: dict):
        """
        Initialize PhotoSector from raw or flattened JSON data.
        Backward compat with raw ('means' list) or flattened ('means_R').
        """
        # Backward compat with raw format
        means = json_data.get('means', [0.0, 0.0, 0.0])
        stds = json_data.get('stds', [0.0, 0.0, 0.0])
        
        self.means_R = float(json_data.get('means_R', means[0]))
        self.means_G = float(json_data.get('means_G', means[1]))
        self.means_B = float(json_data.get('means_B', means[2]))
        
        self.stds_R = float(json_data.get('stds_R', stds[0]))
        self.stds_G = float(json_data.get('stds_G', stds[1]))
        self.stds_B = float(json_data.get('stds_B', stds[2]))
        
        self.dominant = json_data.get('dominant', json_data.get('dominant_channel', 'Unknown'))
        self.imbalance = float(json_data.get('imbalance', json_data.get('channel_imbalance', 0.0)))
        self.green_ratio = float(json_data.get('green_ratio', 0.0))
        self.red_ratio = float(json_data.get('red_ratio', 0.0))
        self.blue_ratio = float(json_data.get('blue_ratio', 0.0))
        self.mean_std = float(json_data.get('mean_std', 0.0))
        self.var = float(json_data.get('var', json_data.get('laplacian_var', 0.0)))
        self.entropy = float(json_data.get('entropy', 0.0))

    def to_json(self) -> dict:
        """
        Convert PhotoSector to JSON-serializable dict (flattened keys).
        """
        return {
            'means_R': self.means_R,
            'means_G': self.means_G,
            'means_B': self.means_B,
            'stds_R': self.stds_R,
            'stds_G': self.stds_G,
            'stds_B': self.stds_B,
            'dominant': self.dominant,
            'imbalance': self.imbalance,
            'green_ratio': self.green_ratio,
            'red_ratio': self.red_ratio,
            'blue_ratio': self.blue_ratio,
            'mean_std': self.mean_std,
            'var': self.var,
            'entropy': self.entropy
        }

class PhotoImage:
    def __init__(self, metrics: dict):
        """
        Initialize PhotoImage with corrupted flag + 5 PhotoSectors.
        """
        self.corrupted = metrics.get('corrupted', False)
        
        # 5 sectors: 4 quadrants + overall
        self.top_left = PhotoSector(metrics.get('top_left', {}))
        self.top_right = PhotoSector(metrics.get('top_right', {}))
        self.bottom_left = PhotoSector(metrics.get('bottom_left', {}))
        self.bottom_right = PhotoSector(metrics.get('bottom_right', {}))
        self.overall = PhotoSector(metrics.get('overall', {}))

    def to_json(self) -> dict:
        """
        Full image to JSON: corrupted + 5 sectors only.
        """
        return {
            'corrupted': self.corrupted,
            'top_left': self.top_left.to_json(),
            'top_right': self.top_right.to_json(),
            'bottom_left': self.bottom_left.to_json(),
            'bottom_right': self.bottom_right.to_json(),
            'overall': self.overall.to_json()
        }
