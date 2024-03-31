from __future__ import annotations

import sys
import asyncio
from asyncio import AbstractEventLoop
from concurrent.futures import ThreadPoolExecutor
from abc import abstractmethod
from inspect import signature, Parameter
from .helper import get_cookies, format_prompt
from ..typing import CreateResult, AsyncResult, Messages, Union
from ..base_provider import BaseProvider
from ..errors import NestAsyncioError, ModelNotSupportedError

