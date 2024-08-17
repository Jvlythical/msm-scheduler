from .importers.google_spreadsheet import GoogleSpreadSheetImporter

class Database():

    def __init__(self, spreadsheet_importer: GoogleSpreadSheetImporter = None):
        self.tables = [[], [], [], []]
        if spreadsheet_importer:
            self.tables = spreadsheet_importer.get()

        self.player_stats = self.tables[0]
        self.player_experiences = self.tables[1]
        self.player_interests = self.tables[2]
        self.player_availabilities = self.tables[3]

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