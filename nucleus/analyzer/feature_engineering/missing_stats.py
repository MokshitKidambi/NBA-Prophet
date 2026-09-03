import pandas as pd
from pathlib import Path
from nba_api.stats.endpoints import commonteamroster
import time

class MissingStats:
    def __init__(self):
        self.player_feature_history_path = Path("C:\\Users\\kidam\\OneDrive\\Documents\\pythonstuff\\NBA-Prophet\\gear3\\data\\features\\player_feature_history.csv")
        self.future_roster_path = Path("C:\\Users\\kidam\\OneDrive\\Documents\\pythonstuff\\NBA-Prophet\\gear4\\data\\rosters\\2026-27_rosters.csv")
        
    def stats_tracker(self):        
        player_feature_history = pd.read_csv(self.player_feature_history_path)
        future_roster = pd.read_csv(self.future_roster_path)
        
        team_ids = future_roster["TEAM_ID"].unique()
        
        all_rosters = []

        for team_id in team_ids:
            try:
                team_roster = commonteamroster.CommonTeamRoster(
                    team_id=team_id,
                    season="2026-27",
                    timeout=60
                ).get_data_frames()[0]

                all_rosters.append(team_roster)

                time.sleep(1)

            except Exception as e:
                print("Failed:", team_id, e)
            
        all_team_rosters = pd.concat(all_rosters, ignore_index = True)
        
        all_team_rosters = all_team_rosters[["PLAYER_ID", "EXP"]]
        
        all_team_rosters = all_team_rosters.drop_duplicates(subset="PLAYER_ID")
        
        current_stats = player_feature_history[player_feature_history["SEASON"] == "2025-26"]
        
        roster_stats = future_roster.merge(current_stats, on = "PLAYER_ID", how = "left")
        
        missing_stats = []
        
        no_player_history = []        
        
        roster_stats = roster_stats.merge(all_team_rosters[["PLAYER_ID", "EXP"]], on = "PLAYER_ID", how = "left")
        
        for index, row in roster_stats.iterrows():
            if row["GP"] == 0 or pd.isna(row["GP"]):
                player_history = player_feature_history[player_feature_history["PLAYER_ID"] == row["PLAYER_ID"]]
                if player_history.empty:
                    no_player_history.append(row)
                    roster_stats.loc[index, "STATUS"] = "NO_HISTORY"
                    if row["EXP"] == "R":
                        roster_stats.loc[index, "ENTRY_TYPE"] = "ROOKIE"
                    continue
                player_history = player_history.sort_values(by = "SEASON", ascending = False)
                for new_index, new_row in player_history.iterrows():
                    if pd.notna(new_row["GP"]) and new_row["GP"] > 0:
                        roster_stats.loc[index, "STATUS"] = "SEASONED_PLAYER"
                        stat_year = int(new_row["SEASON"].split("-")[0])
                        new_row["STAT_YEARS_BACK"] = 2025 - stat_year
                    
                        missing_stats.append(new_row)
                        break
                    else:
                        continue
            else:
                roster_stats.loc[index, "STATUS"] = "NORMAL"
        
        total_missing_stats = pd.DataFrame(missing_stats)
        total_missing_stats.rename(columns={"SEASON": "STAT_SEASON_USED"}, inplace=True)
        
        for other_index, other_row in total_missing_stats.iterrows():
            if other_row["STAT_YEARS_BACK"] == 1:
                total_missing_stats.loc[other_index, "STATUS"] = "RECENT"
                total_missing_stats.loc[other_index, "USE_FALLBACK"] = True
            elif other_row["STAT_YEARS_BACK"] == 2:
                total_missing_stats.loc[other_index, "STATUS"] = "AGING"
                total_missing_stats.loc[other_index, "USE_FALLBACK"] = True
            else:
                total_missing_stats.loc[other_index, "STATUS"] = "STALE"
                total_missing_stats.loc[other_index, "USE_FALLBACK"] = False
        
        no_history_players = pd.DataFrame(no_player_history)
        
        unclassified = roster_stats[(roster_stats["STATUS"] == "NO_HISTORY") &(roster_stats["ENTRY_TYPE"].isna())]

        print(
            roster_stats[
                roster_stats["STATUS"] == "NO_HISTORY"
            ]["ENTRY_TYPE"].value_counts(dropna=False)
        )
        
missing_stats = MissingStats()

missing_stats.stats_tracker()
            
                
        