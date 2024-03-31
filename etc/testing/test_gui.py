# Import the sys module from the standard library to interact with the Python runtime environment
import sys

# Import the Path class from the pathlib module to handle filesystem paths
from pathlib import Path

# Add the parent directory of the current file to the sys.path list
# This allows the script to import modules located in that directory
sys.path.append(str(Path(__file__).parent.parent.parent))

# Import the run_gui function from the g4f.gui module
from g4f.gui import run_gui

# Call the run_gui function to start the GUI
run_gui()
