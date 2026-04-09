import json

class PhotoSector:
    def __init__(self, json_data: dict):
        """
        Initialize PhotoSector from JSON data (top_left region dict).
        Expects keys: 'means', 'stds', 'dominant_channel', 'channel_imbalance',
        'green_ratio', 'red_ratio', 'blue_ratio', 'mean_std', 'laplacian_var', 'entropy'.
        """
        means = json_data.get('means', [0.0, 0.0, 0.0])
        stds = json_data.get('stds', [0.0, 0.0, 0.0])
        
        self.means_R = float(means[0])
        self.means_G = float(means[1])
        self.means_B = float(means[2])
        
        self.stds_R = float(stds[0])
        self.stds_G = float(stds[1])
        self.stds_B = float(stds[2])
        
        self.dominant = json_data.get('dominant_channel', 'Unknown')
        self.imbalance = float(json_data.get('channel_imbalance', 0.0))
        self.green_ratio = float(json_data.get('green_ratio', 0.0))
        self.red_ratio = float(json_data.get('red_ratio', 0.0))
        self.blue_ratio = float(json_data.get('blue_ratio', 0.0))
        self.mean_std = float(json_data.get('mean_std', 0.0))
        self.var = float(json_data.get('laplacian_var', 0.0))
        self.entropy = float(json_data.get('entropy', 0.0))

    def to_json(self) -> dict:
        """
        Convert PhotoSector to JSON-serializable dict.
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
