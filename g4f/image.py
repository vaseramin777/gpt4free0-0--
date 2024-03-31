from __future__ import annotations

import re
from io import BytesIO
import base64
from .typing import ImageType, Union  # Importing custom types from typing module

try:
    from PIL.Image import open as open_image, new as new_image, Image  # Importing PIL's Image module
    from PIL.Image import FLIP_LEFT_RIGHT, ROTATE_180, ROTATE_270, ROTATE_90
    has_requirements = True  # Flag to check if required packages are installed
except ImportError:
    Image = type  # If PIL is not installed, use built-in type as a placeholder
    has_requirements = False
    
from .errors import MissingRequirementsError  # Importing custom error class

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'svg'}  # Allowed image file extensions

def to_image(image: ImageType, is_svg: bool = False) -> Image:
    """
    Converts the input image to a PIL Image object.

    Args:
        image (Union[str, bytes, Image]): The input image.

    Returns:
        Image: The converted PIL Image object.
    """
    if not has_requirements:
        raise MissingRequirementsError('Install "pillow" package for images')
    # ... rest of the function ...

def is_allowed_extension(filename: str) -> bool:
    """
    Checks if the given filename has an allowed extension.

    Args:
        filename (str): The filename to check.

    Returns:
        bool: True if the extension is allowed, False otherwise.
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def is_data_uri_an_image(data_uri: str) -> bool:
    """
    Checks if the given data URI represents an image.

    Args:
        data_uri (str): The data URI to check.

    Raises:
        ValueError: If the data URI is invalid or the image format is not allowed.
    """
    # ... rest of the function ...

def is_accepted_format(binary_data: bytes) -> bool:
    """
    Checks if the given binary data represents an image with an accepted format.

    Args:
        binary_data (bytes): The binary data to check.

    Raises:
        ValueError: If the image format is not allowed.
    """
    # ... rest of the function ...

def extract_data_uri(data_uri: str) -> bytes:
    """
    Extracts the binary data from the given data URI.

    Args:
        data_uri (str): The data URI.

    Returns:
        bytes: The extracted binary data.
    """
    # ... rest of the function ...

def get_orientation(image: Image) -> int:
    """
    Gets the orientation of the given image.

    Args:
        image (Image): The image.

    Returns:
        int: The orientation value.
    """
    # ... rest of the function ...

def process_image(img: Image, new_width: int, new_height: int) -> Image:
    """
    Processes the given image by adjusting its orientation and resizing it.

    Args:
        img (Image): The image to process.
        new_width (int): The new width of the image.
        new_height (int): The new height of the image.

    Returns:
        Image: The processed image.
    """
    # ... rest of the function ...

def to_base64_jpg(image: Image, compression_rate: float) -> str:
    """
    Converts the given image to a base64-encoded string.

    Args:
        image (Image.Image): The image to convert.
        compression_rate (float): The compression rate (0.0 to 1.0).

    Returns:
        str: The base64-encoded image.
    """
    # ... rest of the function ...

def format_images_markdown(images, alt: str, preview: str="{image}?w=200&h=200") -> str:
    """
    Formats the given images as a markdown string.

    Args:
        images: The images to format.
        alt (str): The alt for the images.
        preview (str, optional): The preview URL format. Defaults to "{image}?w=200&h=200".

    Returns:
        str: The formatted markdown string.
    """
    # ... rest of the function ...

def to_bytes(image: Image) -> bytes:
    """
    Converts the given image to bytes.

    Args:
        image (Image.Image): The image to convert.

    Returns:
        bytes: The image as bytes.
    """
    # ... rest of the function ...

class ImageResponse():
    def __init__(
        self,
        images: Union[str, list],
        alt: str,
        options: dict = {}
    ):
        self.images = images
        self.alt = alt
        self.options = options
        
    def __str__(self) -> str:
        return format_images_markdown(self.images, self.alt)
    
    def get(self, key: str):
        return self.options.get(key)
    
class ImageRequest(ImageResponse):
    pass
