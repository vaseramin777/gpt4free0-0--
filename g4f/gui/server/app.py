# Import the Flask module and create a new Flask web server instance
# '__name__' is the name of the current module, and 'template_folder' is the directory where Flask should look for static HTML templates
from flask import Flask
app = Flask(__name__, template_folder='./../client/html')
