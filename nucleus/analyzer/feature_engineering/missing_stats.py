import pandas as pd
from pathlib import Path

class MissingStats:
    def __init__(self):
        self.player_feature_history_path = Path("C:\\Users\\kidam\\OneDrive\\Documents\\pythonstuff\\NBA-Prophet\\gear3\\data\\features\\player_feature_history.csv")
        self.future_roster_path = Path("C:\\Users\\kidam\\OneDrive\\Documents\\pythonstuff\\NBA-Prophet\\gear4\\data\\rosters\\2026-27_rosters.csv")
                
    def stats_tracker(self):        
        player_feature_history = pd.read_csv(self.player_feature_history_path)
        future_roster = pd.read_csv(self.future_roster_path)
        
        current_stats = player_feature_history[player_feature_history["SEASON"] == "2025-26"]
        
        roster_stats = future_roster.merge(current_stats, on = "PLAYER_ID", how = "left")
        
        missing_stats = []
        
        no_player_history = []   
                
        for index, row in roster_stats.iterrows():
            if row["GP"] == 0 or pd.isna(row["GP"]):
                player_history = player_feature_history[player_feature_history["PLAYER_ID"] == row["PLAYER_ID"]]
                if player_history.empty:
                    no_player_history.append(row)
                    roster_stats.loc[index, "STATUS"] = "NO_HISTORY"
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
        
        # no_history_players = pd.DataFrame(no_player_history)

        # no_history_players = no_history_players[
        #     [
        #         "TEAM_ID_x",
        #         "PLAYER_ID",
        #         "PLAYER_NAME_x"
        #     ]
        # ]

        # no_history_players.to_csv("rookies.csv", index=False)
        
        entry_types = pd.read_csv("rookies.csv")
        
        entry_types.loc[entry_types["ROOKIE_SOURCE"] == "OTHER", "ROOKIE_SOURCE"] = "G-LEAGUE"
        
        entry_types.to_csv("rookies.csv", index = False)
        
                                        
missing_stats = MissingStats()

missing_stats.stats_tracker()
            