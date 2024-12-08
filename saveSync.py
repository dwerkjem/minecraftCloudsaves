import os

from modules.logger import setup_logging

def setup(logger):
    logger.debug("setup() called")
    logger.info("Setting up...")

    # Check if the user has a configuration file
    if not os.path.exists("config.json"):
        logger.warning("No configuration file found")
        logger.info("Creating a new configuration file...")
        createConfig(logger)
    else:
        logger.info("Configuration file found")

def createConfig(logger):
    logger.debug("createConfig() called")
    logger.info("Creating a new configuration file...")

    # Create a new configuration file from the default template (config.default.json)
    with open(".config.default.json") as f:
        template = f.read()

    with open("config.json", "w") as f:
        f.write(template)

    logger.info("Configuration file created")


if __name__ == "__main__":
    logger = setup_logging()
    setup(logger)