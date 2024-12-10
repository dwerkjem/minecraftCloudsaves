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

def getGoogleDriveFolderList(logger, client_secrets):
    drive = googleDrive(client_secrets)
    folder_list = drive.ListFile({'q': "'root' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"}).GetList()
    logger.debug(f"Retrieved {len(folder_list)} folders from the root directory.")
    return folder_list

def googleDriveLs(logger, client_secrets, folder):
    drive = googleDrive(client_secrets)
    file_list = drive.ListFile({'q': f"'{folder['id']}' in parents and trashed=false"}).GetList()
    logger.debug(f"Retrieved {len(file_list)} files from the folder '{folder['title']}'.")
    return file_list

def getFolderId(logger, client_secrets, folder_name):
    drive = googleDrive(client_secrets)
    folder_list = drive.ListFile({'q': "'root' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"}).GetList()
    for folder in folder_list:
        if folder['title'] == folder_name:
            logger.debug(f"Found folder '{folder_name}' with ID '{folder['id']}'")
            return folder['id']   
        logger.error(f"Failed to find folder '{folder_name}'")
    return None

def makeFolder(logger, client_secrets, folder_name):
    drive = googleDrive(client_secrets)
    folder = drive.CreateFile({'title': folder_name, 'mimeType': 'application/vnd.google-apps.folder'})
    folder.Upload()
    logger.info(f"Created a new folder '{folder_name}' with ID '{folder['id']}'")
    return folder['id']

def uploadFolder(logger, client_secrets, folder_id, local_folder):
    drive = googleDrive(client_secrets)
    folder = drive.CreateFile({'id': folder_id})
    for root, dirs, files in os.walk(local_folder):
        for file in files:
            file_path = os.path.join(root, file)
            gfile = drive.CreateFile({'title': file, 'parents': [{'id': folder_id}]})
            gfile.SetContentFile(file_path)
            gfile.Upload()
            logger.info(f"Uploaded '{file_path}' to Google Drive")
    logger.info(f"Uploaded all files from '{local_folder}' to Google Drive folder '{folder_id}'")
    return folder_id

def downloadFolder(logger, client_secrets, folder_id, local_folder):
    drive = googleDrive(client_secrets)
    folder = drive.CreateFile({'id': folder_id})
    folder.FetchMetadata()
    folder.GetContentFile(local_folder)
    logger.info(f"Downloaded Google Drive folder '{folder_id}' to '{local_folder}'")
    return folder_id