import os
import pandas as pd
import tempfile

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from msm_scheduler.core.importers.file import FileImporter
from msm_scheduler.core.config import Config
from msm_scheduler.core.gapi import get_credentials
from msm_scheduler.constants.gapi import (
    PLAYER_EXPERIENCES, PLAYERS_SPREADSHEET, PLAYER_AVAILABILITY, 
    PLAYER_INTERESTS, PLAYER_DISCORD_IDS, ROLE_CONFIGS
)

SPREADSHEET_COLUMNS = [
    PLAYERS_SPREADSHEET,
    PLAYER_EXPERIENCES,
    PLAYER_INTERESTS,
    PLAYER_AVAILABILITY,
    PLAYER_DISCORD_IDS
]

class GoogleSpreadSheetImporter():
    def __init__(self, sheet_id: str, columns = SPREADSHEET_COLUMNS):
        self.columns = columns
        self.sheet_id = sheet_id

    def get(self):
        config = Config()

        try:
            service = build("sheets", "v4", credentials=get_credentials())

            # Import data
            sheet = service.spreadsheets()

            data_frames = [self._get_google_spreadsheet_range(sheet, col) for col in self.columns]
        except HttpError as err:
            print(err)
            return [[], [], [], [], [], [], [], []]

        df = pd.DataFrame(data_frames[0])
        with tempfile.NamedTemporaryFile(delete=False, mode='w') as tmp:
            config.players_csv_path = tmp.name
            tmp.write(df.to_csv())

        df = pd.DataFrame(data_frames[1])
        with tempfile.NamedTemporaryFile(delete=False, mode='w') as tmp:
            config.player_experiences_csv_path = tmp.name
            tmp.write(df.to_csv())

        df = pd.DataFrame(data_frames[2])
        with tempfile.NamedTemporaryFile(delete=False, mode='w') as tmp:
            config.player_interests_csv_path = tmp.name
            tmp.write(df.to_csv())

        df = pd.DataFrame(data_frames[3])
        with tempfile.NamedTemporaryFile(delete=False, mode='w') as tmp:
            config.player_availabilities_csv_path = tmp.name
            tmp.write(df.to_csv())

        df = pd.DataFrame(data_frames[4])
        with tempfile.NamedTemporaryFile(delete=False, mode='w') as tmp:
            config.discord_ids_csv_path = tmp.name
            tmp.write(df.to_csv())

        if len(data_frames) > 5:
            df = pd.DataFrame(data_frames[5])
            with tempfile.NamedTemporaryFile(delete=False, mode='w') as tmp:
                config.bosses_csv_path = tmp.name
                tmp.write(df.to_csv())

            df = pd.DataFrame(data_frames[6])
            with tempfile.NamedTemporaryFile(delete=False, mode='w') as tmp:
                config.base_teams_csv_path = tmp.name
                tmp.write(df.to_csv())

            df = pd.DataFrame(data_frames[7])
            with tempfile.NamedTemporaryFile(delete=False, mode='w') as tmp:
                config.role_configs_csv_path = tmp.name
                tmp.write(df.to_csv())

        return FileImporter(config).get()

    def _get_google_spreadsheet_range(self, sheet, sheet_range):
        result = sheet.values().get(spreadsheetId=self.sheet_id, range=sheet_range).execute()
        values = result.get("values", [])
        
        if not values:
            return pd.DataFrame()
        
        # Get the header row
        headers = values[0]
        num_cols = len(headers)
        
        # Pad each data row to match header length
        padded_data = []
        for row in values[1:]:
            # Extend row with empty strings if it's shorter than headers
            padded_row = row + [''] * (num_cols - len(row))
            padded_data.append(padded_row)

        return pd.DataFrame(padded_data, columns=headers)

