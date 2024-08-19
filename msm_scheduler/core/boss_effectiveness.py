import os
import pandas as pd
import numpy as np

from sklearn.preprocessing import normalize
from scipy.optimize import curve_fit
from ..core.importers.google_spreadsheet import GoogleSpreadSheetImporter
from ..models import Boss, Player

SHEET_ID = "1B0Yq3AJXZNYVdVV0BpAFWIfRCxL17VsMrnmMxmXePmA"


def model(X, *params):
    n = len(X)
    result = np.zeros_like(X[0])
    for i in range(n):
        a = params[2 * i]
        b = params[2 * i + 1]
        result += a * X[i]**b
    result += params[2*n]
    result += params[2*n + 1] * X[0] * X[3]
    return result


class BossEffectivenessModel():
    # Model only needs to be fit once as the model parameters are cached
    def __init__(self):
        dirname = os.path.dirname(__file__)
        self.save_path = os.path.join(dirname, 'boss_effectiveness_params.npz')

        try:
            # attempt to load model parameters
            loaded_data = np.load(self.save_path)
            self.params = loaded_data['params']
            self.norms = loaded_data['norms']
        except (FileNotFoundError, KeyError, IOError) as e:
            print(f"Error: {e}. Initializing default parameters.")
            self.params = None
            self.norms = None

    def fit(self, sheet_id, sheet_range):
        sheet = GoogleSpreadSheetImporter(sheet_id)
        df = sheet.get(sheet_range)
        df = df.map(lambda x: pd.to_numeric(x, errors='coerce'))

        A_raw = df.to_numpy()
        A, self.norms = normalize(A_raw, return_norm=True, axis=0)
        self.params, _ = curve_fit(model,
                                   (A[:, 0], A[:, 1], A[:, 2], A[:, 3]),
                                   A[:, 4],
                                   p0=np.zeros(11),
                                   maxfev=50000)

        np.savez(self.save_path, params=self.params, norms=self.norms)

    def transform(self, experience, difficulty='', boss_mdc_req='', player_mdc=''):
        if isinstance(experience, (int, float, list)):
            experience = np.array(experience, dtype=np.float64)
            difficulty = np.array(difficulty, dtype=np.float64)
            boss_mdc_req = np.array(boss_mdc_req, dtype=np.float64)
            player_mdc = np.array(player_mdc, dtype=np.float64)
        elif isinstance(experience, np.ndarray):
            mat = experience
            experience = mat[:, 0].astype(np.float64)
            difficulty = mat[:, 1].astype(np.float64)
            boss_mdc_req = mat[:, 2].astype(np.float64)
            player_mdc = mat[:, 3].astype(np.float64)

        if ((1 > experience) | (experience > 10)).any():
            raise ValueError("Experience must be between 1 and 10")
        if ((1 > difficulty) | (difficulty > 10)).any():
            raise ValueError("Difficulty must be between 1 and 10")

        experience = experience / self.norms[0]
        difficulty = difficulty / self.norms[1]
        boss_mdc_req = boss_mdc_req / self.norms[2]
        player_mdc = player_mdc / self.norms[3]
        y = model((experience, difficulty, boss_mdc_req, player_mdc), *self.params)
        y_scaled = self.norms[-1] * y

        # simple transformation to get rid of negatives
        return y_scaled + 30

    def rate(self, player: Player, boss: Boss):
        return self.transform(
            player.boss_experience(boss),
            boss.experience_required if boss.experience_required > 0 else 1,
            boss.total_max_damage_cap_required,
            player.max_damage_cap
        )
