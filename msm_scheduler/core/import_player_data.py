import os.path
import pandas as pd

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from .clean_data import clean_data

SHEET_ID = "1B0Yq3AJXZNYVdVV0BpAFWIfRCxL17VsMrnmMxmXePmA"

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]


def _get_sheet_range(sheet, sheet_range):
    result = sheet.values().get(spreadsheetId=SHEET_ID, range=sheet_range).execute()
    values = result.get("values", [])

    # Add suffix to column names indicating Player Interests (except the 'Name' column)
    if 'Interests' in sheet_range:
        values[0][1:-1] = [x + '_interest' for x in values[0][1:-1]]
    return pd.DataFrame(values[1:], columns=values[0])


def import_player_data(creds=None,
                       columns=['Players!A1:F', 'Player Experiences!A1:F',
                                'Player Interests!A1:F', 'Player Availability!A1:H']):
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "application_default_credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("sheets", "v4", credentials=creds)

        # Import data
        sheet = service.spreadsheets()

        data_frames = [_get_sheet_range(sheet, col) for col in columns]
        df = pd.merge(data_frames[0], data_frames[1], on="Name", how="left")
        df = pd.merge(df, data_frames[2], on="Name", how="left")
        df = pd.merge(df, data_frames[3], on="Identity", how="left")

    except HttpError as err:
        print(err)

    return clean_data(df)
