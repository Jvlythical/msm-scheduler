import pandas as pd
import numpy as np
import pdb

from sklearn.preprocessing import normalize
from scipy.optimize import curve_fit
from ..core.importers.google_spreadsheet import GoogleSpreadSheetImporter

SHEET_ID = "1B0Yq3AJXZNYVdVV0BpAFWIfRCxL17VsMrnmMxmXePmA"


def model(X, *params):
    # y = a1 x1^b1 + ... + an xn^bn
    n = len(X)
    result = np.zeros_like(X[0])
    for i in range(n):
        a = params[2 * i]
        b = params[2 * i + 1]
        result += a * X[i]**b
    return result


class BossEffectivenessModel():
    def __init__(self):
        self.params = []
        self.norms = np.zeros(0)
        self.Xtrue = np.zeros(0)
        self.ytrue = np.zeros(0)

    def fit(self, sheet_id, sheet_range):
        sheet = GoogleSpreadSheetImporter(sheet_id)
        df = sheet.get(sheet_range)
        df = df.map(lambda x: pd.to_numeric(x, errors='coerce'))
        self.Xtrue = df.iloc[:, :4].values
        self.ytrue = df['Effectiveness'].values

        A_raw = df.to_numpy()
        A, self.norms = normalize(A_raw, return_norm=True, axis=0)

        self.params, _ = curve_fit(model,
                                   (A[:, 0], A[:, 1], A[:, 2], A[:, 3]),
                                   A[:, 4],
                                   p0=np.zeros(8),
                                   maxfev=5000)

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

        experience = experience / self.norms[0]
        difficulty = difficulty / self.norms[1]
        boss_mdc_req = boss_mdc_req / self.norms[2]
        player_mdc = player_mdc / self.norms[3]
        y = model((experience, difficulty, boss_mdc_req, player_mdc), *self.params)
        return self.norms[-1] * y


bem = BossEffectivenessModel()
bem.fit(SHEET_ID, ['Boss Effectiveness!A1:E'])

print(bem.transform(10, 10, 350, 30))
print(bem.transform([10, 10], [10, 10], [350, 350], [30, 45]))


# ========= SCRATCH / PLOTS
# from sklearn.metrics import mean_squared_error
# import matplotlib.pyplot as plt
# # # Import data
# # sheet = GoogleSpreadSheetImporter(SHEET_ID)
# # df = sheet.get(['Boss Effectiveness!A1:G'])
# #
# # # preprocessing
# # label_encoder = LabelEncoder()
# # df['Boss'] = label_encoder.fit_transform(df['Boss'])
# # df = df.applymap(lambda x: pd.to_numeric(x, errors='coerce'))
# #
# # A = df.astype(int).to_numpy()
# # A, norms = normalize(A, return_norm=True)
# # norms = norms[:, np.newaxis]
# # B = norms * A
# # print(B[:5, :])
# #
# #
# # params, cov_mat = curve_fit(model, (A[:, 0], A[:, 1], A[:, 2], A[:, 3]), A[:, 4], p0=np.zeros(8), maxfev=5000)
# # print("-----")
# # be = model((A[:, 0], A[:, 1], A[:, 2], A[:, 3]), *params)
# # be = norms * be[:, np.newaxis]
# #
# # print(be.T)
#
#
# def chatgpt(X):
#     return X[:, 3] / X[:, 2] * X[:, 0] * 525 / X[:, 1]
#
#
# y_chatgpt = chatgpt(bem.Xtrue)
#
# # print(be.T)
# # print(f"curve_fit score = {score_preds(be)}")
#
# plt.subplot(1, 2, 1)
# plt.scatter(bem.ytrue, y_chatgpt)
# plt.title(f'score = {mean_squared_error(bem.ytrue, y_chatgpt)}')
# plt.xlabel('boss effectiveness')
# plt.ylabel('chatgpt values')
# plt.axline([0, 0], slope=1)
#
# plt.subplot(1, 2, 2)
# plt.scatter(bem.ytrue, bem.transform(bem.Xtrue))
# plt.xlabel('boss effectiveness')
# plt.ylabel('curve_fit values')
# plt.axline([0, 0], slope=1)
# plt.show()
