from pathlib import Path
import pandas
# Stats from season x will help predict the regular seasons wins for season x + 1

class FeatureEngineer:
    def __init__(self):
        self.team_metadata_columns = ["TEAM_ID", "TEAM_NAME", "FEATURE_SEASON", "TARGET_SEASON"]
        self.player_metadata_columns = ["PLAYER_ID", "PLAYER_NAME", "TEAM_ID", "SEASON"]
        self.target_column = "NEXT_SEASON_WIN_PCT"

        self.team_path = Path("C:\\Users\\kidam\\OneDrive\\Documents\\pythonstuff\\NBA-Prophet\\gear3\\data\\filtered\\teams")
        self.player_path = Path("C:\\Users\\kidam\\OneDrive\\Documents\\pythonstuff\\NBA-Prophet\\gear3\\data\\filtered\\players")
        self.feature_path = Path("C:\\Users\\kidam\\OneDrive\\Documents\\pythonstuff\\NBA-Prophet\\gear3\\data\\features")
        
        self.team_scoring_features = ["PPG"]
        self.team_record_features = ["W", "L", "W_PCT"]
        self.team_efficiency_features = ["TS_PCT", "OFF_RATING", "DEF_RATING", "NET_RATING"]
        self.team_possession_features = ["TM_TOV_PCT", "OREB_PCT", "DREB_PCT", "AST_RATIO"]
        self.team_context_features = ["PACE"]

        self.team_model_features = ["NET_RATING", "TM_TOV_PCT", "DREB_PCT", "AST_RATIO", "PACE"]

        self.player_production_features = ["PPG", "REB", "AST"]
        self.player_efficiency_features = ["TS_PCT"]
        self.player_impact_features = ["PLUS_MINUS"]
        self.future_player_impact_features = ["BPM", "VORP"]
        self.player_role_features = ["USG_PCT", "TOTAL_MINS", "MPG" "GP"]
        self.player_availability_features = ["GP", "TOTAL_MINS", "MPG"]

        self.team_features = (self.team_scoring_features + self.team_efficiency_features + self.team_possession_features + self.team_context_features + self.team_record_features)
        self.player_features = (self.player_production_features + self.player_efficiency_features + self.player_impact_features + self.player_role_features + self.player_availability_features)

        self.team_season_files = sorted(self.team_path.iterdir())
        self.player_season_files = sorted(self.player_path.iterdir())

        self.team_training_sim_arena = []
        self.player_feature_history = []

    def remove_dup_features(self):
        self.player_features = list(dict.fromkeys(self.player_features))
        for feature in self.team_features:
            if self.team_features.count(feature) > 1:
                self.team_features.remove(feature)

    def training(self):
        self.remove_dup_features()
        self.team_training_sim_arena = []
        self.player_feature_history = []
        for season in range(len(self.team_season_files) - 1):
            data_file = self.team_season_files[season]
            data_file_reader = pandas.read_csv(data_file)
            target_file = self.team_season_files[season + 1]
            target_file_reader = pandas.read_csv(target_file)

            next_season_info = target_file_reader[["TEAM_ID", "W_PCT"]].copy()
            next_season_info.rename(columns = {"W_PCT": "NEXT_SEASON_WIN_PCT"}, inplace = True)
            team_training_sim = data_file_reader.merge(next_season_info, on = "TEAM_ID", how = "inner", validate = "one_to_one")
            team_training_sim["TARGET_SEASON"] = target_file_reader["SEASON"].iloc[0]
            team_training_sim["PPG"] = team_training_sim["PTS"] / team_training_sim["GP"]
            team_training_sim.rename(columns = {"SEASON": "FEATURE_SEASON"}, inplace = True)

            for columns in team_training_sim.columns:
                if columns in self.team_metadata_columns or columns in self.team_features or columns == self.target_column:
                    continue
                else:
                    team_training_sim.drop(columns = columns, inplace = True)
            self.team_training_sim_arena.append(team_training_sim)

        for season in range(len(self.player_season_files)):
            player_data_file = self.player_season_files[season]
            player_data_file_reader = pandas.read_csv(player_data_file)
            player_data_file_reader["PPG"] = player_data_file_reader["PTS"] / player_data_file_reader["GP"]
            player_data_file_reader.rename(columns = {"MIN_trad": "TOTAL_MINS"}, inplace = True)
            player_data_file_reader.rename(columns = {"MIN_adv": "MPG"}, inplace = True)
        
            for columns in player_data_file_reader.columns:
                if columns in self.player_metadata_columns or columns in self.player_features:
                    continue
                else:
                    player_data_file_reader.drop(columns = columns, inplace = True)
            self.player_feature_history.append(player_data_file_reader)

        team_training_arena = pandas.concat(self.team_training_sim_arena)
        team_training_arena.to_csv(self.feature_path / "training_ground.csv", index = False)

        correlations = team_training_arena[self.team_features + ["NEXT_SEASON_WIN_PCT"]].corr()["NEXT_SEASON_WIN_PCT"]
        corr_matrix = team_training_arena[self.team_features].corr()

        X = team_training_arena[self.team_model_features]
        Y = team_training_arena[self.target_column]

        player_feature_history = pandas.concat(self.player_feature_history)
        player_feature_history.to_csv(self.feature_path / "player_feature_history.csv", index = False)

        print(X.shape)
        print(Y.shape)
        print(X.isna().sum())
        print(Y.isna().sum())
        print(team_training_arena.shape)            

feature = FeatureEngineer()
feature.training()