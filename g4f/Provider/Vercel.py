from __future__ import annotations  # Allows using class names in type hints before they are defined

import json
import base64
import requests
import random
import uuid

try:
    import execjs  # Required for generating anti-bot token
    has_requirements = True
except ImportError:
    has_requirements = False

from ..typing import Messages, TypedDict, CreateResult, Any  # Import custom types
from .base_provider import AbstractProvider  # Import base provider class
from ..errors import MissingRequirementsError  # Import custom error class


