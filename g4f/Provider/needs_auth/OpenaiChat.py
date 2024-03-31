from __future__ import annotations

import asyncio
import uuid
import json
import os

try:
    from py_arkose_generator.arkose import get_values_for_request  # Try to import Arkose generator
    from async_property import async_cached_property  # Try to import async_cached_property
    has_requirements = True
except ImportError:  # If any of the imports fail, set has_requirements to False

