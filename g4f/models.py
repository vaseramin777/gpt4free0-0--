# Import necessary modules: `dataclass` for defining classes with default values, and various providers for machine learning models.
from dataclasses import dataclass
from .Provider   import RetryProvider, ProviderType
from .Provider   import (
    Chatgpt4Online,
    PerplexityLabs,
    ChatgptDemoAi,
    GeminiProChat,
    ChatgptNext,
    HuggingChat,
    ChatgptDemo,
    FreeChatgpt,
    GptForLove,
    ChatgptAi,
    DeepInfra,
    ChatBase,
    Liaobots,
    GeekGpt,
    FakeGpt,
    FreeGpt,
    Llama2,
    Vercel,
    Phind,
    GptGo,
    Gpt6,
    Bard,
    Bing,
    You,
    Pi,
)

# Define the `Model` class with attributes for the model's name, base provider, and best provider.
# The `unsafe_hash=True` argument is used to allow hashable dataclass instances with mutable fields.
@dataclass(unsafe_hash=True)
class Model:
    name: str
    base_provider: str
    best_provider: ProviderType = None

# Define a method for getting a list of all model names.
    @staticmethod
    def __all__() -> list[str]:
        return _all_models

# Define the default model configuration.
default = Model(
    name          = "",
    base_provider = "",
    best_provider = RetryProvider([
        Bing,
        ChatgptAi, GptGo, GeekGpt,
        You,
        Chatgpt4Online
    ])
)

# Define several predefined model configurations as instances of the `Model` class.
# These configurations are stored in a dictionary called `ModelUtils.convert`.

# Define a utility class for mapping string identifiers to Model instances.
class ModelUtils:
    convert: dict[str, Model] = {
        # gpt-3.5
        'gpt-3.5-turbo'          : gpt_35_turbo,
        'gpt-3.5-turbo-0613'     : gpt_35_turbo_0613,
        'gpt-3.5-turbo-16k'      : gpt_35_turbo_16k,
        'gpt-3.5-turbo-16k-0613' : gpt_35_turbo_16k_0613,

        'gpt-3.5-long': gpt_35_long,

        # gpt-4
        'gpt-4'          : gpt_4,
        'gpt-4-0613'     : gpt_4_0613,
        'gpt-4-32k'      : gpt_4_32k,
        'gpt-4-32k-0613' : gpt_4_32k_0613,
        'gpt-4-turbo'    : gpt_4_turbo,

        # Llama 2
        'llama2-7b' : llama2_7b,
        'llama2-13b': llama2_13b,
        'llama2-70b': llama2_70b,
        'codellama-34b-instruct': codellama_34b_instruct,

        # Mistral
        'mixtral-8x7b': mixtral_8x7b,
        'mistral-7b': mistral_7b,

        # Misc models
        'dolphin-mixtral-8x7b': dolphin_mixtral_8x7b,
        'lzlv-70b': lzlv_70b,
        'airoboros-70b': airoboros_70b,
        'airoboros-l2-70b': airoboros_l2_70b,
        'openchat_3.5': openchat_35,
        'gemini-pro': gemini_pro,
        'bard': bard,
        'claude-v2': claude_v2,
        'pi': pi
    }

# Define a variable for getting a list of all model names.
_all_models = list(ModelUtils.convert.keys())
