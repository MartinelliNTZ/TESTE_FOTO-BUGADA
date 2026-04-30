from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class SectorMetrics:
    """
    Model representing metrics for an image sector (quadrant).
    Each sector contains RGB and HSV channel statistics.
    """
    # RGB Channel Statistics
    means: List[float] = field(default_factory=lambda: [0.0, 0.0, 0.0])
    stds: List[float] = field(default_factory=lambda: [0.0, 0.0, 0.0])
    dominant_channel: str = ""
    channel_imbalance: float = 0.0
    
    # Color Ratios
    green_ratio: float = 0.0
    red_ratio: float = 0.0
    blue_ratio: float = 0.0
    
    # Global Statistics
    mean_std: float = 0.0
    entropy: float = 0.0
    laplacian_var: float = 0.0
    
    # Perceptual Hash
    phash: str = ""
    
    # HSV Channel Statistics
    hsv_means: List[float] = field(default_factory=lambda: [0.0, 0.0, 0.0])
    hsv_stds: List[float] = field(default_factory=lambda: [0.0, 0.0, 0.0])
    hsv_dominant: str = ""
    hsv_imbalance: float = 0.0
    
    # HSV Color Ratios
    hsv_s_ratio: float = 0.0
    hsv_v_ratio: float = 0.0
    hsv_h_ratio: float = 0.0
    
    # HSV Global Statistics
    hsv_mean_std: float = 0.0
    hsv_entropy: float = 0.0
    hsv_var: float = 0.0
    
    @classmethod
    def from_dict(cls, data: dict) -> 'SectorMetrics':
        """
        Create a SectorMetrics instance from a dictionary.
        
        Args:
            data: Dictionary containing sector metrics data
            
        Returns:
            SectorMetrics instance
        """
        return cls(
            means=data.get('means', [0.0, 0.0, 0.0]),
            stds=data.get('stds', [0.0, 0.0, 0.0]),
            dominant_channel=data.get('dominant_channel', ''),
            channel_imbalance=data.get('channel_imbalance', 0.0),
            green_ratio=data.get('green_ratio', 0.0),
            red_ratio=data.get('red_ratio', 0.0),
            blue_ratio=data.get('blue_ratio', 0.0),
            mean_std=data.get('mean_std', 0.0),
            entropy=data.get('entropy', 0.0),
            laplacian_var=data.get('laplacian_var', 0.0),
            phash=data.get('phash', ''),
            hsv_means=data.get('hsv_means', [0.0, 0.0, 0.0]),
            hsv_stds=data.get('hsv_stds', [0.0, 0.0, 0.0]),
            hsv_dominant=data.get('hsv_dominant', ''),
            hsv_imbalance=data.get('hsv_imbalance', 0.0),
            hsv_s_ratio=data.get('hsv_s_ratio', 0.0),
            hsv_v_ratio=data.get('hsv_v_ratio', 0.0),
            hsv_h_ratio=data.get('hsv_h_ratio', 0.0),
            hsv_mean_std=data.get('hsv_mean_std', 0.0),
            hsv_entropy=data.get('hsv_entropy', 0.0),
            hsv_var=data.get('hsv_var', 0.0)
        )
    
    def to_dict(self) -> dict:
        """
        Convert SectorMetrics to dictionary.
        
        Returns:
            Dictionary representation
        """
        return {
            'means': self.means,
            'stds': self.stds,
            'dominant_channel': self.dominant_channel,
            'channel_imbalance': self.channel_imbalance,
            'green_ratio': self.green_ratio,
            'red_ratio': self.red_ratio,
            'blue_ratio': self.blue_ratio,
            'mean_std': self.mean_std,
            'entropy': self.entropy,
            'laplacian_var': self.laplacian_var,
            'phash': self.phash,
            'hsv_means': self.hsv_means,
            'hsv_stds': self.hsv_stds,
            'hsv_dominant': self.hsv_dominant,
            'hsv_imbalance': self.hsv_imbalance,
            'hsv_s_ratio': self.hsv_s_ratio,
            'hsv_v_ratio': self.hsv_v_ratio,
            'hsv_h_ratio': self.hsv_h_ratio,
            'hsv_mean_std': self.hsv_mean_std,
            'hsv_entropy': self.hsv_entropy,
            'hsv_var': self.hsv_var
        }
    
    @property
    def is_grey(self) -> bool:
        """Check if the sector is essentially grey (RGB values equal)."""
        return (self.means[0] == self.means[1] == self.means[2] and 
                self.stds[0] < 1.0 and self.stds[1] < 1.0 and self.stds[2] < 1.0)
    
    @property
    def has_low_variance(self) -> bool:
        """Check if the sector has low variance (possibly corrupted)."""
        return self.laplacian_var < 50.0
    
    @property
    def has_low_entropy(self) -> bool:
        """Check if the sector has low entropy (possibly corrupted)."""
        return self.entropy < 4.0
    
    @property
    def has_green_dominance(self) -> bool:
        """Check if green channel dominates excessively."""
        return self.green_ratio > 50.0
