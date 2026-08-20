from pathlib import Path
import pandas
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

class PredictorV1:
    def __init__(self):
        self.X = ["NET_RATING", "TM_TOV_PCT", "DREB_PCT", "AST_RATIO", "PACE", "NET_PPG_CHANGE", "RETAINED_MINUTES", "ROSTER_AVAILABILITY", "NET_SCORING_LOAD", "NET_EFFICIENCY_LOAD", "NET_USAGE_LOAD", "NET_PLUS_MINUS_LOAD"]
        self.dummyX = ["NET_RATING", "TM_TOV_PCT", "DREB_PCT", "AST_RATIO", "PACE", "NET_PPG_CHANGE", "RETAINED_MINUTES", "ROSTER_AVAILABILITY"]
        self.Y = "NEXT_SEASON_WIN_PCT"

        self.team_experiment_features = ["NET_RATING", "TM_TOV_PCT", "DREB_PCT", "AST_RATIO", "PACE"]
        self.player_experiment_features = ["PPG", "TS_PCT","USG_PCT", "MPG", "TOTAL_MINS", "GP", "PLUS_MINUS"]

        self.team_training_ground_path = Path("C:\\Users\\kidam\\OneDrive\\Documents\\pythonstuff\\NBA-Prophet\\gear3\\data\\features\\training_ground.csv")
        self.player_feature_history = Path("C:\\Users\\kidam\\OneDrive\\Documents\\pythonstuff\\NBA-Prophet\\gear3\\data\\features\\player_feature_history.csv")
        self.season = "FEATURE_SEASON"

        self.team_id_list = ["1610612737", "1610612738", "1610612766", "1610612741", ""]

    def experiment_predictor(self):
        team_training_ground = pandas.read_csv(self.team_training_ground_path)
        player_feature_history = pandas.read_csv(self.player_feature_history)

        team_ppg = (player_feature_history.groupby(["TEAM_ID", "SEASON"], as_index=False)["PPG"].sum())

        team_ppg.rename(columns={"PPG": "ROSTER_PPG_SUM"}, inplace=True)

        team_plusminus = (player_feature_history.groupby(["TEAM_ID", "SEASON"], as_index=False)["PLUS_MINUS"].sum())

        player_feature_history["TS_WEIGHTED"] = (
            player_feature_history["TS_PCT"] *
            player_feature_history["TOTAL_MINS"]
        )

        player_feature_history["USG_WEIGHTED"] = (
            player_feature_history["USG_PCT"] *
            player_feature_history["TOTAL_MINS"]
        )

        team_ts = (player_feature_history.groupby(["TEAM_ID", "SEASON"], as_index = False)["TS_WEIGHTED"].sum())
        team_usg = (player_feature_history.groupby(["TEAM_ID", "SEASON"], as_index = False)["USG_WEIGHTED"].sum())

        player_team_features = team_ppg.merge(
            team_plusminus,
            on=["TEAM_ID", "SEASON"],
            how="inner"
        )

        player_team_features = player_team_features.merge(
            team_ts,
            on=["TEAM_ID", "SEASON"],
            how="inner"
        )

        player_team_features = player_team_features.merge(
            team_usg,
            on=["TEAM_ID", "SEASON"],
            how="inner"
        )
        
        player_team_seasons = (player_feature_history.groupby(["TEAM_ID", "SEASON"], as_index = False))

        roster = {}

        for (team_id, season), group in player_team_seasons:
            roster[(team_id, season)] = set(group["PLAYER_ID"])

        seasons = sorted(player_feature_history["SEASON"].unique())

        returning_list = []
        outgoing_list = []
        incoming_list = []

        for i in range(len(seasons) - 1):
            old_season = seasons[i]
            new_season = seasons[i + 1]

            for team_id in player_feature_history[player_feature_history["SEASON"] == old_season]["TEAM_ID"].unique():

                old_key = (team_id, old_season)
                new_key = (team_id, new_season)

                if new_key not in roster:
                    continue

                old_roster = roster[old_key]
                new_roster = roster[new_key]

                returning = old_roster & new_roster
                outgoing = old_roster - new_roster
                incoming = new_roster - old_roster

                returning_list.append(returning)
                outgoing_list.append(outgoing)
                incoming_list.append(incoming)

        X_data = team_training_ground[self.X]
        Y_data = team_training_ground[self.Y]
        season_data = team_training_ground[self.season]

        train_mask = season_data < "2023-24"
        test_mask = season_data == "2023-24"

        X_train = X_data[train_mask]
        Y_train = Y_data[train_mask]

        X_test = X_data[test_mask]
        Y_test = Y_data[test_mask]

        model = LinearRegression()

        model.fit(X_train, Y_train)

        prediction = model.predict(X_test)

        mae = mean_absolute_error(Y_test, prediction)

        print(f"MAE: {mae}")

        test_info = team_training_ground.loc[test_mask, ["TEAM_NAME", "FEATURE_SEASON", "TARGET_SEASON"]]

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

        median_error = result["ABSOLUTE_ERROR_82"].median()
        
        print(f"Median Error: {median_error}")

        naive_prediction = team_training_ground.loc[test_mask, "W_PCT"]
        naive_mae = mean_absolute_error(Y_test, naive_prediction)

        print(f"Naive MAE: {naive_mae}")
        print(f"Naive MAE Wins: {naive_mae * 82}")

        simple_prediction = [0.500] * len(Y_test)

        simple_mae = mean_absolute_error(Y_test, simple_prediction)

        print(f"Simple MAE: {simple_mae}")
        print(f"Simple MAE Wins: {simple_mae * 82}")

        print(result.head())

    def predict_season(self, test_season):
        training_ground = pandas.read_csv(self.team_training_ground_path)
        player_feature_history = pandas.read_csv(self.player_feature_history)
        team_ppg = (player_feature_history.groupby(["TEAM_ID", "SEASON"], as_index=False)["PPG"].sum())

        team_ppg.rename(columns={"PPG": "ROSTER_PPG_SUM"}, inplace=True)

        team_plusminus = (player_feature_history.groupby(["TEAM_ID", "SEASON"], as_index=False)["PLUS_MINUS"].sum())

        player_feature_history["TS_WEIGHTED"] = (
            player_feature_history["TS_PCT"] *
            player_feature_history["TOTAL_MINS"]
        )

        player_feature_history["USG_WEIGHTED"] = (
            player_feature_history["USG_PCT"] *
            player_feature_history["TOTAL_MINS"]
        )

        team_ts = (player_feature_history.groupby(["TEAM_ID", "SEASON"], as_index = False)["TS_WEIGHTED"].sum())
        team_usg = (player_feature_history.groupby(["TEAM_ID", "SEASON"], as_index = False)["USG_WEIGHTED"].sum())

        player_team_features = team_ppg.merge(
            team_plusminus,
            on=["TEAM_ID", "SEASON"],
            how="inner"
        )

        player_team_features = player_team_features.merge(
            team_ts,
            on=["TEAM_ID", "SEASON"],
            how="inner"
        )

        player_team_features = player_team_features.merge(
            team_usg,
            on=["TEAM_ID", "SEASON"],
            how="inner"
        )

        player_team_seasons = (player_feature_history.groupby(["TEAM_ID", "SEASON"], as_index = False))

        player_feature_history["SCORING_LOAD"] = player_feature_history["PPG"] * player_feature_history["MPG"]
        
        player_feature_history["EFFICIENCY_LOAD"] = player_feature_history["TS_PCT"] * player_feature_history["MPG"]
        
        player_feature_history["USAGE_LOAD"] = player_feature_history["USG_PCT"] * player_feature_history["MPG"]
                
        player_feature_history["PLUS_MINUS_LOAD"] =player_feature_history["PLUS_MINUS"] * player_feature_history["MPG"]

        roster = {}

        roster_changes = []

        for (team_id, season), group in player_team_seasons:
            roster[(team_id, season)] = set(group["PLAYER_ID"])

        seasons = sorted(player_feature_history["SEASON"].unique())

        for i in range(len(seasons) - 1):
            old_season = seasons[i]
            new_season = seasons[i + 1]

            for team_id in player_feature_history[player_feature_history["SEASON"] == old_season]["TEAM_ID"].unique():

                old_key = (team_id, old_season)
                new_key = (team_id, new_season)

                if new_key not in roster:
                    continue

                old_roster = roster[old_key]
                new_roster = roster[new_key]

                returning = old_roster & new_roster
                outgoing = old_roster - new_roster
                incoming = new_roster - old_roster

                roster_changes.append({
                    "TEAM_ID": team_id,
                    "OLD_SEASON": old_season,
                    "NEW_SEASON": new_season,
                    "RETURNING": returning,
                    "OUTGOING": outgoing,
                    "INCOMING": incoming
                })

        roster_changes = pandas.DataFrame(roster_changes)

        for index, row in roster_changes.iterrows():

            SEASON = row["OLD_SEASON"]
            outgoing_players = row["OUTGOING"]
            returning_players = row["RETURNING"]
            incoming_players = row["INCOMING"]
            TEAM_ID = row["TEAM_ID"]

            outgoing_stats = player_feature_history[
                (player_feature_history["SEASON"] == SEASON) &
                (player_feature_history["PLAYER_ID"].isin(outgoing_players))
            ]

            returning_stats = player_feature_history[
                (player_feature_history["SEASON"] == SEASON) &
                (player_feature_history["PLAYER_ID"].isin(returning_players))
            ]

            incoming_stats = player_feature_history[
                (player_feature_history["SEASON"] == SEASON) &
                (player_feature_history["PLAYER_ID"].isin(incoming_players))
            ]

            team_stats = training_ground[(training_ground["FEATURE_SEASON"] == SEASON) & (training_ground["TEAM_ID"] == TEAM_ID)]
            old_team_stats = player_feature_history[(player_feature_history["SEASON"] == SEASON) & (player_feature_history["TEAM_ID"] == TEAM_ID)]

            outgoing_ppg = outgoing_stats["PPG"].sum()
            outgoing_total_mins = outgoing_stats["TOTAL_MINS"].sum()

            roster_changes.loc[index, "OUTGOING_PPG"] = outgoing_ppg
            roster_changes.loc[index, "OUTGOING_TOTAL_MINS"] = outgoing_total_mins

            outgoing_scoring_load = outgoing_stats["SCORING_LOAD"].sum()
            roster_changes.loc[index, "OUTGOING_SCORING_LOAD"] = outgoing_scoring_load

            outgoing_efficiency_load = outgoing_stats["EFFICIENCY_LOAD"].sum()
            roster_changes.loc[index, "OUTGOING_EFFICIENCY_LOAD"] = outgoing_efficiency_load

            outgoing_plus_minus_load = outgoing_stats["PLUS_MINUS_LOAD"].sum()
            roster_changes.loc[index, "OUTGOING_PLUS_MINUS_LOAD"] = outgoing_plus_minus_load

            outgoing_usage_load = outgoing_stats["USAGE_LOAD"].sum()
            roster_changes.loc[index, "OUTGOING_USAGE_LOAD"] = outgoing_usage_load            

            returning_ppg = returning_stats["PPG"].sum()
            returning_total_mins = returning_stats["TOTAL_MINS"].sum()

            roster_changes.loc[index, "RETURNING_PPG"] = returning_ppg
            roster_changes.loc[index, "RETURNING_TOTAL_MINS"] = returning_total_mins

            returning_scoring_load = incoming_stats["SCORING_LOAD"].sum()
            roster_changes.loc[index, "RETURNING_SCORING_LOAD"] = returning_scoring_load

            returning_efficiency_load = outgoing_stats["EFFICIENCY_LOAD"].sum()
            roster_changes.loc[index, "RETURNING_EFFICIENCY_LOAD"] = returning_efficiency_load

            returning_plus_minus_load = outgoing_stats["PLUS_MINUS_LOAD"].sum()
            roster_changes.loc[index, "RETURNING_PLUS_MINUS_LOAD"] = returning_plus_minus_load

            returning_usage_load = outgoing_stats["USAGE_LOAD"].sum()
            roster_changes.loc[index, "RETURNING_USAGE_LOAD"] = returning_usage_load

            incoming_ppg = incoming_stats["PPG"].sum()
            incoming_total_mins = incoming_stats["TOTAL_MINS"].sum()

            roster_changes.loc[index, "INCOMING_PPG"] = incoming_ppg
            roster_changes.loc[index, "INCOMING_TOTAL_MINS"] = incoming_total_mins

            incoming_scoring_load = incoming_stats["SCORING_LOAD"].sum()
            roster_changes.loc[index, "INCOMING_SCORING_LOAD"] = incoming_scoring_load

            incoming_efficiency_load = incoming_stats["EFFICIENCY_LOAD"].sum()
            roster_changes.loc[index, "INCOMING_EFFICIENCY_LOAD"] = incoming_efficiency_load

            incoming_plus_minus_load = incoming_stats["PLUS_MINUS_LOAD"].sum()
            roster_changes.loc[index, "INCOMING_PLUS_MINUS_LOAD"] = incoming_plus_minus_load

            incoming_usage_load = incoming_stats["USAGE_LOAD"].sum()
            roster_changes.loc[index, "INCOMING_USAGE_LOAD"] = incoming_usage_load              

            team_gp = (team_stats["W"] + team_stats["L"]).iloc[0]
            old_team_stats = old_team_stats.copy()

            old_team_stats["PLAYER_AVAILABILITY"] = (old_team_stats["GP"] / team_gp)

            old_team_stats["WEIGHTED_AVAILABILITY"] = (old_team_stats["PLAYER_AVAILABILITY"] * old_team_stats["TOTAL_MINS"])

            roster_availability = (old_team_stats["WEIGHTED_AVAILABILITY"].sum() / old_team_stats["TOTAL_MINS"].sum())

            roster_changes.loc[index, "ROSTER_AVAILABILITY"] = roster_availability
        
        roster_changes["NET_PPG_CHANGE"] = roster_changes["INCOMING_PPG"] - roster_changes["OUTGOING_PPG"]
        
        roster_changes["RETAINED_MINUTES"] = roster_changes["RETURNING_TOTAL_MINS"] / (roster_changes["RETURNING_TOTAL_MINS"] + roster_changes["OUTGOING_TOTAL_MINS"])

        roster_changes["NET_SCORING_LOAD"] = roster_changes["INCOMING_SCORING_LOAD"] - roster_changes["OUTGOING_SCORING_LOAD"]
        roster_changes["NET_EFFICIENCY_LOAD"] = roster_changes["INCOMING_EFFICIENCY_LOAD"] - roster_changes["OUTGOING_EFFICIENCY_LOAD"]
        roster_changes["NET_USAGE_LOAD"] = roster_changes["INCOMING_USAGE_LOAD"] - roster_changes["OUTGOING_USAGE_LOAD"]
        roster_changes["NET_PLUS_MINUS_LOAD"] = roster_changes["INCOMING_PLUS_MINUS_LOAD"] - roster_changes["OUTGOING_PLUS_MINUS_LOAD"]

        merge = training_ground.merge(
                roster_changes[[
                    "TEAM_ID",
                    "OLD_SEASON",
                    "NET_PPG_CHANGE",
                    "RETAINED_MINUTES",
                    "ROSTER_AVAILABILITY",

                    "NET_SCORING_LOAD",
                    "NET_EFFICIENCY_LOAD",
                    "NET_USAGE_LOAD",
                    "NET_PLUS_MINUS_LOAD",

                    "RETURNING_SCORING_LOAD",
                    "RETURNING_EFFICIENCY_LOAD",
                    "RETURNING_USAGE_LOAD",
                    "RETURNING_PLUS_MINUS_LOAD",

                    "INCOMING_SCORING_LOAD",
                    "INCOMING_EFFICIENCY_LOAD",
                    "INCOMING_USAGE_LOAD",
                    "INCOMING_PLUS_MINUS_LOAD",

                    "OUTGOING_SCORING_LOAD",
                    "OUTGOING_EFFICIENCY_LOAD",
                    "OUTGOING_USAGE_LOAD",
                    "OUTGOING_PLUS_MINUS_LOAD"                    
                ]], left_on=["TEAM_ID", "FEATURE_SEASON"], right_on=["TEAM_ID", "OLD_SEASON"], how="inner", validate="one_to_one")

        merge.drop(columns = ["OLD_SEASON"], inplace = True)

        X_data = merge[self.X]
        Y_data = merge[self.Y]
        season_data = merge[self.season]
         
        train_mask = season_data < test_season
        test_mask = season_data == test_season
         
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
         
        print(result.head())

    def take_all_seasons(self):
         frontyear = 2017
         backyear = (frontyear + 1) % 100

         while frontyear != 2024:
              print(f"RESULTS FOR: {frontyear}-{backyear}")
              print()
              self.predict_season(f"{frontyear}-{backyear}")
              print()
              print()
              frontyear += 1
              backyear = (frontyear + 1) % 100
              continue

    def traded_player_check(self):
        player_feature_history = pandas.read_csv(self.player_feature_history)
        random_player_id = 1627783
        another_random_player_id = 1628384

        print(player_feature_history[(player_feature_history["PLAYER_ID"] == another_random_player_id) & (player_feature_history["SEASON"] == "2023-24")]
        [
            ["PLAYER_ID", "PLAYER_NAME", "TEAM_ID", "SEASON", "GP", "TOTAL_MINS", "PPG"]
        ])

        player_feature_history["SCORING_LOAD"] = player_feature_history["PPG"] * player_feature_history["MPG"]

        player_feature_history["EFFICIENCY_LOAD"] = player_feature_history["TS_PCT"] * player_feature_history["MPG"]

        player_feature_history["USAGE_LOAD"] = player_feature_history["USG_PCT"] * player_feature_history["MPG"]
        
        player_feature_history["PLUS_MINUS_LOAD"] =player_feature_history["PLUS_MINUS"] * player_feature_history["MPG"]

        print(player_feature_history.columns.tolist)
        
        



predictor = PredictorV1()
predictor.take_all_seasons()


 