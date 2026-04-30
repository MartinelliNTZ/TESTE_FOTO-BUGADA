import os
from PIL import Image, ExifTags
import numpy as np
import cv2
from skimage import measure
import imagehash
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

class ImageAnalyzer:
    def __init__(self, image_path: str):
        self.path = image_path
        self.image = None
        self.exif = {}
        self._load_image()
        self._extract_exif()

    def _load_image(self):
        self.image = cv2.imread(self.path)
        if self.image is None:
            raise ValueError(f"Could not load image: {self.path}")
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)

    def _extract_exif(self):
        pil_image = Image.open(self.path)
        exifdata = pil_image.getexif()
        for tag_id, value in exifdata.items():
            tag = ExifTags.TAGS.get(tag_id, tag_id)
            self.exif[tag] = value

    def get_full_metrics(self):
        from metadata.ImageRGBUtil import ImageRGBUtil
        
        # Delegate tudo para ImageRGBUtil
        return ImageRGBUtil.get_full_metrics(self.image, self.path, self.exif, self.image.shape[0], self.image.shape[1])
