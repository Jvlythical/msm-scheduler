import os.path
import pandas as pd
import numpy as np

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
SHEET_ID = "1B0Yq3AJXZNYVdVV0BpAFWIfRCxL17VsMrnmMxmXePmA"


def _get_sheet_range(sheet, sheet_range):
    result = sheet.values().get(spreadsheetId=SHEET_ID, range=sheet_range).execute()
    values = result.get("values", [])
    df = pd.DataFrame(values[1:], columns=values[0])
    return df


def import_data():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "application_default_credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("sheets", "v4", credentials=creds)

        # Import data
        sheet = service.spreadsheets()
        df1 = _get_sheet_range(sheet, "Players!A1:F")
        df2 = _get_sheet_range(sheet, "Player Experiences!A1:F")
        df3 = _get_sheet_range(sheet, "Player Interests!A1:F")
        df4 = _get_sheet_range(sheet, "Player Availability!A1:H")

        df = pd.merge(df1, df2, on="Name", how="left")
        df = pd.merge(df, df3, on="Name", how="left",
                      suffixes=(None, "_Interest"))
        df = pd.merge(df, df4, on="Identity", how="left")

        # Clean data
        df["MDC"] = df["Max Damage Cap (in M)"]
        df.dropna(subset=["MDC"], inplace=True)
        df.reset_index(drop=True, inplace=True)
        df["MDC"] = df["MDC"].astype(float)
        df["Bishop"] = df["Class"] == "Bishop"

    except HttpError as err:
        print(err)

    return df
#
# def random_assignment(df):
#     time_slots = ["Mon19", "Tu19"]
#     assignment = []
#
#     in_team_char = np.zeros_like(df["Name"], bool)
#     for time_slot in time_slots:
#         # Check if we can fill a team
#         if sum(df[time_slot] & np.logical_not(in_team_char)) < 10:
#             continue
#         # Assign a bishop to the team
#         team = [int(np.random.choice(np.where(
#                 list(df["Bishop"] & df[time_slot] & np.logical_not(in_team_char)))[0], 1,)[0])]
#         in_team_id = np.zeros_like(df["Name"])
#         in_team_char[team[0]] = True
#         in_team_id[df["Identity"] == df.loc[team[0], "Identity"]] = True
#         while len(team) < 10:
#             lst = np.where(
#                 [
#                     ai and not bi and not ci and not di
#                     for ai, bi, ci, di in zip(
#                         df[time_slot], in_team_id, in_team_char, df["Bishop"]
#                     )
#                 ]
#             )[0]
#             if len(lst) == 0:
#                 break
#             char = int(np.random.choice(lst))
#             if df.loc[char, "Bishop"]:
#                 continue
#             if not in_team_char[char]:
#                 team.append(char)
#                 in_team_char[char] = True
#                 in_team_id[df["Identity"] == df.loc[char, "Identity"]] = True
#         if len(team) == 10:
#             assignment.append(team)
#     mdc = np.array([df.loc[s, "MDC"].sum() for s in assignment])
#     assignment.append(float(sum((mdc - np.mean(mdc)) ** 2)))
#
#     return assignment
#
#
# np.random.seed(19)
#

# def scheduler(df):
#     df["Monday"] = df["Monday"].fillna("")
#     df["Tuesday"] = df["Tuesday"].fillna("")
#     df["Mon19"] = df["Monday"].apply(lambda x: "19" in x)
#     df["Tu19"] = df["Tuesday"].apply(lambda x: "19" in x)
#     df["InTeam"] = False
#
#     df_results = []
#     for i in range(100):
#         assignment = random_assignment(df)
#         if len(assignment) != 3:
#             continue
#         df_results.append(assignment)
#     best_teams = np.argmin([x[2] for x in df_results])
#     df_best = pd.DataFrame(
#         {
#             "Mon19": list(df.loc[df_results[best_teams][0], "Name"]),
#             "MDC1": list(df.loc[df_results[best_teams][0], "MDC"]),
#             "Class1": list(df.loc[df_results[best_teams][0], "Class"]),
#             "Tu19": list(df.loc[df_results[best_teams][1], "Name"]),
#             "MDC2": list(df.loc[df_results[best_teams][1], "MDC"]),
#             "Class2": list(df.loc[df_results[best_teams][1], "Class"]),
#         }
#     )
#     print(df_best)
#
