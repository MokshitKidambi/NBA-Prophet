import pandas

# Initializing Data Frames for 2025-26
trad_team_file = "C:\\Users\\kidam\\OneDrive\\Documents\\pythonstuff\\NBA-Prophet\\gear3\\data\\unfiltered\\teams\\traditional\\2025-26_traditional_stats.csv"
adv_team_file = "C:\\Users\\kidam\\OneDrive\\Documents\\pythonstuff\\NBA-Prophet\\gear3\\data\\unfiltered\\teams\\advanced\\2025-26_advanced_stats.csv"

adv_player_file = "C:\\Users\\kidam\\OneDrive\\Documents\\pythonstuff\\NBA-Prophet\\gear3\\data\\unfiltered\\players\\advanced\\2025-26_advanced_stats.csv"
trad_player_file = "C:\\Users\\kidam\\OneDrive\\Documents\\pythonstuff\\NBA-Prophet\\gear3\\data\\unfiltered\\players\\traditional\\2025-26_traditional_stats.csv"

trad_team = pandas.read_csv(trad_team_file)
adv_team = pandas.read_csv(adv_team_file)

trad_player = pandas.read_csv(trad_player_file)
adv_player = pandas.read_csv(adv_player_file)

# Adding SEASON COlUMN
trad_team["SEASON"] = "2025-26"
adv_team["SEASON"] = "2025-26"
trad_player["SEASON"] = "2025-26"
adv_player["SEASON"] = "2025-26"


# MUST KEEP columns
team_identifiers = ["TEAM_ID", "TEAM_NAME"]
player_identifiers = ["PLAYER_ID", "PLAYER_NAME", "TEAM_ID"]

# Dropping _RANK columnns
trad_team_columns = set(trad_team.columns)
adv_team_columns = set(adv_team.columns)

trad_player_columns = set(trad_player.columns)
adv_player_columns = set(adv_player.columns)

trad_player_list = list(trad_player_columns)
adv_player_list = list(adv_player_columns)

trad_team_list = list(trad_player_columns)
adv_team_list = list(adv_player_columns)

trad_team_rank = [column for column in trad_team.columns if column.endswith("_RANK")]
trad_team.drop(columns = trad_team_rank, inplace = True)

trad_player_rank = [column for column in trad_player.columns if column.endswith("_RANK")]
trad_player.drop(columns = trad_player_rank, inplace = True)

adv_team_rank = [column for column in adv_team.columns if column.endswith("_RANK")]
adv_team.drop(columns = adv_team_rank, inplace = True)

adv_player_rank = [column for column in adv_player.columns if column.endswith("_RANK")]
adv_player.drop(columns = adv_player_rank, inplace = True)

# Checking for duplicate rows
adv_team_duplicate = adv_team.drop_duplicates() if adv_team.duplicated().sum() != 0 else adv_team
adv_team = adv_team_duplicate

trad_team_duplicate = trad_team.drop_duplicates() if trad_team.duplicated().sum() != 0 else trad_team
trad_team = trad_team_duplicate

adv_player_duplicate = adv_player.drop_duplicates() if adv_player.duplicated().sum() != 0 else adv_player
adv_player = adv_player_duplicate

trad_player_duplicate = trad_player.drop_duplicates() if trad_player.duplicated().sum() != 0 else trad_player
trad_player = trad_player_duplicate

# Checking for missing identifiers
for items in range(0, len(team_identifiers)):
    if trad_team[team_identifiers[items]].isna().any():
        print(f"{team_identifiers[items]} is missing in Traditional Team")
    if adv_team[team_identifiers[items]].isna().any():
        print(f"{team_identifiers[items]} is missing in Advanced Team")

for items in range(0, len(player_identifiers)):
    if trad_player[player_identifiers[items]].isna().any():
        print(f"{player_identifiers[items]} is missing in Traditional Players")
    if adv_player[player_identifiers[items]].isna().any():
        print(f"{player_identifiers[items]} is missing in Advanced Players")