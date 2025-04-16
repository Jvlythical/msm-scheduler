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
        self.player_discord_ids = []
        self.bosses = []
        self.base_teams = []
        self.role_configs = []

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

        if tables[4]:
            self.player_discord_ids = tables[4]

        if len(tables) > 5:
            self.bosses = tables[5]
            self.base_teams = tables[6]
            self.role_configs = tables[7]

    def right_merge_tables(self, tables: list):
        if tables[0]:
            self.right_merge_player_stats(tables[0])
        
        if tables[1]:
            self.right_merge_player_experiences(tables[1])

        if tables[2]:
            self.right_merge_player_interests(tables[2])

        if tables[3]:
            self.right_merge_player_availabilities(tables[3])

        if tables[4]:
            self.right_merge_player_discord_ids(tables[4])

        if len(tables) > 5:
            self.right_merge_bosses(tables[5])
            self.right_merge_base_teams(tables[6])
            self.right_merge_role_configs(tables[7])

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

    @property
    def role_configs(self):
        return self._role_configs

    @role_configs.setter
    def role_configs(self, v):
        self._role_configs = v

    def right_merge_bosses(self, bosses: list):
        self.right_merge(self.bosses, bosses, lambda row: row['name'])

    def right_merge_base_teams(self, base_teams: list):
        self.right_merge(self.base_teams, base_teams, lambda row: row['time'])

    def right_merge_player_availabilities(self, player_availabilities: list):
        self.right_merge(self.player_availabilities, player_availabilities, lambda row: row['identity'])

    def right_merge_player_experiences(self, player_experiences: list):
        self.right_merge(self.player_experiences, player_experiences, lambda row: row['name'])

    def right_merge_player_interests(self, player_interests: list):
        self.right_merge(self.player_interests, player_interests, lambda row: row['name'])

    def right_merge_player_stats(self, player_stats: list):
        self.right_merge(self.player_stats, player_stats, lambda row: row['name'])

    def right_merge_player_discord_ids(self, player_discord_ids: list):
        self.right_merge(self.player_discord_ids, player_discord_ids, lambda row: row['identity'])

    def right_merge_role_configs(self, role_configs: list):
        self.right_merge(self.role_configs, role_configs, lambda row: row['role_name'])

    def right_merge(self, table1: list, table2: list, get_key = None):
        index = {}

        i = 0
        for row in table1:
            key = get_key(row) if callable(get_key) else row[0]
            index[key] = i
            i += 1

        new_rows = []
        for row in table2:
            key = get_key(row) if callable(get_key) else row[0]
            if not index.get(key):
                new_rows.append(row)
                continue
            table1[index.get(key)] = row

        table1 += new_rows
