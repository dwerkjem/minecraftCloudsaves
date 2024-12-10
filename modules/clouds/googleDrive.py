from pydrive2.drive import GoogleDrive
from pydrive2.auth import GoogleAuth

def googleDrive(client_secrets):
    gauth = GoogleAuth()
    gauth.LoadClientConfigFile(client_secrets)
    drive = GoogleDrive(gauth)
    return drive

def testGoogleDrive( logger, client_secrets):
    try:
        googleDrive(client_secrets)
        return True
    except Exception as e:
        logger.error(f"Failed to authenticate with Google Drive: {e}")
    return False