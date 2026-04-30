from enum import Enum


class MetadataFieldKey(Enum):
    """
    Enum representing all possible metadata field keys used in the photo analyzer system.
    Includes EXIF fields, sector metrics, analysis results, and detection fields.
    """
    
    # ===== FILE-LEVEL FIELDS =====
    FILE = "file"
    PATH = "path"
    FORMAT = "format"
    SIZE_MB = "SizeMb"
    WIDTH = "width"
    HEIGHT = "height"
    
    # ===== GPS/EXIF FIELDS =====
    GPS_MAP_DATUM = "GPSMapDatum"
    GPS_INFO = "GPSInfo"
    GPS_LATITUDE = "GPSLatitude"
    GPS_LONGITUDE = "GPSLongitude"
    GPS_ALTITUDE = "GPSAltitude"
    
    # ===== CAMERA/IMAGE EXIF FIELDS =====
    MAKE = "Make"
    MODEL = "Model"
    SOFTWARE = "Software"
    CAMERA_SERIAL_NUMBER = "CameraSerialNumber"
    UNIQUE_CAMERA_MODEL = "UniqueCameraModel"
    PROCESSING_SOFTWARE = "ProcessingSoftware"
    IMAGE_DESCRIPTION = "ImageDescription"
    ORIENTATION = "Orientation"
    DATE_TIME = "DateTime"
    DATE_TIME_ORIGINAL = "DateTimeOriginal"
    DATE_TIME_DIGITIZED = "DateTimeDigitized"
    
    # ===== RESOLUTION FIELDS =====
    RESOLUTION_UNIT = "ResolutionUnit"
    X_RESOLUTION = "XResolution"
    Y_RESOLUTION = "YResolution"
    
    # ===== COLOR/CHANNEL FIELDS =====
    Y_CB_CR_POSITIONING = "YCbCrPositioning"
    
    # ===== XP METADATA FIELDS =====
    XP_COMMENT = "XPComment"
    XP_KEYWORDS = "XPKeywords"
    XP_TITLE = "XPTitle"
    XP_SUBJECT = "XPSubject"
    XP_AUTHOR = "XPAuthor"
    
    # ===== EXIF OFFSET/TAGS =====
    EXIF_OFFSET = "ExifOffset"
    
    # ===== SECTOR KEYS =====
    TOP_LEFT = "top_left"
    TOP_RIGHT = "top_right"
    BOTTOM_LEFT = "bottom_left"
    BOTTOM_RIGHT = "bottom_right"
    OVERALL = "overall"
    
    # ===== SECTOR RGB METRICS =====
    MEANS = "means"
    STDS = "stds"
    DOMINANT_CHANNEL = "dominant_channel"
    CHANNEL_IMBALANCE = "channel_imbalance"
    GREEN_RATIO = "green_ratio"
    RED_RATIO = "red_ratio"
    BLUE_RATIO = "blue_ratio"
    MEAN_STD = "mean_std"
    ENTROPY = "entropy"
    LAPLACIAN_VAR = "laplacian_var"
    PHASH = "phash"    

    
    # ===== CORRUPTION DETECTION FIELDS =====
    CORRUPTED = "corrupted"
    DIAGNOSTICO = "diagnostico"
    DIAGNOSTICO_STATUS = "status"
    DIAGNOSTICO_DETALHES = "detalhes"
    DIAGNOSTICO_SEVERIDADE = "severidade"
    DIAGNOSTICO_EVIDENCIAS = "evidencias"
    
    # ===== EXIF DATA WRAPPER =====
    EXIF = "exif"
    
    @classmethod
    def get_all_exif_fields(cls) -> list:
        """Returns all EXIF-related field keys."""
        return [
            cls.GPS_INFO,
            cls.GPS_MAP_DATUM,
            cls.GPS_LATITUDE,
            cls.GPS_LONGITUDE,
            cls.GPS_ALTITUDE,
            cls.MAKE,
            cls.MODEL,
            cls.SOFTWARE,
            cls.CAMERA_SERIAL_NUMBER,
            cls.UNIQUE_CAMERA_MODEL,
            cls.PROCESSING_SOFTWARE,
            cls.IMAGE_DESCRIPTION,
            cls.ORIENTATION,
            cls.DATE_TIME,
            cls.DATE_TIME_ORIGINAL,
            cls.DATE_TIME_DIGITIZED,
            cls.RESOLUTION_UNIT,
            cls.X_RESOLUTION,
            cls.Y_RESOLUTION,
            cls.Y_CB_CR_POSITIONING,
            cls.XP_COMMENT,
            cls.XP_KEYWORDS,
            cls.XP_TITLE,
            cls.XP_SUBJECT,
            cls.XP_AUTHOR,
            cls.EXIF_OFFSET,
        ]


    
    @classmethod
    def get_sector_names(cls) -> list:
        """Returns all sector name keys."""
        return [
            cls.TOP_LEFT,
            cls.TOP_RIGHT,
            cls.BOTTOM_LEFT,
            cls.BOTTOM_RIGHT,
            cls.OVERALL,
        ]
    
    @classmethod
    def get_detection_fields(cls) -> list:
        """Returns all corruption detection field keys."""
        return [
            cls.CORRUPTED,
            cls.DIAGNOSTICO,
            cls.DIAGNOSTICO_STATUS,
            cls.DIAGNOSTICO_DETALHES,
            cls.DIAGNOSTICO_SEVERIDADE,
            cls.DIAGNOSTICO_EVIDENCIAS,
        ]
    
    @classmethod
    def from_string(cls, value: str) -> 'MetadataFieldKey':
        """
        Create enum from string value.
        
        Args:
            value: String representation of the field
            
        Returns:
            MetadataFieldKey enum value
        """
        for member in cls:
            if member.value == value:
                return member
        raise ValueError(f"Unknown field key: {value}")
