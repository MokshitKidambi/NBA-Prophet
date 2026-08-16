from pathlib import Path
import pandas

class PredictorV1:
    def __init__(self):
        self.X = ["NET_RATING","TS_PCT", "TM_TOV_PCT", "OREB_PCT", "DREB_PCT", "AST_RATIO", "PACE"]
        self.Y = "NEXT_SEASON_WIN_PCT"

        self.training_ground_path = Path("C:\\Users\\kidam\\OneDrive\\Documents\\pythonstuff\\NBA-Prophet\\gear3\\data\\features\\training_ground.csv")
        self.season = "FEATURE_SEASON"

    def predictor(self):
        training_ground = pandas.read_csv(self.training_ground_path)
        X_data = training_ground[self.X]
        Y_data = training_ground[self.Y]
        season_data = training_ground[self.season]

        train_mask = season_data <= "2021-22"
        test_mask = season_data >= "2022-23"

        X_train = X_data[train_mask]
        Y_train = Y_data[train_mask]

        X_test = X_data[test_mask]
        Y_test = Y_data[test_mask]

 