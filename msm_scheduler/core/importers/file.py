import csv
import os

from ..config import Config

from ..transformers.csv_to_base_teams import CSVToBaseTeamsTransformer
from ..transformers.csv_to_bosses import CSVToBossesTransformer
from ..transformers.csv_to_players import CSVToPlayersTransformer
from ..transformers.csv_to_player_availabilities import CSVToPlayerAvailabilitiesTransformer
from ..transformers.csv_to_player_interests import CSVToPlayerInterestsTransformer
from ..transformers.csv_to_player_player_experiences import CSVToPlayerExperiencesTransformer
from ..transformers.csv_to_player_discord_ids import CSVToPlayerDiscordIdsTransformer
from ..transformers.csv_to_role_config import CSVToRoleConfigTransformer

class FileImporter():

  def __init__(self, config: Config):
    self.config = config

  @property
  def base_teams(self):
    if not os.path.exists(self.config.base_teams_csv_path):
      return []
    
    with open(self.config.base_teams_csv_path, mode='r') as file:
      rows = csv.DictReader(file)
      return CSVToBaseTeamsTransformer(rows).tranform()

  @property
  def bosses(self):
    if not os.path.exists(self.config.bosses_csv_path):
      return []
    
    with open(self.config.bosses_csv_path, mode='r') as file:
      rows = csv.DictReader(file)
      return CSVToBossesTransformer(rows).tranform()

  @property
  def player_availabilities(self):
    if not os.path.exists(self.config.player_availabilities_csv_path):
      return []

    with open(self.config.player_availabilities_csv_path, mode='r') as file:
      rows = csv.DictReader(file)
      return CSVToPlayerAvailabilitiesTransformer(rows).tranform()

  @property
  def player_experiences(self):
    if not os.path.exists(self.config.player_availabilities_csv_path):
      return []

    with open(self.config.player_experiences_csv_path, mode='r') as file:
      rows = csv.DictReader(file)
      return CSVToPlayerExperiencesTransformer(rows).tranform()

  @property
  def player_interests(self):
    if not os.path.exists(self.config.player_interests_csv_path):
      return []

    with open(self.config.player_interests_csv_path, mode='r') as file:
      rows = csv.DictReader(file)
      return CSVToPlayerInterestsTransformer(rows).tranform()

  @property
  def player_stats(self):
    if not os.path.exists(self.config.players_csv_path):
      return []

    with open(self.config.players_csv_path, mode='r') as file:
      rows = csv.DictReader(file)
      return CSVToPlayersTransformer(rows).tranform()

  @property
  def player_discord_ids(self):
    if not os.path.exists(self.config.discord_ids_csv_path):
      return []

    with open(self.config.discord_ids_csv_path, mode='r') as file:
      rows = csv.DictReader(file)
      return CSVToPlayerDiscordIdsTransformer(rows).tranform()

  @property
  def role_configs(self):
    if not hasattr(self.config, 'role_configs_csv_path') or not os.path.exists(self.config.role_configs_csv_path):
      return []
    
    with open(self.config.role_configs_csv_path, mode='r') as file:
      rows = csv.DictReader(file)
      return CSVToRoleConfigTransformer(rows).transform()

  def get(self):
    return [
      self.player_stats, self.player_experiences, self.player_interests, self.player_availabilities, self.player_discord_ids, self.bosses, self.base_teams, self.role_configs
    ]