import os
import pandas as pd

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from ..transformers.google_spreadsheet import GoogleSpreadSheetTransformer
from ...constants.gapi import CREDENTIALS_FILE_NAME, SCOPES

SHEET_ID = "1B0Yq3AJXZNYVdVV0BpAFWIfRCxL17VsMrnmMxmXePmA"


class GoogleSpreadSheetImporter():

    def __init__(self, sheet_id: str = SHEET_ID):
        self.google_spreadsheet_columns = [
            'Players!A1:F',
            'Player Experiences!A1:F',
            'Player Interests!A1:F',
            'Player Availability!A1:H'
        ]
        self.sheet_id = sheet_id

    @property
    def gapi_credentials(self):
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(CREDENTIALS_FILE_NAME):
            creds = Credentials.from_authorized_user_file(CREDENTIALS_FILE_NAME, SCOPES)
        else:
            creds = None

        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(CREDENTIALS_FILE_NAME, "w") as token:
                token.write(creds.to_json())

        return creds

    def get(self, columns=None):
        columns = columns or self.google_spreadsheet_columns
        try:
            service = build("sheets", "v4", credentials=self.gapi_credentials)

            # Import data
            sheet = service.spreadsheets()

            if len(columns) == 1:
                return self._get_google_spreadsheet_range(sheet, columns[0])

            data_frames = [self._get_google_spreadsheet_range(sheet, col) for col in columns]

            df = pd.merge(data_frames[0], data_frames[1], on="Name", how="left")
            df = pd.merge(df, data_frames[2], on="Name", how="left")
            df = pd.merge(df, data_frames[3], on="Identity", how="left")
        except HttpError as err:
            print(err)
            return [[], [], [], []]

        return GoogleSpreadSheetTransformer(df).transform()

    def _get_google_spreadsheet_range(self, sheet, sheet_range):
        result = sheet.values().get(spreadsheetId=self.sheet_id, range=sheet_range).execute()
        values = result.get("values", [])

        # Add suffix to column names indicating Player Interests (except the 'Name' column)
        if 'Interests' in sheet_range:
            values[0][1:] = [x + '_interest' for x in values[0][1:]]
        return pd.DataFrame(values[1:], columns=values[0])
