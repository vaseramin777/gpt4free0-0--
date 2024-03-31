# Importing necessary modules and classes
from __future__ import annotations

from ..base_provider import BaseProvider, ProviderType
from .retry_provider import RetryProvider
from .base_provider import AsyncProvider, AsyncGeneratorProvider
from .create_images import CreateImagesProvider
from .deprecated import *
from .needs_auth import *
from .unfinished import *
from .selenium import *

# Importing specific classes from various modules
from .AiAsk import AiAsk
from .AiChatOnline import AiChatOnline
from .AItianhu import AItianhu
from .Aura import Aura
from .Bestim import Bestim
from .Bing import Bing
from .ChatAnywhere import ChatAnywhere
from .ChatBase import ChatBase
from .ChatForAi import ChatForAi
from .Chatgpt4Online import Chatgpt4Online
from .ChatgptAi import ChatgptAi
from .ChatgptDemo import ChatgptDemo
from .ChatgptDemoAi import ChatgptDemoAi
from .ChatgptFree import ChatgptFree
from .ChatgptLogin import ChatgptLogin
from .ChatgptNext import ChatgptNext
from .ChatgptX import ChatgptX
from .Chatxyz import Chatxyz
from .DeepInfra import DeepInfra
from .FakeGpt import FakeGpt
from .FreeChatgpt import FreeChatgpt
from .FreeGpt import FreeGpt
from .GeekGpt import GeekGpt
from .GeminiProChat import GeminiProChat
from .Gpt6 import Gpt6
from .GPTalk import GPTalk
from .GptChatly import GptChatly
from .GptForLove import GptForLove
from .GptGo import GptGo
from .GptGod import GptGod
from .GptTalkRu import GptTalkRu
from .Hashnode import Hashnode
from .HuggingChat import HuggingChat
from .Koala import Koala
from .Liaobots import Liaobots
from .Llama2 import Llama2
from .OnlineGpt import OnlineGpt
from .PerplexityLabs import PerplexityLabs
from .Phind import Phind
from .Pi import Pi
from .Vercel import Vercel
from .Ylokh import Ylokh
from .You import You

# Importing sys module
import sys

# Assigning a list of modules to the variable __modules__
__modules__ = [
    getattr(sys.modules[__name__], provider) for provider in dir()
    if not provider.startswith("__")
]

# Assigning a list of provider classes to the variable __providers__
__providers__ = [
    provider for provider in __modules__
    if isinstance(provider, type)
    and issubclass(provider, BaseProvider)
]

# Assigning a list of provider names to the variable __all__
__all__ = [provider.__name__ for provider in __providers__]

# Creating a dictionary with provider names as keys and provider classes as values
__map__ = dict([(provider.__name__, provider) for provider in __providers__])

# Defining a class ProviderUtils with a class attribute convert
class ProviderUtils:
    convert: dict[str, ProviderType] = __map__
