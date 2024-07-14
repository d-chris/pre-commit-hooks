# logger_config.py
import logging


def get_logger(name: str) -> logging.Logger:
    # Create a logger for the given name
    log = logging.getLogger(name)

    # Set the log level for this logger
    log.setLevel(logging.CRITICAL)

    # Check if handlers are already configured
    if not log.handlers:
        # Create a handler for the logger
        handler = logging.StreamHandler()

        # Set the log level for the handler
        handler.setLevel(logging.INFO)

        # Create a formatter and set it for the handler
        formatter = logging.Formatter("%(name)s: %(message)s")
        handler.setFormatter(formatter)

        # Add the handler to the logger
        log.addHandler(handler)

    return log
