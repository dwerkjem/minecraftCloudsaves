import json
import os

import questionary

from modules.clouds.googleDrive import *


def createConfig(logger):
    logger.debug("createConfig() called")
    logger.info("Creating a new configuration file...")

    confirm = questionary.confirm("Would you like to set up a new configuration file?").ask()
    if not confirm:
        logger.info("User declined to set up a new configuration file")
        return
    logger.info("User confirmed to set up a new configuration file")
    clouds = ["Google Drive", "SFTP", "Local", "SQL"]
    selected_clouds = []

    while clouds:
        cloud = questionary.select("Select a cloud providers:", choices=clouds).ask()
        selected_clouds.append(cloud)
        clouds.remove(cloud)
        if clouds:
            another = questionary.confirm("Would you like to set up another cloud provider?", default=False).ask()
            if not another:
                break        

    config = {"cloud_providers": selected_clouds}

    if "Google Drive" in selected_clouds:
        config["google_drive"] = {
            "secret_file": questionary.path("Enter the path to the Google Drive secret file:").ask(),
        }
        # test the secret file
        secret_file = config["google_drive"]["secret_file"]
        if not os.path.exists(secret_file):
            logger.error("The Google Drive secret file does not exist")
            return
        if not testGoogleDrive(logger, secret_file):
            return
        folders = getGoogleDriveFolderList(logger, secret_file)
        folder_names = [folder["title"] for folder in folders]
        folder_names.append("Make a new folder")
        folder = questionary.select("Select a folder to sync:", choices=folder_names).ask()
        if folder == "Make a new folder":
            folder = questionary.text("Enter the name of the new folder:").ask()
            makeFolder(logger, secret_file, folder)
        config["google_drive"]["folder_name"] = folder


    with open("config.json", "w") as config_file:
        json.dump(config, config_file, indent=4)

    logger.info("Configuration file created with the following content:")
    logger.info(json.dumps(config, indent=4))

