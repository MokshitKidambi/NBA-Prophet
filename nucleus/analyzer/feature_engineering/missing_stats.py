import pandas as pd
import os
import requests
from pathlib import Path
from nba_api.stats.endpoints import drafthistory

class MissingStats:
    def __init__(self):
        self.player_feature_history_path = Path("C:\\Users\\kidam\\OneDrive\\Documents\\pythonstuff\\NBA-Prophet\\gear3\\data\\features\\player_feature_history.csv")
        self.future_roster_path = Path("C:\\Users\\kidam\\OneDrive\\Documents\\pythonstuff\\NBA-Prophet\\gear4\\data\\rosters\\2026-27_rosters.csv")
        self.roster_stats = pd.DataFrame()
        self.ncaa_translation_path = Path("ncaa_translation_sample.csv")
        
        self.MPG_X = ["PRE_NBA_MPG"]
        self.MPG_Y = ["FIRST_VALUABLE_NBA_MPG"]
        
        self.PPG_X = ["PRE_NBA_PPG"]
        self.PPG_Y = ["FIRST_VALUABLE_NBA_PPG"]
        
        self.RPG_X = ["PRE_NBA_RPG"]
        self.MRPG_Y = ["FIRST_VALUABLE_NBA_RPG"]
                
        self.APG_X = ["PRE_NBA_APG"]
        self.APG_Y = ["FIRST_VALUABLE_NBA_APG"]
                        
        self.TS_PCT_X = ["PRE_NBA_TS_PCT"]
        self.TS_PCT_Y = ["FIRST_VALUABLE_NBA_TS_PCT"]
                                
        self.USG_PCT_X = ["PRE_NBA_USG_PCT"]
        self.USG_PCT_Y = ["FIRST_VALUABLE_NBA_USG_PCT"]

                
    def stats_tracker(self):
                
        rookie_stats = pd.read_csv("rookies.csv")       
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
                    rookie_row = rookie_stats[rookie_stats["PLAYER_ID"] == row["PLAYER_ID"]]
                    no_player_history.append(row)
                    roster_stats.loc[index, "STATUS"] = "NO_HISTORY"
                    if rookie_row.empty:
                        print("ROOKIE NOT FOUND:", row["PLAYER_NAME_x"])
                        continue
                    
                    rookie_row = rookie_row.iloc[0]

                    roster_stats.loc[index, "GP"] = rookie_row["GP"]
                    roster_stats.loc[index, "MPG"] = rookie_row["MPG"]
                    roster_stats.loc[index, "PPG"] = rookie_row["PPG"]
                    roster_stats.loc[index, "TS_PCT"] = rookie_row["TS_PCT"]
                    roster_stats.loc[index, "USG_PCT"] = rookie_row["USG_PCT"]
                    roster_stats.loc[index, "RPG"] = rookie_row["RPG"]
                    roster_stats.loc[index, "APG"] = rookie_row["APG"]

                    roster_stats.loc[index, "STAT_SOURCE"] = rookie_row["ROOKIE_SOURCE"]
                    roster_stats.loc[index, "HAS_IMPUTED_STATS"] = rookie_row["HAS_IMPUTED_STATS"]
                    
                    continue
                player_history = player_history.sort_values(by = "SEASON", ascending = False)
                for new_index, new_row in player_history.iterrows():
                    if pd.notna(new_row["GP"]) and new_row["GP"] > 0:
                        roster_stats.loc[index, "STATUS"] = "SEASONED_PLAYER"

                        stat_year = int(new_row["SEASON"].split("-")[0])
                        new_row["STAT_YEARS_BACK"] = 2025 - stat_year

                        roster_stats.loc[index, "GP"] = new_row["GP"]
                        roster_stats.loc[index, "TOTAL_MINS"] = new_row["TOTAL_MINS"]
                        roster_stats.loc[index, "REB"] = new_row["REB"]
                        roster_stats.loc[index, "AST"] = new_row["AST"]
                        roster_stats.loc[index, "MPG"] = new_row["MPG"]
                        roster_stats.loc[index, "PPG"] = new_row["PPG"]
                        roster_stats.loc[index, "TS_PCT"] = new_row["TS_PCT"]
                        roster_stats.loc[index, "USG_PCT"] = new_row["USG_PCT"]
                        roster_stats.loc[index, "PLUS_MINUS"] = new_row["PLUS_MINUS"]

                        roster_stats.loc[index, "STAT_SOURCE"] = "NBA_FALLBACK"
                        roster_stats.loc[index, "HAS_IMPUTED_STATS"] = False

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
        
        roster_stats["RPG"] = roster_stats["RPG"].fillna(
            roster_stats["REB"] / roster_stats["GP"]
        )

        roster_stats["APG"] = roster_stats["APG"].fillna(
            roster_stats["AST"] / roster_stats["GP"]
        )

        roster_stats["RPG"] = roster_stats["RPG"].round(1)
        roster_stats["APG"] = roster_stats["APG"].round(1)
        
        roster_stats["STAT_SOURCE"] = roster_stats["STAT_SOURCE"].fillna("NBA")
        
        self.roster_stats = roster_stats
    
    def track_first_valuable_NBA_season_data(self):
        roster_stats = self.roster_stats
        player_feature_history = pd.read_csv(self.player_feature_history_path)
        
        college_players = []
        other_org_players = []
        high_school_and_blank_players = []
        combo_draft = []
        for year in range (2017, 2025):
            draft = drafthistory.DraftHistory(season_year_nullable = str(year)).get_data_frames()[0]
            combo_draft.append(draft)
        
        draft_accumulation = pd.concat(combo_draft, ignore_index = True)
        draft_accumulation = draft_accumulation[["PERSON_ID", "PLAYER_NAME", "SEASON", "ORGANIZATION_TYPE"]]
        
        draft_accumulation.rename(columns={"PERSON_ID": "PLAYER_ID", "SEASON": "DRAFT_YEAR"},inplace=True)
        
        draft_accumulation = draft_accumulation[draft_accumulation["PLAYER_NAME"] != "Mitchell Robinson"]
        
        print(draft_accumulation.columns.tolist())
        
        for index, row in draft_accumulation.iterrows():
            if row["ORGANIZATION_TYPE"] == "College/University":
                college_players.append(row)
            elif row["ORGANIZATION_TYPE"] == "Other Team/Club":
                other_org_players.append(row)
            else:
                high_school_and_blank_players.append(row)
        
        ncaa_players = pd.DataFrame(college_players)
        g_international_players = pd.DataFrame(other_org_players)
        unofficial_org_players = pd.DataFrame(high_school_and_blank_players)
        
        ncaa_players = ncaa_players.merge(player_feature_history, on = "PLAYER_ID", how = "left")
        g_international_players = g_international_players.merge(player_feature_history, on = "PLAYER_ID", how = "left")
        unofficial_org_players = unofficial_org_players.merge(player_feature_history, on = "PLAYER_ID", how = "left")
        
        ncaa_players["RPG"] = ncaa_players["REB"] / ncaa_players["GP"]
        
        ncaa_players["APG"] = ncaa_players["AST"] / ncaa_players["GP"]
        
        ncaa_players = ncaa_players.sort_values(by = ["PLAYER_ID", "SEASON"], ascending = True)
        
        ncaa_selected_players = set()
        

        for ncaa_index, ncaa_row in ncaa_players.iterrows():

            if ncaa_row["PLAYER_ID"] in ncaa_selected_players:
                continue
            
            if pd.isna(ncaa_row["SEASON"]):
                continue
            
            n_nba_year = int(ncaa_row["SEASON"].split("-")[0])
            n_draft_year = int(ncaa_row["DRAFT_YEAR"])
            
            if n_nba_year > n_draft_year + 1:
                continue

            if ncaa_row["GP"] >= 20 and ncaa_row["MPG"] >= 10:
                ncaa_players.loc[ncaa_index, "FIRST_VALUABLE_NBA_SEASON"] = ncaa_row["SEASON"]
                ncaa_players.loc[ncaa_index, "FIRST_VALUABLE_NBA_GP"] = ncaa_row["GP"]
                ncaa_players.loc[ncaa_index, "FIRST_VALUABLE_NBA_MPG"] = ncaa_row["MPG"]
                ncaa_players.loc[ncaa_index, "FIRST_VALUABLE_NBA_PPG"] = ncaa_row["PPG"]
                ncaa_players.loc[ncaa_index, "FIRST_VALUABLE_NBA_RPG"] = ncaa_row["RPG"]
                ncaa_players.loc[ncaa_index, "FIRST_VALUABLE_NBA_APG"] = ncaa_row["APG"]
                ncaa_players.loc[ncaa_index, "FIRST_VALUABLE_NBA_TS_PCT"] = ncaa_row["TS_PCT"]
                ncaa_players.loc[ncaa_index, "FIRST_VALUABLE_NBA_USG_PCT"] = ncaa_row["USG_PCT"]

                ncaa_selected_players.add(ncaa_row["PLAYER_ID"])
                
        g_international_players["RPG"] = (g_international_players["REB"] / g_international_players["GP"])
        g_international_players["APG"] = (g_international_players["AST"] / g_international_players["GP"])

        g_international_players = g_international_players.sort_values(by = ["PLAYER_ID", "SEASON"], ascending = True)

        g_international_selected_players = set()

        for g_index, g_row in g_international_players.iterrows():
            if g_row["PLAYER_ID"] in g_international_selected_players:
                continue
            
            if pd.isna(g_row["SEASON"]):
                continue
            
            g_nba_year = int(g_row["SEASON"].split("-")[0])
            g_draft_year = int(g_row["DRAFT_YEAR"])
                        
            if g_nba_year > g_draft_year + 1:
                continue

            if g_row["GP"] >= 20 and g_row["MPG"] >= 10:
                g_international_players.loc[g_index, "FIRST_VALUABLE_NBA_SEASON"] = g_row["SEASON"]
                g_international_players.loc[g_index, "FIRST_VALUABLE_NBA_GP"] = g_row["GP"]
                g_international_players.loc[g_index, "FIRST_VALUABLE_NBA_MPG"] = g_row["MPG"]
                g_international_players.loc[g_index, "FIRST_VALUABLE_NBA_PPG"] = g_row["PPG"]
                g_international_players.loc[g_index, "FIRST_VALUABLE_NBA_RPG"] = g_row["RPG"]
                g_international_players.loc[g_index, "FIRST_VALUABLE_NBA_APG"] = g_row["APG"]
                g_international_players.loc[g_index, "FIRST_VALUABLE_NBA_TS_PCT"] = g_row["TS_PCT"]
                g_international_players.loc[g_index, "FIRST_VALUABLE_NBA_USG_PCT"] = g_row["USG_PCT"]
                
                g_international_selected_players.add(g_row["PLAYER_ID"])
        
        unofficial_org_players["RPG"] = (unofficial_org_players["REB"] / unofficial_org_players["GP"])
        unofficial_org_players["APG"] = (unofficial_org_players["AST"] / unofficial_org_players["GP"])

        unofficial_org_players = unofficial_org_players.sort_values(by = ["PLAYER_ID", "SEASON"], ascending = True)

        unofficial_org_selected_players = set()

        for u_index, u_row in unofficial_org_players.iterrows():
            if u_row["PLAYER_ID"] in unofficial_org_selected_players:
                continue

            if pd.isna(u_row["SEASON"]):
                continue
            
            u_nba_year = int(u_row["SEASON"].split("-")[0])
            u_draft_year = int(u_row["DRAFT_YEAR"])
                        
            if u_nba_year > u_draft_year + 1:
                continue

            if u_row["GP"] >= 20 and u_row["MPG"] >= 10:
                unofficial_org_players.loc[u_index, "FIRST_VALUABLE_NBA_SEASON"] = u_row["SEASON"]
                unofficial_org_players.loc[u_index, "FIRST_VALUABLE_NBA_GP"] = u_row["GP"]
                unofficial_org_players.loc[u_index, "FIRST_VALUABLE_NBA_MPG"] = u_row["MPG"]
                unofficial_org_players.loc[u_index, "FIRST_VALUABLE_NBA_PPG"] = u_row["PPG"]
                unofficial_org_players.loc[u_index, "FIRST_VALUABLE_NBA_RPG"] = u_row["RPG"]
                unofficial_org_players.loc[u_index, "FIRST_VALUABLE_NBA_APG"] = u_row["APG"]
                unofficial_org_players.loc[u_index, "FIRST_VALUABLE_NBA_TS_PCT"] = u_row["TS_PCT"]
                unofficial_org_players.loc[u_index, "FIRST_VALUABLE_NBA_USG_PCT"] = u_row["USG_PCT"]
                
                unofficial_org_selected_players.add(u_row["PLAYER_ID"])
                
        ncaa_transitions = ncaa_players[ncaa_players["FIRST_VALUABLE_NBA_SEASON"].notna()].copy() 
        g_inter_transitions = g_international_players[g_international_players["FIRST_VALUABLE_NBA_SEASON"].notna()].copy()
        
        ncaa_transitions = ncaa_transitions[
            [
                "PLAYER_ID",
                "PLAYER_NAME_x",
                "DRAFT_YEAR",
                "ORGANIZATION_TYPE",

                "FIRST_VALUABLE_NBA_SEASON",
                "FIRST_VALUABLE_NBA_GP",
                "FIRST_VALUABLE_NBA_MPG",
                "FIRST_VALUABLE_NBA_PPG",
                "FIRST_VALUABLE_NBA_RPG",
                "FIRST_VALUABLE_NBA_APG",
                "FIRST_VALUABLE_NBA_TS_PCT",
                "FIRST_VALUABLE_NBA_USG_PCT"
            ]
        ].copy()
        
        ncaa_transitions.rename(columns = {"PLAYER_NAME_x": "PLAYER_NAME"}, inplace = True)
        
        cols_to_round = [
            "FIRST_VALUABLE_NBA_MPG",
            "FIRST_VALUABLE_NBA_PPG",
            "FIRST_VALUABLE_NBA_RPG",
            "FIRST_VALUABLE_NBA_APG"
        ]

        ncaa_transitions[cols_to_round] = ncaa_transitions[cols_to_round].round(1)
        
        ncaa_transitions.to_csv("ncaa_transitions.csv", index = False)
        
        g_inter_transitions = g_inter_transitions[
            [
                "PLAYER_ID",
                "PLAYER_NAME_x",
                "DRAFT_YEAR",
                "ORGANIZATION_TYPE",

                "FIRST_VALUABLE_NBA_SEASON",
                "FIRST_VALUABLE_NBA_GP",
                "FIRST_VALUABLE_NBA_MPG",
                "FIRST_VALUABLE_NBA_PPG",
                "FIRST_VALUABLE_NBA_RPG",
                "FIRST_VALUABLE_NBA_APG",
                "FIRST_VALUABLE_NBA_TS_PCT",
                "FIRST_VALUABLE_NBA_USG_PCT"
            ]
        ].copy()
        
        g_inter_transitions.rename(columns = {"PLAYER_NAME_x": "PLAYER_NAME"}, inplace = True)
        
        cols_to_round = [
            "FIRST_VALUABLE_NBA_MPG",
            "FIRST_VALUABLE_NBA_PPG",
            "FIRST_VALUABLE_NBA_RPG",
            "FIRST_VALUABLE_NBA_APG"
        ]

        g_inter_transitions[cols_to_round] = g_inter_transitions[cols_to_round].round(1)
        
        g_inter_transitions.to_csv("g_inter_transitions.csv", index = False)       
         
    def collect_preNBA_stats(self):
        cbbd_api = os.environ["CBBD_API_KEY"]

        url = "https://api.collegebasketballdata.com/stats/player/season"
        
        headers = {"Authorization": f"Bearer {cbbd_api}"}
        
        college_stat_list = []
        
        for year in range(2017, 2025):
            for attempt in range(3):
                try:
                    response = requests.get(url, headers = headers, params = {"season": year}, timeout=60)
                    response.raise_for_status()

                    college_stats = pd.json_normalize(response.json())
                    college_stat_list.append(college_stats)
                    
                    break

                except requests.exceptions.ReadTimeout:
                    print(f"{year} timed out, attempt {attempt + 1}/3")
        
        new_params = {"season": 2017}

        new_response = requests.get(
            url,
            headers=headers,
            params=new_params,
            timeout=90
        )

        new_response.raise_for_status()

        stats_2017 = pd.json_normalize(new_response.json())
            
        ncaa_stat_list = pd.concat(college_stat_list, ignore_index = True)
        
        ncaa_stat_list["MPG"] = ncaa_stat_list["minutes"] / ncaa_stat_list["games"]
        ncaa_stat_list["PPG"] = ncaa_stat_list["points"] / ncaa_stat_list["games"]
        ncaa_stat_list["RPG"] = ncaa_stat_list["rebounds.total"] / ncaa_stat_list["games"]
        ncaa_stat_list["APG"] = ncaa_stat_list["assists"] / ncaa_stat_list["games"]

        ncaa_stat_list["TS_PCT"] = ncaa_stat_list["trueShootingPct"]
        ncaa_stat_list["USG_PCT"] = ncaa_stat_list["usage"] / 100
        
        ncaa_stat_list = ncaa_stat_list[[
            "season",
            "name",
            "team",
            "games",
            "minutes",
            "points",
            "rebounds.total",
            "assists",
            "trueShootingPct",
            "usage"
        ]].copy()
        
        stats_2017 = stats_2017[
            [
                "season",
                "name",
                "team",
                "games",
                "minutes",
                "points",
                "rebounds.total",
                "assists",
                "trueShootingPct",
                "usage"
            ]
        ]

        ncaa_stat_list = pd.concat(
            [stats_2017, ncaa_stat_list],
            ignore_index=True
        )
        
        ncaa_stat_list.to_csv("ncaa_stat_list.csv", index = False)
        
    def track_preNBA_stats(self):
        ncaa_transitions = pd.read_csv("ncaa_transitions.csv")
        ncaa_stat_list = pd.read_csv("ncaa_stat_list.csv")
        
        name_aliases = {"Omari Spellman": "Omari Rasulala Spellman"}
        ncaa_transitions["PRE_NBA_SEASON"] = ncaa_transitions["DRAFT_YEAR"]
        ncaa_transitions.loc[ncaa_transitions["PLAYER_NAME"] == "De'Anthony Melton", "PRE_NBA_SEASON"] = 2017
        ncaa_transitions["CBBD_NAME"] = (ncaa_transitions["PLAYER_NAME"].replace(name_aliases))
        matched = ncaa_transitions.merge(ncaa_stat_list, left_on=["CBBD_NAME", "PRE_NBA_SEASON"], right_on = ["name", "season"], how = "left")
                
        matched["PRE_NBA_GP"] = matched["games"]

        matched["PRE_NBA_MPG"] = matched["minutes"] / matched["games"]
        matched["PRE_NBA_PPG"] = matched["points"] / matched["games"]
        matched["PRE_NBA_RPG"] = matched["rebounds.total"] / matched["games"]
        matched["PRE_NBA_APG"] = matched["assists"] / matched["games"]

        matched["PRE_NBA_TS_PCT"] = matched["trueShootingPct"]
        matched["PRE_NBA_USG_PCT"] = matched["usage"] / 100
        
        matched[
            [
                "PRE_NBA_MPG",
                "PRE_NBA_PPG",
                "PRE_NBA_RPG",
                "PRE_NBA_APG"
            ]
        ] = matched[
            [
                "PRE_NBA_MPG",
                "PRE_NBA_PPG",
                "PRE_NBA_RPG",
                "PRE_NBA_APG"
            ]
        ].round(1)
        
        matched["PRE_NBA_USG_PCT"] = matched["PRE_NBA_USG_PCT"].round(3)
        
        matched = matched[
            [
                "PLAYER_ID",
                "PLAYER_NAME",
                "DRAFT_YEAR",
                "ORGANIZATION_TYPE",

                "PRE_NBA_SEASON",
                "PRE_NBA_GP",
                "PRE_NBA_MPG",
                "PRE_NBA_PPG",
                "PRE_NBA_RPG",
                "PRE_NBA_APG",
                "PRE_NBA_TS_PCT",
                "PRE_NBA_USG_PCT",

                "FIRST_VALUABLE_NBA_SEASON",
                "FIRST_VALUABLE_NBA_GP",
                "FIRST_VALUABLE_NBA_MPG",
                "FIRST_VALUABLE_NBA_PPG",
                "FIRST_VALUABLE_NBA_RPG",
                "FIRST_VALUABLE_NBA_APG",
                "FIRST_VALUABLE_NBA_TS_PCT",
                "FIRST_VALUABLE_NBA_USG_PCT"
            ]
        ].copy()
        
        matched.to_csv("ncaa_translation_sample.csv", index = False)
                
missing_stats = MissingStats()

missing_stats.track_preNBA_stats()
            