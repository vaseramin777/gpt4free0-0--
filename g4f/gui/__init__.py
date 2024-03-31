# Import necessary modules and functions from the local server package.
# If the necessary packages are not installed, raise a MissingRequirementsError.
try:
    from .server.app     import app
    from .server.website import Website
    from .server.backend import Backend_Api
except ImportError:
    from g4f.errors import MissingRequirementsError
    raise MissingRequirementsError('Install "flask" and "werkzeug" package for gui')

def run_gui(host: str = '0.0.0.0', port: int = 80, debug: bool = False) -> None:
    """
    Run the GUI for the application.

    This function sets up the Flask application, adds all the necessary routes
    for the website and backend API, and starts the server.

    Args:
        host (str): The host address to bind the server to. Default is '0.0.0.0'.
        port (int): The port number to bind the server to. Default is 80.
        debug (bool): Whether or not to run the server in debug mode. Default is False.

    Returns:
        None
    """
    config = {
        'host' : host,
        'port' : port,
        'debug': debug
    }

    # Create a Website object and add all its routes to the Flask application.
    site = Website(app)
    for route in site.routes:
        app.add_url_rule(
            route,
            view_func = site.routes[route]['function'],
            methods   = site.routes[route]['methods'],
        )

    # Create a Backend_Api object and add all its routes to the Flask application.
    backend_api  = Backend_Api(app)
    for route in backend_api.routes:
        app.add_url_rule(
            route,
            view_func = backend_api.routes[route]['function'],
            methods   = backend_api.routes[route]['methods'],
        )

    # Print a message indicating that the server is starting.
    print(
