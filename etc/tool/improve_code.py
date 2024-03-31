import sys, re
from pathlib import Path
from os import path  # Importing os module to get the absolute path

sys.path.append(str(Path(__file__).parent.parent.parent))  # Adding the parent directory to the system path

import g4f  # Importing g4f module

def read_code(text):
    """
    This function searches for a code block in the provided text and returns it.

    Parameters:
    text (str): The text to search for a code block in.

    Returns:
    str: The code block found in the text.
    """
    if match := re.search(r"```(python|py|)\n(?P<code>[\S\s]+?)\n```", text):
        return match.group("code")

