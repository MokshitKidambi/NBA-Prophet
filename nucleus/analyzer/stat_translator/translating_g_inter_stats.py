import numpy as np
import pandas as pd
from pathlib import Path

class Translating_G_Inter_Stats:
    def __init__(self):
        self.inter_transition_path = Path("g_inter_transitions.csv")
        self.inter_translation_path = Path("inter_translation.csv")
        self.g_translation_path = Path("g_league_translation.csv")
        
        self.MPG_X = ["PRE_NBA_MPG"]
        self.MPG_Y = ["FIRST_VALUABLE_NBA_MPG"]
        
        self.PPG_X = ["PRE_NBA_PPG"]
        self.PPG_Y = ["FIRST_VALUABLE_NBA_PPG"]
        
        self.RPG_X = ["PRE_NBA_RPG"]
        self.RPG_Y = ["FIRST_VALUABLE_NBA_RPG"]
                
        self.APG_X = ["PRE_NBA_APG"]
        self.APG_Y = ["FIRST_VALUABLE_NBA_APG"]
                        
        self.TS_PCT_X = ["PRE_NBA_TS_PCT"]
        self.TS_PCT_Y = ["FIRST_VALUABLE_NBA_TS_PCT"]
                                
        self.USG_PCT_X = ["PRE_NBA_USG_PCT"]
        self.USG_PCT_Y = ["FIRST_VALUABLE_NBA_USG_PCT"]
        
    def differentiating_stats(self):
        inter = pd.read_csv(self.inter_transition_path)
        
        inter["SOURCE"] = "INTERNATIONAL"

        g_league_players = [
            "Jalen Green",
            "Jonathan Kuminga",
            "MarJon Beauchamp",
            "Dyson Daniels",
            "Jaden Hardy",
            "Scoot Henderson",
            "Matas Buzelis",
            "Ronald Holland II"
        ]

        ote_players = [
            "Amen Thompson",
            "Ausar Thompson"
        ]

        inter.loc[
            inter["PLAYER_NAME"].isin(g_league_players),
            "SOURCE"
        ] = "G-LEAGUE"

        inter.loc[
            inter["PLAYER_NAME"].isin(ote_players),
            "SOURCE"
        ] = "OTHER"
        
        international_history = inter[
            inter["SOURCE"] == "INTERNATIONAL"
        ].copy()

        g_league_history = inter[
            inter["SOURCE"] == "G-LEAGUE"
        ].copy()
        
        return international_history, g_league_history
    
    def getting_pre_stats(self):
        inter_hist, g_hist = self.differentiating_stats()
        inter_translated = pd.read_csv(self.inter_translation_path)
        g_translated = pd.read_csv(self.g_translation_path)
        
        pre_nba_cols = [
            "PLAYER_ID",
            "PRE_NBA_SEASON",
            "PRE_NBA_GP",
            "PRE_NBA_MPG",
            "PRE_NBA_PPG",
            "PRE_NBA_RPG",
            "PRE_NBA_APG",
            "PRE_NBA_TS_PCT",
            "PRE_NBA_USG_PCT"
        ]
        
        inter_matched = inter_hist.merge(
            inter_translated[pre_nba_cols],
            on="PLAYER_ID",
            how="inner", validate = "one_to_one"
        )
        
        g_matched = g_hist.merge(
            g_translated[pre_nba_cols],
            on="PLAYER_ID",
            how="inner", validate = "one_to_one"
        )
        
        g_matched.to_csv("g_league_translation.csv")

into = Translating_G_Inter_Stats()
into.getting_pre_stats()
