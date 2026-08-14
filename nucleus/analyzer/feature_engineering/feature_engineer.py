from pathlib import Path
import pandas
# Stats from season x will help predict the regular seasons wins for season x + 1

class FeatureEngineer:
    def __init__(self):
        self.metadata_columns = ["TEAM_ID", "TEAM_NAME", "FEATURE_SEASON", "TARGET_SEASON"]
        self.target_column = "NEXT_SEASON_WINS"

        self.team_path = Path("C:\\Users\\kidam\\OneDrive\\Documents\\pythonstuff\\NBA-Prophet\\gear3\\data\\filtered\\teams")
        self.player_path = Path("C:\\Users\\kidam\\OneDrive\\Documents\\pythonstuff\\NBA-Prophet\\gear3\\data\\filtered\\players")
        self.feature_path = Path("C:\\Users\\kidam\\OneDrive\\Documents\\pythonstuff\\NBA-Prophet\\gear3\\data\\features")
        
        self.team_scoring_features = ["PTS", "OPP_PTS"]
        self.team_record_features = ["W", "L", "W_PCT"]
        self.team_efficiency_features = ["TS_PCT", "OFF_RATING", "DEF_RATING", "NET_RATING"]
        self.team_possession_features = ["TM_TOV_PCT", "OREB_PCT", "DREB_PCT", "AST_RATIO"]
        self.team_context_features = ["PACE"]

        self.player_production_features = ["PTS", "REB", "AST"]
        self.player_efficiency_features = ["TS_PCT"]
        self.player_impact_features = ["PLUS_MINUS"]
        self.future_player_impact_features = ["BPM", "VORP"]
        self.player_role_features = ["USG_PCT", "MIN", "GP"]
        self.player_availability_features = ["GP", "MIN"]

        self.team_features = (self.team_scoring_features + self.team_efficiency_features + self.team_possession_features + self.team_context_features + self.team_record_features)
        self.player_features = (self.player_production_features + self.player_efficiency_features + self.player_impact_features + self.player_role_features + self.player_availability_features)

        self.season_files = sorted(self.team_path.iterdir())
        self.training_sim_arena = []

    def remove_dup_features(self):
        for feature in self.player_features:
            if self.player_features.count(feature) > 1:
                self.player_features.remove(feature)
        for feature in self.team_features:
            if self.team_features.count(feature) > 1:
                self.team_features.remove(feature)

    def training(self):
        index = 0
        for season in range(len(self.season_files) - 1):
            data_file = self.season_files[season]
            data_file_reader = pandas.read_csv(data_file)
            target_file = self.season_files[season + 1]
            target_file_reader = pandas.read_csv(target_file)

            next_season_info = target_file_reader[["TEAM_ID", "W"]].copy()
            next_season_info.rename(columns = {"W": "NEXT_SEASON_WINS"}, inplace = True)
            training_sim = data_file_reader.merge(next_season_info, on = "TEAM_ID", how = "inner", validate = "one_to_one")
            training_sim["TARGET_SEASON"] = target_file_reader["SEASON"].iloc[0]
            training_sim.rename(columns = {"SEASON": "FEATURE_SEASON"}, inplace = True)

            for columns in training_sim.columns:
                if columns in self.metadata_columns or columns in self.team_features or columns == "NEXT_SEASON_WINS" or columns == "SEASON":
                    continue
                else:
                    training_sim.drop(columns = columns, inplace = True)
            self.training_sim_arena.append(training_sim)

            training_arena = pandas.concat(self.training_sim_arena)
            training_arena.to_csv(self.feature_path / "training_ground.csv")
            
feature = FeatureEngineer()
print(feature.training())