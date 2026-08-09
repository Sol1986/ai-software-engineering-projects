"""
This creates machine-readable logs that work well in Docker and cloud platforms. 
Important rule: log request IDs and operational metadata, but do not log the user’s 
full business request—it could contain sensitive information.

"""

import logging

from pythonjsonlogger.json import JsonFormatter


# Defines a function named configure_logging.
# log_level must be text, such as "INFO" or "ERROR".
# -> None means this function performs setup but does not return a value.
def configure_logging(log_level: str) -> None:
    """“Configure logging using the level I provide. Create a terminal output handler, 
    format each log as JSON with a timestamp, severity, logger name, and message, remove old handlers, 
    then make this handler the main way the application writes logs.”"""

    # Creates a handler that sends log messages to the terminal/console.
    # A handler is the part of logging that decides where a log message goes.
    handler = logging.StreamHandler()

    # Gives that handler a JSON formatter, which controls how each log message looks.
    handler.setFormatter(
        # Defines the fields included in every log entry:
        # time, severity level, logger name, and message.
        JsonFormatter("%(asctime)s %(levelname)s %(name)s %(message)s")
    )


    root_logger = logging.getLogger() # Gets the root logger: the main logger that other loggers inherit from.
    root_logger.setLevel(log_level) # Sets the minimum severity that will be shown, using the value passed into the function.
    root_logger.handlers.clear() # Removes any existing output handlers to prevent duplicate log messages.
    root_logger.addHandler(handler) # Adds the JSON terminal handler created above to the root logger.
