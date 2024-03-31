# Importing necessary modules
import sys
from pathlib import Path
import asyncio

# Adding the parent directory of the current file to the system path
sys.path.append(str(Path(__file__).parent.parent.parent))

# Importing g4f module with debug logging enabled
import g4f
g4f.debug.logging = True
from g4f.debug import access_token
provider = g4f.Provider.OpenaiChat

# Setting the target ISO and language
iso = "GE"
language = "german"

# Defining the translate prompt with instructions for the translation
translate_prompt = f"""
Translate this markdown document to {language}.
Don't translate or change inline code examples.
