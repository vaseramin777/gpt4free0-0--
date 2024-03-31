import argparse
from enum import Enum

import g4f
from g4f import Provider

from g4f.gui.run import gui_parser, run_gui_args

def run_gui(args):
    # Print a message indicating that the GUI is running
    print("Running GUI...")

def main():
    # Define an Enum class for IgnoredProviders, using the names of all Provider classes
    IgnoredProviders = Enum("ignore_providers", {key: key for key in Provider.__all__})
    
    # Create an ArgumentParser object to parse command-line arguments
    parser = argparse.ArgumentParser(description="Run gpt4free")
    
    # Add a subparser for the 'api' mode
    subparsers = parser.add_subparsers(dest="mode", help="Mode to run the g4f in.")
    api_parser=subparsers.add_parser("api")
    
    # Add arguments for the 'api' mode
    api_parser.add_argument("--bind", default="0.0.0.0:1337", help="The bind string.")
    api_parser.add_argument("--debug", type=bool, default=False, help="Enable verbose logging")
    api_parser.add_argument("--ignored-providers", nargs="+", choices=[provider.name for provider in IgnoredProviders],
                            default=[], help="List of providers to ignore when processing request.")
    
    # Add a subparser for the 'gui' mode
    subparsers.add_parser("gui", parents=[gui_parser()], add_help=False)

    # Parse the command-line arguments
    args = parser.parse_args()
    
    # Check if the 'api' mode was specified
    if args.mode == "api":
        # Import the Api class from g4f.api
        from g4f.api import Api
        
        # Create an instance of the Api class, passing the required arguments
        controller=Api(engine=g4f, debug=args.debug, list_ignored_providers=args.ignored_providers)
        
        # Call the run()
