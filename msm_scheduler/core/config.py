import os
import yaml

FILE_NAME = 'config.yml'

class Config:
  def __init__(self, path: str = None):
      self.path = path or os.path.join(os.getcwd(), FILE_NAME)
      self.load()

      # If the config does not exist, use template
      if not os.path.exists(self.path):
          self._create_default_file()

  @property
  def base_teams_csv_path(self):
    return self._base_teams_csv_path

  @base_teams_csv_path.setter
  def base_teams_csv_path(self, v: str):
    self._base_teams_csv_path = v

  @property
  def bosses_csv_path(self):
    return self._bosses_csv_path

  @bosses_csv_path.setter
  def bosses_csv_path(self, v):
    self._bosses_csv_path = v

  @property
  def gapi_credentials(self):
    return self._gapi_credentials

  @gapi_credentials.setter
  def gapi_credentials(self, v: str):
    self._gapi_credentials = v

  @property
  def player_availabilities_csv_path(self):
    return self._player_availabilities_csv_path
  
  @player_availabilities_csv_path.setter
  def player_availabilities_csv_path(self, v: str):
    self._player_availabilities_csv_path = v

  @property
  def player_experiences_csv_path(self):
    return self._player_experiences_csv_path

  @player_experiences_csv_path.setter
  def player_experiences_csv_path(self, v: str):
    self._player_experiences_csv_path = v

  @property
  def player_interests_csv_path(self):
    return self._player_interests_csv_path

  @player_interests_csv_path.setter
  def player_interests_csv_path(self, v: str):
    self._player_interests_csv_path = v

  @property
  def players_csv_path(self):
    return self._players_csv_path

  @players_csv_path.setter
  def players_csv_path(self, v: str):
    self._players_csv_path = v

  def load(self):
    with open(self.path, 'r') as fp:
      config = yaml.safe_load(fp) or {}
      self.base_teams_csv_path = config.get('base_teams_csv_path') or ''
      self.bosses_csv_path = config.get('bosses_csv_path') or ''
      self.gapi_credentials = config.get('gapi_credentials') or ''
      self.player_availabilities_csv_path = config.get('player_availabilities_csv_path') or ''
      self.player_experiences_csv_path = config.get('player_experiences_csv_path') or ''
      self.player_interests_csv_path = config.get('player_interests_csv_path') or ''
      self.players_csv_path = config.get('players_csv_path') or ''

  def _create_default_file(self):
    with open(self.path, 'w') as fp:
      config = {
        'gapi_credentials': self.gapi_credentials,
        'base_teams_csv_path': self.base_teams_csv_path,
        'bosses_csv_path': self.bosses_csv_path,
        'player_availabilities_csv_path': self.player_availabilities_csv_path,
        'player_experiences_csv_path': self.player_experiences_csv_path,
        'player_interets_csv_path': self.player_interests_csv_path,
        'players_csv_path': self.players_csv_path,
      }
      fp.write(yaml.safe_dump(config))