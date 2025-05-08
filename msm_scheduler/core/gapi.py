import os
from google.oauth2 import service_account
from msm_scheduler.constants.gapi import SCOPES, CREDENTIALS_FILE_NAME

def get_credentials():
    """Get valid Google API credentials using service account."""
    try:
        return service_account.Credentials.from_service_account_file(
            CREDENTIALS_FILE_NAME,
            scopes=SCOPES
        )
    except Exception as e:
        raise Exception(
            f"Error loading service account credentials from {CREDENTIALS_FILE_NAME}. "
            "Please ensure you have downloaded your service account key file from Google Cloud Console "
            "and placed it at the correct location."
        ) from e 