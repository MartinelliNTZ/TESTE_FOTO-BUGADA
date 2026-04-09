class PhotoSector:
    def __init__(self, json_data: dict):
        """
        Initialize PhotoSector from raw or flattened JSON data.
        Backward compat with raw ('means' list) or flattened ('means_R').
        """
        # Backward compat with raw format
        means = json_data.get('means', [0.0, 0.0, 0.0])
        stds = json_data.get('stds', [0.0, 0.0, 0.0])
        
        self.top_left_means_R = float(json_data.get('top_left_means_R', json_data.get('means_R', means[0])))
        self.top_left_means_G = float(json_data.get('top_left_means_G', json_data.get('means_G', means[1])))
        self.top_left_means_B = float(json_data.get('top_left_means_B', json_data.get('means_B', means[2])))
        
        self.top_left_stds_R = float(json_data.get('top_left_stds_R', json_data.get('stds_R', stds[0])))
        self.top_left_stds_G = float(json_data.get('top_left_stds_G', json_data.get('stds_G', stds[1])))
        self.top_left_stds_B = float(json_data.get('top_left_stds_B', json_data.get('stds_B', stds[2])))
        
        self.top_left_dominant = json_data.get('top_left_dominant', json_data.get('dominant', json_data.get('dominant_channel', 'Unknown')))
        self.top_left_imbalance = float(json_data.get('top_left_imbalance', json_data.get('imbalance', json_data.get('channel_imbalance', 0.0))))
        self.top_left_green_ratio = float(json_data.get('top_left_green_ratio', json_data.get('green_ratio', 0.0)))
        self.top_left_red_ratio = float(json_data.get('top_left_red_ratio', json_data.get('red_ratio', 0.0)))
        self.top_left_blue_ratio = float(json_data.get('top_left_blue_ratio', json_data.get('blue_ratio', 0.0)))
        self.top_left_mean_std = float(json_data.get('top_left_mean_std', json_data.get('mean_std', 0.0)))
        self.top_left_var = float(json_data.get('top_left_var', json_data.get('var', json_data.get('laplacian_var', 0.0))))
        self.top_left_entropy = float(json_data.get('top_left_entropy', json_data.get('entropy', 0.0)))

    def to_json(self) -> dict:
        """
        Convert PhotoSector to flattened JSON-serializable dict.
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
