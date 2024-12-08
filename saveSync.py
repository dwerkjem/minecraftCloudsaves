import sys
import logging
# Parse command-line arguments
args = sys.argv[1:]

def setup_logging():
    # ANSI color codes
    class LogColors:
        DEBUG = "\033[94m"  # Blue
        INFO = "\033[92m"   # Green
        WARNING = "\033[93m" # Yellow
        ERROR = "\033[91m"  # Red
        RESET = "\033[0m"   # Reset to default

    # Custom formatter to add colors
    class ColorFormatter(logging.Formatter):
        FORMAT = "%(levelname)s (%(filename)s): %(message)s "

        COLOR_MAP = {
            logging.DEBUG: LogColors.DEBUG,
            logging.INFO: LogColors.INFO,
            logging.WARNING: LogColors.WARNING,
            logging.ERROR: LogColors.ERROR,
        }

        def format(self, record):
            color = self.COLOR_MAP.get(record.levelno, LogColors.RESET)
            formatted = super().format(record)
            return f"{color}{formatted}{LogColors.RESET}"

    

    # Determine the logging level
    if 'D' in args:
        log_level = logging.DEBUG
        debug = True
    elif 'V' in args:
        log_level = logging.INFO
    elif 'S' in args:
        log_level = logging.ERROR
    else:
        log_level = logging.WARNING  # Default level

    # Configure logging
    handler = logging.StreamHandler()
    handler.setFormatter(ColorFormatter(ColorFormatter.FORMAT))
    logging.basicConfig(level=log_level, handlers=[handler])

    # Create logger
    logger = logging.getLogger(__name__)

    if debug:
        logger.debug("Debug mode enabled")
        logger.debug(f"Arguments: {args}")
    
    return logger

def saveSync(logger):
    logger.debug("saveSync() called")
    logger.info("Syncing files...")

    clouds = ["Drive", "Dropbox", ]

if __name__ == "__main__":
    logger = setup_logging()