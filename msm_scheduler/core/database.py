import pdb

from .config import Config
from .importers.file import FileImporter
from .importers.google_spreadsheet import GoogleSpreadSheetImporter

class Database():

    def __init__(self, config: Config):
        self.config = config
        self.player_stats = []
        self.player_experiences = []
        self.player_interests = []
        self.player_availabilities = []

    def load_from_google_spreadsheet(self, spreadsheet_importer: GoogleSpreadSheetImporter = None):
        tables = spreadsheet_importer.get()
        self.load_tables(tables)

    def load_from_file(self, file_importer: FileImporter):
        tables = file_importer.get()
        self.load_tables(tables)

    def load_tables(self, tables: list):
        if tables[0]:
            self.player_stats = tables[0]
        
        if tables[1]:
            self.player_experiences = tables[1]

        if tables[2]:
            self.player_interests = tables[2]

        if tables[3]:
            self.player_availabilities = tables[3]

        if len(tables) > 4:
            self.bosses = tables[4]
            self.base_teams = tables[5]

    @property
    def base_teams(self):
        return self._base_teams

    @base_teams.setter
    def base_teams(self, v):
        self._base_teams = v

    @property
    def bosses(self):
        return self._bosses

    @bosses.setter
    def bosses(self, v):
        self._bosses = v

    @property
    def player_availabilities(self):
        return self._player_availabilities

    @player_availabilities.setter
    def player_availabilities(self, v):
        self._player_availabilities = v

    @property
    def player_experiences(self):
        return self._player_experiences

    @player_experiences.setter
    def player_experiences(self, v):
        self._player_experiences = v 

    @property
    def player_interests(self):
        return self._player_interests

    @player_interests.setter
    def player_interests(self, v):
        self._player_interests = v

    @property
    def player_stats(self):
        return self._player_stats

    @player_stats.setter
    def player_stats(self, v):
        self._player_stats = v