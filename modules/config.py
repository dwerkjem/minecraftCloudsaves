import json

import questionary

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
        cloud = questionary.select("Select a cloud provider:", choices=clouds).ask()
        selected_clouds.append(cloud)
        clouds.remove(cloud)
        if clouds:
            another = questionary.confirm("Would you like to set up another cloud provider?").ask()
            if not another:
                break

    config = {"cloud_providers": selected_clouds}

    with open("config.json", "w") as config_file:
        json.dump(config, config_file, indent=4)

    logger.info("Configuration file created with the following content:")
    logger.info(json.dumps(config, indent=4))

