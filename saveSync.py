import os

from modules.logger import setup_logging

def setup(logger):
    logger.debug("setup() called")
    logger.info("Setting up...")

    # Check if the user has a configuration file
    if not os.path.exists("config.json"):
        logger.warning("No configuration file found")
        logger.info("Creating a new configuration file...")

def saveSync(logger):
    logger.debug("saveSync() called")
    logger.info("Syncing files...")

    clouds = ["Drive", "SFTP"]

if __name__ == "__main__":
    logger = setup_logging()