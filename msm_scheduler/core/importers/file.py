import csv

from ..config import Config

from ..transformers.csv_to_players import CSVToPlayersTransformer
from ..transformers.csv_to_player_availabilities import CSVToPlayerAvailabilitiesTransformer
from ..transformers.csv_to_player_interests import CSVToPlayerInterestsTransformer
from ..transformers.csv_to_player_player_experiences import CSVToPlayerExperiencesTransformer

class FileImporter():

  def __init__(self, config: Config):
    self.config = config

  @property
  def player_availabilities(self):
    with open(self.config.player_availabilities_csv_path, mode='r') as file:
      rows = csv.DictReader(file)
      return CSVToPlayerAvailabilitiesTransformer(rows).tranform()

  @property
  def player_experiences(self):
    with open(self.config.player_experiences_csv_path, mode='r') as file:
      rows = csv.DictReader(file)
      return CSVToPlayerExperiencesTransformer(rows).tranform()

  @property
  def player_interests(self):
    with open(self.config.player_interests_csv_path, mode='r') as file:
      rows = csv.DictReader(file)
      return CSVToPlayerInterestsTransformer(rows).tranform()

  @property
  def player_stats(self):
    with open(self.config.players_csv_path, mode='r') as file:
      rows = csv.DictReader(file)
      return CSVToPlayersTransformer(rows).tranform()

  def get(self):
    return [self.player_stats, self.player_experiences, self.player_interests, self.player_availabilities]