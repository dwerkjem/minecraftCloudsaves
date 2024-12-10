from pydrive2.drive import GoogleDrive
from pydrive2.auth import GoogleAuth
import os

def googleDrive(client_secrets, credentials_file='credentials.json'):
    gauth = GoogleAuth()
    gauth.LoadClientConfigFile(client_secrets)

    # Attempt to load saved credentials if they exist
    if os.path.exists(credentials_file):
        gauth.LoadCredentialsFile(credentials_file)

    # If no credentials or expired credentials, perform webserver auth flow
    if not gauth.credentials or gauth.access_token_expired:
        gauth.LocalWebserverAuth()
        gauth.SaveCredentialsFile(credentials_file)

    drive = GoogleDrive(gauth)
    return drive

def testGoogleDrive(logger, client_secrets):
    try:
        drive = googleDrive(client_secrets)
        # Simple test: list root directory files
        drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
        return True
    except Exception as e:
        logger.error(f"Failed to authenticate with Google Drive: {e}", exc_info=True)
        return False

def getGoogleDriveFileList(logger, client_secrets):
    drive = googleDrive(client_secrets)
    file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    logger.info(f"Retrieved {len(file_list)} files from the root directory.")
    return file_list

def getGoogleDriveFolderList(logger, client_secrets):
    drive = googleDrive(client_secrets)
    folder_list = drive.ListFile({'q': "'root' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"}).GetList()
    logger.info(f"Retrieved {len(folder_list)} folders from the root directory.")
    return folder_list
