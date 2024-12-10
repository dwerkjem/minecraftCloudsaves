import json
import os

import questionary

from modules.clouds.googleDrive import *

def setup_google_drive(logger, config):
    try:
        secret_file = questionary.path("Enter the path to the Google Drive secret file:").ask()
        while not os.path.exists(secret_file):
            logger.error("The Google Drive secret file does not exist. Please try again.")
            secret_file = questionary.path("Enter the path to the Google Drive secret file:").ask()

        if not testGoogleDrive(logger, secret_file):
            logger.error("Failed to connect to Google Drive with the provided credentials.")
            if questionary.confirm("Try again?", default=True).ask():
                return setup_google_drive(logger, config)
            else:
                logger.warning("Skipping Google Drive setup.")
                return

        config["google_drive"] = {"secret_file": secret_file}

        folders = getGoogleDriveFolderList(logger, secret_file)
        if not folders:
            logger.warning("No folders found in Google Drive.")
            if questionary.confirm("Create a new folder?", default=True).ask():
                new_folder_name = questionary.text("Enter the name of the new folder:").ask()
                makeFolder(logger, secret_file, new_folder_name)
                config["google_drive"]["folder_name"] = new_folder_name
            return
        
        folder_names = [folder["title"] for folder in folders] + ["Make a new folder"]
        folder_choice = questionary.select("Select a folder to sync:", choices=folder_names).ask()
        if folder_choice == "Make a new folder":
            folder_choice = questionary.text("Enter the name of the new folder:").ask()
            makeFolder(logger, secret_file, folder_choice)

        config["google_drive"]["folder_name"] = folder_choice

    except KeyboardInterrupt:
        logger.info("Configuration creation canceled by user (Ctrl+C). No config will be created.")
        # Raise the exception again to be caught by createConfig
        raise

def createConfig(logger):
    logger.debug("createConfig() called")
    logger.info("Creating a new configuration file...")

    try:
        if not questionary.confirm("Would you like to set up a new configuration file?").ask():
            logger.info("User declined to set up a new configuration file")
            return

        config = {}
        clouds = ["Google Drive", "SFTP", "Local", "SQL"]
        selected_clouds = []

        while clouds:
            cloud = questionary.select("Select a cloud provider:", choices=clouds).ask()
            selected_clouds.append(cloud)
            clouds.remove(cloud)
            if clouds and not questionary.confirm("Would you like to set up another cloud provider?", default=False).ask():
                break

        config["cloud_providers"] = selected_clouds

        # If Google Drive is selected, run its setup
        if "Google Drive" in selected_clouds:
            setup_google_drive(logger, config)

        if not config:
            logger.info("No configuration was created.")
            return

        with open("config.json", "w") as config_file:
            json.dump(config, config_file, indent=4)
        logger.info("Configuration file created with the following content:")
        logger.info(json.dumps(config, indent=4))

    except KeyboardInterrupt:
        logger.info("Configuration creation canceled by user (Ctrl+C). No config will be created.")
        return
