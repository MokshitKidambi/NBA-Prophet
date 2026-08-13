import pandas

# Initializing Files
trad_team_file = "C:\\Users\\kidam\\OneDrive\\Documents\\pythonstuff\\NBA-Prophet\\gear3\\data\\unfiltered\\teams\\traditional\\2025-26_traditional_stats.csv"
adv_team_file = "C:\\Users\\kidam\\OneDrive\\Documents\\pythonstuff\\NBA-Prophet\\gear3\\data\\unfiltered\\teams\\advanced\\2025-26_advanced_stats.csv"

adv_player_file = "C:\\Users\\kidam\\OneDrive\\Documents\\pythonstuff\\NBA-Prophet\\gear3\\data\\unfiltered\\players\\advanced\\2025-26_advanced_stats.csv"
trad_player_file = "C:\\Users\\kidam\\OneDrive\\Documents\\pythonstuff\\NBA-Prophet\\gear3\\data\\unfiltered\\players\\traditional\\2025-26_traditional_stats.csv"

trad_team = pandas.read_csv(trad_team_file)
adv_team = pandas.read_csv(adv_team_file)

trad_player = pandas.read_csv(trad_player_file)
adv_player = pandas.read_csv(adv_player_file)

team_merger = trad_team.merge(adv_team, on = "TEAM_ID", how = "inner", suffixes = ("_trad", "_adv"), validate = "one_to_one")
player_merger = trad_player.merge(adv_player, on = "PLAYER_ID", how = "inner", suffixes = ("_trad", "_adv"), validate = "one_to_one")

same_team_columns = set(trad_team.columns) & set(adv_team.columns)
same_player_columns = set(trad_player.columns) & set(adv_player.columns)

same_team_columns.remove("TEAM_ID")
same_player_columns.remove("PLAYER_ID")

for column in same_team_columns:
    trad_team_column = f"{column}_trad"
    adv_column = f"{column}_adv"

    if team_merger[trad_team_column].equals(team_merger[adv_column]):
        team_merger.rename(columns = {trad_team_column: column}, inplace = True)
        team_merger.drop(columns = [adv_column], inplace = True)

for column in same_player_columns:
    trad_column = f"{column}_trad"
    adv_column = f"{column}_adv"

    if player_merger[trad_column].equals(player_merger[adv_column]):
        player_merger.rename(columns = {trad_column: column}, inplace = True)
        player_merger.drop(columns = [adv_column], inplace = True)

print(player_merger.columns.tolist)
print(player_merger.shape)
print(team_merger.columns.tolist)
print(team_merger.shape)