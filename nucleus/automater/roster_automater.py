import pandas as pd
from nba_api.stats.endpoints import playerindex, commonplayerinfo

current = pd.read_csv(r"C:\Users\kidam\OneDrive\Documents\pythonstuff\NBA-Prophet\Q2\data\rosters\previous_roster.csv")

ncaa_stat_list = pd.read_csv(r"C:\Users\kidam\OneDrive\Documents\pythonstuff\NBA-Prophet\Q2\data\rookie_data\ncaa\ncaa_stat_list.csv")

players = playerindex.PlayerIndex(season = "2026-27").get_data_frames()[0]

players.rename(columns = {
    "PERSON_ID": "PLAYER_ID",
    "ROSTER_STATUS": "ROSTERSTATUS"
    }, inplace = True
)

players["PLAYER_NAME"] = players["PLAYER_FIRST_NAME"] + " " + players["PLAYER_LAST_NAME"]

players["SEASON"] = "2026-27"

for index, row in players.iterrows():
    if row["PLAYER_NAME"] == "Tucker DeVries" or row["PLAYER_NAME"] == "Alpha Diallo" or row["PLAYER_NAME"] == "Bryce Hopkins":
        players.loc[index, "POSITION"] = "F"
    elif row["PLAYER_NAME"] == "Josh Dix" or row["PLAYER_NAME"] == "J'Vonne Hadley" or row["PLAYER_NAME"] == "Jaylin Sellers":
        players.loc[index, "POSITION"] = "G"
    else:
        continue
    
players_raw = players.copy()

no_rookie_row = players_raw[players_raw["PLAYER_ID"].isin([1642966, 1642893])]

for no_index, no_row in no_rookie_row.iterrows():
    
    found_ncaa = False
    
    for ncaa_index, ncaa_row in ncaa_stat_list.iterrows():
        if no_row["COLLEGE"] == ncaa_row["team"]:
            no_rookie_row.loc[no_index, "ROOKIE_SOURCE"] = "NCAA"
            found_ncaa = True
            break
        else:
            continue
    
    if found_ncaa:
        continue
    
    info = commonplayerinfo.CommonPlayerInfo(
        player_id=int(no_row["PLAYER_ID"])
    ).get_data_frames()[0]

    affiliation = info.iloc[0]["LAST_AFFILIATION"]

    affiliation_country = affiliation.split("/")[-1]
    
    if affiliation_country != "USA":
        no_rookie_row.loc[no_index, "ROOKIE_SOURCE"] = "INTERNATIONAL"
    else:
        no_rookie_row.loc[no_index, "ROOKIE_SOURCE"] = "G-LEAGUE"
    
players = players[["TEAM_ID", "PLAYER_ID", "PLAYER_NAME", "ROSTERSTATUS", "SEASON", "POSITION"]].copy()

#players.to_csv(r"C:\Users\kidam\OneDrive\Documents\pythonstuff\NBA-Prophet\Q2\data\rosters\current_roster.csv", index = False)
    
comparison = current.merge(
    players,
    on="PLAYER_ID",
    how="outer",
    suffixes=("_OLD", "_NEW"),
    indicator=True
)

added = comparison[comparison["_merge"] == "right_only"]

removed = comparison[comparison["_merge"] == "left_only"]

both = comparison[comparison["_merge"] == "both"]

team_changes = both[
    both["TEAM_ID_OLD"] != both["TEAM_ID_NEW"]
]

unchanged = both[
    both["TEAM_ID_OLD"] == both["TEAM_ID_NEW"]
]

for col in ["TEAM_ID_OLD", "TEAM_ID_NEW"]:
    comparison[col] = comparison[col].astype("Int64")

added = added.copy()
removed = removed.copy()
team_changes = team_changes.copy()

added["CHANGE_TYPE"] = "ADDED"
removed["CHANGE_TYPE"] = "REMOVED"
team_changes["CHANGE_TYPE"] = "TEAM_CHANGED"

changes = pd.concat(
    [added, removed, team_changes],
    ignore_index=True
)

changes["PLAYER_NAME"] = changes["PLAYER_NAME_NEW"].combine_first(
    changes["PLAYER_NAME_OLD"]
)

for col in ["TEAM_ID_OLD", "TEAM_ID_NEW"]:
    changes[col] = changes[col].astype("Int64")

changes = changes[
    [
        "PLAYER_ID",
        "PLAYER_NAME",
        "CHANGE_TYPE",
        "TEAM_ID_OLD",
        "TEAM_ID_NEW"
    ]
]

#changes.to_csv(r"C:\Users\kidam\OneDrive\Documents\pythonstuff\NBA-Prophet\Q2\data\rosters\roster_changes.csv", index = False)