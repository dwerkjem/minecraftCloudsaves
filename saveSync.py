import os

from modules.config import createConfig

from modules.logger import setup_logging

def setup(logger):
    logger.debug("setup() called")
    logger.info("Setting up...")

    if not os.path.exists("config.json"):
        logger.warning("No configuration file found")
        logger.info("Creating a new configuration file...")
        createConfig(logger)
    else:
        logger.info("Configuration file found")



if __name__ == "__main__":
    logger = setup_logging()
    setup(logger)