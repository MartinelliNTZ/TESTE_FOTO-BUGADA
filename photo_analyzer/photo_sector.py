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
        
        self.top_left_means_R = float(means[0])
        self.top_left_means_G = float(means[1])
        self.top_left_means_B = float(means[2])
        
        self.top_left_stds_R = float(stds[0])
        self.top_left_stds_G = float(stds[1])
        self.top_left_stds_B = float(stds[2])
        
        self.top_left_dominant = json_data.get('dominant_channel', 'Unknown')
        self.top_left_imbalance = float(json_data.get('channel_imbalance', 0.0))
        self.top_left_green_ratio = float(json_data.get('green_ratio', 0.0))
        self.top_left_red_ratio = float(json_data.get('red_ratio', 0.0))
        self.top_left_blue_ratio = float(json_data.get('blue_ratio', 0.0))
        self.top_left_mean_std = float(json_data.get('mean_std', 0.0))
        self.top_left_var = float(json_data.get('laplacian_var', 0.0))
        self.top_left_entropy = float(json_data.get('entropy', 0.0))

    def to_json(self) -> dict:
        """
        Convert PhotoSector to JSON-serializable dict.
        """
        return {
            'top_left_means_R': self.top_left_means_R,
            'top_left_means_G': self.top_left_means_G,
            'top_left_means_B': self.top_left_means_B,
            'top_left_stds_R': self.top_left_stds_R,
            'top_left_stds_G': self.top_left_stds_G,
            'top_left_stds_B': self.top_left_stds_B,
            'top_left_dominant': self.top_left_dominant,
            'top_left_imbalance': self.top_left_imbalance,
            'top_left_green_ratio': self.top_left_green_ratio,
            'top_left_red_ratio': self.top_left_red_ratio,
            'top_left_blue_ratio': self.top_left_blue_ratio,
            'top_left_mean_std': self.top_left_mean_std,
            'top_left_var': self.top_left_var,
            'top_left_entropy': self.top_left_entropy
        }
