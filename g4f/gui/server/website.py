from flask import render_template, send_file, redirect
from time import time
from os import urandom

class Website:
    def __init__(self, app) -> None:
        # Initialize the Website class with the Flask app instance
        self.app = app
        self.routes = {
            # Define the application routes with their corresponding functions and HTTP methods
            '/': {
                'function': lambda: redirect('/chat'),
                'methods': ['GET', 'POST']
            },
            '/chat/': {
                'function': self._index,
                'methods': ['GET', 'POST']
            },
            '/chat/<conversation_id>': {
                'function': self._chat,
                'methods': ['GET', 'POST']
            },
            '/assets/<folder>/<file>': {
                'function': self._assets,
                'methods': ['GET', 'POST']
            }
        }

    def _chat(self, conversation_id):
        # Redirect to the homepage if the conversation ID contains no hyphens
        if '-' not in conversation_id:
            return redirect('/chat')

        # Render the index.html template with the provided conversation ID
        return render_template('index.html', chat_id = conversation_id)

    def _index(self):
        # Generate a unique conversation ID using random hexadecimal strings and the current timestamp
        conversation_id = f'{urandom(4).hex()}-{urandom(2).hex()}-{urandom(2).hex()}-{urandom(2).hex()}-{hex(int(time() * 1000))[2:]}'

        # Render the index.html template with the generated conversation ID
        return render_template('index.html', chat_id = conversation_id)

    def _assets(self, folder: str, file: str):
        # Attempt to send the specified file from the client folder as a response
        try:
            return send_file(f"./../client/{folder}/{file}", as_attachment=False)
        except:
            # If the file is not found, return a 
