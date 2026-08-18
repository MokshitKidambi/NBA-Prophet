from pathlib import Path
import pandas
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

class PredictorV1:
    def __init__(self):
        self.X = ["NET_RATING", "TM_TOV_PCT", "DREB_PCT", "AST_RATIO", "PACE"]
        self.Y = "NEXT_SEASON_WIN_PCT"

        self.experiment_features = ["NET_RATING", "TM_TOV_PCT", "DREB_PCT", "AST_RATIO", "PACE"]

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

        model = LinearRegression()

        model.fit(X_train, Y_train)

        prediction = model.predict(X_test)

        mae = mean_absolute_error(Y_test, prediction)

        print(f"MAE: {mae}")

        test_info = training_ground.loc[test_mask, ["TEAM_NAME", "FEATURE_SEASON", "TARGET_SEASON"]]

        result = pandas.DataFrame()

        result["ACTUAL_WIN_PCT"] = Y_test
        result["PREDICTED_WIN_PCT"] = prediction

        result["ACTUAL_WIN_82"] = result["ACTUAL_WIN_PCT"] * 82
        result["PREDICTED_WIN_82"] = result["PREDICTED_WIN_PCT"] * 82

        result["ABSOLUTE_ERROR_82"] = abs(result["ACTUAL_WIN_82"] - result["PREDICTED_WIN_82"])

        result = pandas.concat([test_info, result], axis = 1)

        result = result.sort_values(by = "ABSOLUTE_ERROR_82", ascending = False)

        test_info = test_info.reset_index(drop = True)
        result = result.reset_index(drop = True)

        # print(result.head())

        median_error = result["ABSOLUTE_ERROR_82"].median()
        
        print(f"Median Error: {median_error}")

        naive_prediction = training_ground.loc[test_mask, "W_PCT"]
        naive_mae = mean_absolute_error(Y_test, naive_prediction)

        print(f"Naive MAE: {naive_mae}")
        print(f"Naive MAE Wins: {naive_mae * 82}")

        simple_prediction = [0.500] * len(Y_test)

        simple_mae = mean_absolute_error(Y_test, simple_prediction)

        print(f"Simple MAE: {simple_mae}")
        print(f"Simple MAE Wins: {simple_mae * 82}")

    def experiment_predictor(self):
            training_ground = pandas.read_csv(self.training_ground_path)
            X_data = training_ground[self.experiment_features]
            Y_data = training_ground[self.Y]
            season_data = training_ground[self.season]
    
            train_mask = season_data <= "2021-22"
            test_mask = season_data >= "2022-23"
    
            X_train = X_data[train_mask]
            Y_train = Y_data[train_mask]
    
            X_test = X_data[test_mask]
            Y_test = Y_data[test_mask]
    
            model = LinearRegression()
    
            model.fit(X_train, Y_train)
    
            prediction = model.predict(X_test)
    
            mae = mean_absolute_error(Y_test, prediction)
    
            print(f"MAE: {mae}")
    
            test_info = training_ground.loc[test_mask, ["TEAM_NAME", "FEATURE_SEASON", "TARGET_SEASON"]]
    
            result = pandas.DataFrame()
    
            result["ACTUAL_WIN_PCT"] = Y_test
            result["PREDICTED_WIN_PCT"] = prediction
    
            result["ACTUAL_WIN_82"] = result["ACTUAL_WIN_PCT"] * 82
            result["PREDICTED_WIN_82"] = result["PREDICTED_WIN_PCT"] * 82
    
            result["ABSOLUTE_ERROR_82"] = abs(result["ACTUAL_WIN_82"] - result["PREDICTED_WIN_82"])
    
            result = pandas.concat([test_info, result], axis = 1)
    
            result = result.sort_values(by = "ABSOLUTE_ERROR_82", ascending = False)
    
            test_info = test_info.reset_index(drop = True)
            result = result.reset_index(drop = True)
    
            print(result.head())
    
            median_error = result["ABSOLUTE_ERROR_82"].median()
            
            print(f"Median Error: {median_error}")
    
            naive_prediction = training_ground.loc[test_mask, "W_PCT"]
            naive_mae = mean_absolute_error(Y_test, naive_prediction)
    
            print(f"Naive MAE: {naive_mae}")
            print(f"Naive MAE Wins: {naive_mae * 82}")
    
            simple_prediction = [0.500] * len(Y_test)
    
            simple_mae = mean_absolute_error(Y_test, simple_prediction)
    
            print(f"Simple MAE: {simple_mae}")
            print(f"Simple MAE Wins: {simple_mae * 82}")


predictor = PredictorV1()
predictor.experiment_predictor()


 