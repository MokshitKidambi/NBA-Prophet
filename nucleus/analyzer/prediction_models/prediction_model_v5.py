from pathlib import Path
import pandas
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error
from nba_api.stats.endpoints import commonallplayers
from nba_api.stats.endpoints import playerindex

class PredictorV5:
    def __init__(self):
        self.X = ["NET_RATING", "TM_TOV_PCT", "DREB_PCT", "AST_RATIO", "PACE", "NET_PPG_CHANGE", "RETAINED_MINUTES", "NET_SCORING_LOAD", "NET_EFFICIENCY_LOAD", "NET_USAGE_LOAD", "NET_PLUS_MINUS_LOAD", "CORE_AVAILABILITY_STD_DEV", "RETURNING_SCORING_SHARE"]
        self.dummyX = ["NET_RATING", "TM_TOV_PCT", "DREB_PCT", "AST_RATIO", "PACE", "NET_PPG_CHANGE", "RETAINED_MINUTES", "NET_SCORING_LOAD", "NET_EFFICIENCY_LOAD", "NET_USAGE_LOAD", "NET_PLUS_MINUS_LOAD", "CORE_AVAILABILITY_STD_DEV", "RETURNING_SCORING_SHARE"]
        self.Y = "NEXT_SEASON_WIN_PCT"
        self.roster_features = [
            "NET_PPG_CHANGE",
            "RETAINED_MINUTES",
            "NET_SCORING_LOAD",
            "NET_EFFICIENCY_LOAD",
            "NET_USAGE_LOAD",
            "NET_PLUS_MINUS_LOAD",
            "CORE_AVAILABILITY_STD_DEV",
            "RETURNING_SCORING_SHARE"
        ]

        self.team_experiment_features = ["NET_RATING", "TM_TOV_PCT", "DREB_PCT", "AST_RATIO", "PACE"]
        self.player_experiment_features = ["PPG", "TS_PCT","USG_PCT", "MPG", "TOTAL_MINS", "GP", "PLUS_MINUS"]

        self.team_training_ground_path = Path("C:\\Users\\kidam\\OneDrive\\Documents\\pythonstuff\\NBA-Prophet\\gear3\\data\\features\\training_ground.csv")
        self.player_feature_history = Path("C:\\Users\\kidam\\OneDrive\\Documents\\pythonstuff\\NBA-Prophet\\gear3\\data\\features\\player_feature_history.csv")
        self.season = "FEATURE_SEASON"

        self.median_historical_error = 6.392883589805631
        self._75th_percentile_historical_error = 9.801230645128888

        self.median_historical_error_rounded = 6
        self._75th_percentile_historical_error_rounded = 10

        self.feature_labels = {
            "NET_RATING": "Team Performance",
            "TM_TOV_PCT": "Turnover Rate",
            "DREB_PCT": "Defensive Rebounding",
            "AST_RATIO": "Ball Movement",
            "PACE": "Pace",

            "NET_PPG_CHANGE": "Roster Scoring Change",
            "RETAINED_MINUTES": "Roster Continuity",
            "NET_SCORING_LOAD": "Scoring Personnel Change",
            "NET_EFFICIENCY_LOAD": "Efficiency Personnel Change",
            "NET_USAGE_LOAD": "Usage Redistribution",
            "NET_PLUS_MINUS_LOAD": "Player Impact Change",

            "CORE_AVAILABILITY_STD_DEV": "Core Availability Stability",
            "RETURNING_SCORING_SHARE": "Returning Scoring"
        }

    def predict_season(self, test_season, team_index = 0, explain = False):

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
            TARGET_SEASON = row["NEW_SEASON"]
            outgoing_players = row["OUTGOING"]
            returning_players = row["RETURNING"]
            incoming_players = row["INCOMING"]
            TEAM_ID = row["TEAM_ID"]

            outgoing_stats = player_feature_history[
                (player_feature_history["SEASON"] == SEASON) &
                (player_feature_history["TEAM_ID"] == TEAM_ID) &
                (player_feature_history["PLAYER_ID"].isin(outgoing_players))
            ]

            returning_stats = player_feature_history[
                (player_feature_history["SEASON"] == SEASON) &
                (player_feature_history["TEAM_ID"] == TEAM_ID) &
                (player_feature_history["PLAYER_ID"].isin(returning_players))
            ]

            incoming_stats = player_feature_history[
                (player_feature_history["SEASON"] == SEASON) &
                (player_feature_history["PLAYER_ID"].isin(incoming_players))
            ]

            team_stats = training_ground[(training_ground["FEATURE_SEASON"] == SEASON) & (training_ground["TEAM_ID"] == TEAM_ID)]
            target_team_stats = training_ground[(training_ground["FEATURE_SEASON"] == TARGET_SEASON) & (training_ground["TEAM_ID"] == TEAM_ID)]
            old_team_stats = player_feature_history[(player_feature_history["SEASON"] == SEASON) & (player_feature_history["TEAM_ID"] == TEAM_ID)]
            new_team_stats = player_feature_history[(player_feature_history["SEASON"] == TARGET_SEASON) & (player_feature_history["TEAM_ID"] == TEAM_ID)]

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

            returning_scoring_load = returning_stats["SCORING_LOAD"].sum()
            roster_changes.loc[index, "RETURNING_SCORING_LOAD"] = returning_scoring_load

            returning_efficiency_load = returning_stats["EFFICIENCY_LOAD"].sum()
            roster_changes.loc[index, "RETURNING_EFFICIENCY_LOAD"] = returning_efficiency_load

            returning_plus_minus_load = returning_stats["PLUS_MINUS_LOAD"].sum()
            roster_changes.loc[index, "RETURNING_PLUS_MINUS_LOAD"] = returning_plus_minus_load

            returning_usage_load = returning_stats["USAGE_LOAD"].sum()
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

            old_team_scoring_load = old_team_stats["SCORING_LOAD"].sum()
            old_team_efficiency_load = old_team_stats["EFFICIENCY_LOAD"].sum()
            old_team_usage_load = old_team_stats["USAGE_LOAD"].sum()

            returning_scoring_share = returning_scoring_load / old_team_scoring_load
            roster_changes.loc[index, "RETURNING_SCORING_SHARE"] = returning_scoring_share

            returning_efficiency_share = returning_efficiency_load / old_team_efficiency_load
            roster_changes.loc[index, "RETURNING_EFFICIENCY_SHARE"] = returning_efficiency_share

            returning_usage_share = returning_usage_load / old_team_usage_load
            roster_changes.loc[index, "RETURNING_USAGE_SHARE"] = returning_usage_share         

            team_gp = (team_stats["W"] + team_stats["L"]).iloc[0]

            old_team_stats = old_team_stats.copy()

            old_team_stats["PLAYER_AVAILABILITY"] = (old_team_stats["GP"] / team_gp)

            availability = old_team_stats["GP"] / team_gp

            missed_availability = 1 - availability

            old_team_stats["WEIGHTED_AVAILABILITY"] = (old_team_stats["PLAYER_AVAILABILITY"] * old_team_stats["TOTAL_MINS"])

            roster_availability = (old_team_stats["WEIGHTED_AVAILABILITY"].sum() / old_team_stats["TOTAL_MINS"].sum())

            roster_changes.loc[index, "ROSTER_AVAILABILITY"] = roster_availability

            old_team_stats["LOST_SCORING_AVAILABILITY"] = (old_team_stats["SCORING_LOAD"] * missed_availability)
            old_team_stats["LOST_EFFICIENCY_AVAILABILITY"] = (old_team_stats["EFFICIENCY_LOAD"] * missed_availability)
            old_team_stats["LOST_USAGE_AVAILABILITY"] = (old_team_stats["USAGE_LOAD"] * missed_availability)
            old_team_stats["LOST_PLUS_MINUS_AVAILABILITY"] = (old_team_stats["PLUS_MINUS_LOAD"] * missed_availability)

            lost_scoring_availability = old_team_stats["LOST_SCORING_AVAILABILITY"].sum()
            lost_efficiency_availability = old_team_stats["LOST_EFFICIENCY_AVAILABILITY"].sum()
            lost_usage_availability = old_team_stats["LOST_USAGE_AVAILABILITY"].sum()
            lost_plus_minus_availability = old_team_stats["LOST_PLUS_MINUS_AVAILABILITY"].sum()

            roster_changes.loc[index, "LOST_SCORING_AVAILABILITY"] = lost_scoring_availability 
            roster_changes.loc[index, "LOST_EFFICIENCY_AVAILABILITY"] = lost_efficiency_availability 
            roster_changes.loc[index, "LOST_USAGE_AVAILABILITY"] = lost_usage_availability 
            roster_changes.loc[index, "LOST_PLUS_MINUS_AVAILABILITY"] = lost_plus_minus_availability

            core = old_team_stats.nlargest(8, "MPG")
            core_player_ids = set(core["PLAYER_ID"])

            if target_team_stats.empty:
                roster_changes.loc[index, "TARGET_OLD_CORE_AVAILABILITY"] = pandas.NA

            else:
                target_team_gp = (
                    target_team_stats["W"] + target_team_stats["L"]
                ).iloc[0]

                new_team_stats = new_team_stats.copy()

                new_team_stats["PLAYER_AVAILABILITY"] = (
                    new_team_stats["GP"] / target_team_gp
                )

                old_core_stats = new_team_stats[
                    new_team_stats["PLAYER_ID"].isin(core_player_ids)
                ]

                target_core_availability = (
                    old_core_stats
                    .set_index("PLAYER_ID")["PLAYER_AVAILABILITY"]
                    .reindex(core_player_ids, fill_value=0)
                )

                target_availability = target_core_availability.mean()

                roster_changes.loc[index, "TARGET_OLD_CORE_AVAILABILITY"] = target_availability

            core_availability = core["PLAYER_AVAILABILITY"].mean()

            returning_core = core_player_ids & returning_players

            returning_core_share = len(returning_core) / len(core_player_ids)
            roster_changes.loc[index, "RETURNING_CORE_SHARE"] = returning_core_share

            core_availability_std_dev = core["PLAYER_AVAILABILITY"].std()

            core_weighted_availability = (core["PLAYER_AVAILABILITY"] * core["MPG"]).sum() / core["MPG"].sum()

            roster_changes.loc[index, "CORE_AVAILABILITY"] = core_availability
            roster_changes.loc[index, "CORE_WEIGHTED_AVAILABILITY"] = core_weighted_availability
            roster_changes.loc[index, "CORE_AVAILABILITY_STD_DEV"] = core_availability_std_dev

               
        roster_changes["NET_PPG_CHANGE"] = roster_changes["INCOMING_PPG"] - roster_changes["OUTGOING_PPG"]
        
        roster_changes["RETAINED_MINUTES"] = roster_changes["RETURNING_TOTAL_MINS"] / (roster_changes["RETURNING_TOTAL_MINS"] + roster_changes["OUTGOING_TOTAL_MINS"])

        roster_changes["NET_SCORING_LOAD"] = roster_changes["INCOMING_SCORING_LOAD"] - roster_changes["OUTGOING_SCORING_LOAD"]
        roster_changes["NET_EFFICIENCY_LOAD"] = roster_changes["INCOMING_EFFICIENCY_LOAD"] - roster_changes["OUTGOING_EFFICIENCY_LOAD"]
        roster_changes["NET_USAGE_LOAD"] = roster_changes["INCOMING_USAGE_LOAD"] - roster_changes["OUTGOING_USAGE_LOAD"]
        roster_changes["NET_PLUS_MINUS_LOAD"] = roster_changes["INCOMING_PLUS_MINUS_LOAD"] - roster_changes["OUTGOING_PLUS_MINUS_LOAD"]

        hist_data = training_ground.merge(
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
                    "OUTGOING_PLUS_MINUS_LOAD",

                    "LOST_SCORING_AVAILABILITY",
                    "LOST_EFFICIENCY_AVAILABILITY",
                    "LOST_USAGE_AVAILABILITY",
                    "LOST_PLUS_MINUS_AVAILABILITY",

                    "CORE_AVAILABILITY",
                    "CORE_WEIGHTED_AVAILABILITY",
                    "CORE_AVAILABILITY_STD_DEV",

                    "RETURNING_SCORING_SHARE",
                    "RETURNING_EFFICIENCY_SHARE",
                    "RETURNING_USAGE_SHARE",
                    "RETURNING_CORE_SHARE",

                    "TARGET_OLD_CORE_AVAILABILITY"                   
                ]], left_on=["TEAM_ID", "FEATURE_SEASON"], right_on=["TEAM_ID", "OLD_SEASON"], how="inner", validate="one_to_one")

        hist_data.drop(columns = ["OLD_SEASON"], inplace = True)

        X_data = hist_data[self.X]
        Y_data = hist_data[self.Y]
        season_data = hist_data[self.season]
         
        train_mask = season_data < test_season
        test_mask = season_data == test_season
         
        X_train = X_data[train_mask]
        Y_train = Y_data[train_mask]
         
        X_test = X_data[test_mask]
        Y_test = Y_data[test_mask]

        scaler = StandardScaler()

        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
         
        model = Ridge(alpha = 7.0)
         
        model.fit(X_train_scaled, Y_train)

        model_coef = pandas.DataFrame()

        for i in range(len(self.X)):
            model_coef.loc[i, "FEATURE"] = self.X[i]
            model_coef.loc[i, "COEFFICIENT"] = model.coef_[i] * 82
            model_coef.loc[i, "ABS_COEFFICIENT"] = abs(model.coef_[i] * 82)

        model_coef = model_coef.sort_values(by = "ABS_COEFFICIENT", ascending = False)

        contributions = X_test_scaled * model.coef_
        contribution_wins = contributions * 82
         
        prediction = model.predict(X_test_scaled)

        team_contributions = pandas.DataFrame({"FEATURE": self.X, "CONTRIBUTION_WINS": contribution_wins[team_index]})
        team_contributions["ABS_CONTRIBUTION"] = abs(team_contributions["CONTRIBUTION_WINS"])
        team_contributions = team_contributions.sort_values(by = "ABS_CONTRIBUTION", ascending = False)        
                
        mae = mean_absolute_error(Y_test, prediction)
         
        test_info = hist_data.loc[test_mask, ["TEAM_NAME", "FEATURE_SEASON", "TARGET_SEASON", "TARGET_OLD_CORE_AVAILABILITY"]]

        team_name = test_info.iloc[team_index]["TEAM_NAME"]

        if explain:
            positive = team_contributions[
                team_contributions["CONTRIBUTION_WINS"] > 0
            ].head(3)

            negative = team_contributions[
                team_contributions["CONTRIBUTION_WINS"] < 0
            ].head(3)

            print(f"Top 3 Positive Contributors for The {team_name}:")
            print(positive)
            print()
            print(f"Top 3 Negative Contributors for The {team_name}:")
            print(negative)
            print()

        print(f"MAE: {mae}")

        result = pandas.DataFrame()
         
        result["ACTUAL_WIN_PCT"] = Y_test
        result["PREDICTED_WIN_PCT"] = prediction
         
        result["ACTUAL_WIN_82"] = result["ACTUAL_WIN_PCT"] * 82
        result["PREDICTED_WIN_82"] = result["PREDICTED_WIN_PCT"] * 82
         
        result["ABSOLUTE_ERROR_82"] = abs(result["ACTUAL_WIN_82"] - result["PREDICTED_WIN_82"])
        result["PREDICTION_ERROR_82"] = (result["PREDICTED_WIN_82"] - result["ACTUAL_WIN_82"])
         
        result = pandas.concat([test_info, result], axis = 1)
         
        result = result.sort_values(by = "ABSOLUTE_ERROR_82", ascending = False)
         
        test_info = test_info.reset_index(drop = True)
        result = result.reset_index(drop = True)
         
        median_error = result["ABSOLUTE_ERROR_82"].median()
                 
        print(f"Median Error: {median_error}")
         
        naive_prediction = hist_data.loc[test_mask, "W_PCT"]
        naive_mae = mean_absolute_error(Y_test, naive_prediction)
         
        print(f"Naive MAE: {naive_mae}")
        print(f"Naive MAE Wins: {naive_mae * 82}")
         
        simple_prediction = [0.500] * len(Y_test)
         
        simple_mae = mean_absolute_error(Y_test, simple_prediction)
         
        print(f"Simple MAE: {simple_mae}")
        print(f"Simple MAE Wins: {simple_mae * 82}")

        print(hist_data["FEATURE_SEASON"].unique())
        print(player_feature_history["SEASON"].unique())

        return result, hist_data

    def take_all_seasons(self):
         results = []
         frontyear = 2017
         backyear = (frontyear + 1) % 100

         while frontyear != 2024:
              print(f"RESULTS FOR: {frontyear}-{backyear}")
              print()
              result, _ = self.predict_season(f"{frontyear}-{backyear}")
              results.append(result)
              print()
              print()
              frontyear += 1
              backyear = (frontyear + 1) % 100
              continue

         result_comb = pandas.concat(results, ignore_index=True)

         print("BIGGEST MISSES")
         print(
            result_comb
            .sort_values("ABSOLUTE_ERROR_82", ascending=False)
            .head(10)
        )

         print("\nMOST OVERPREDICTED")
         print(
            result_comb
            .sort_values("PREDICTION_ERROR_82", ascending=False)
            .head(10)
        )

         print("\nMOST UNDERPREDICTED")
         print(
            result_comb
            .sort_values("PREDICTION_ERROR_82")
            .head(10)
        )

         print("\nERROR BY SEASON")
         print(
            result_comb
            .groupby("TARGET_SEASON")["ABSOLUTE_ERROR_82"]
            .agg(["mean", "median"])
        )

         result_comb["AVAILABILITY_BUCKET"] = pandas.cut(
            result_comb["TARGET_OLD_CORE_AVAILABILITY"],
            bins=[0, 0.35, 0.65, 1.0],
            labels=["LOW", "MEDIUM", "HIGH"],
            include_lowest=True
        )

         print(
            result_comb.groupby("AVAILABILITY_BUCKET")[
                "ABSOLUTE_ERROR_82"
            ].agg(["count", "mean", "median"])
        )

         error_median = result_comb["ABSOLUTE_ERROR_82"].median()
         error_75 = result_comb["ABSOLUTE_ERROR_82"].quantile(0.75)

         print("Overall median historical error:", error_median)
         print("75th percentile historical error:", error_75)

         return result_comb

    def traded_player_check(self):
        player_feature_history = pandas.read_csv(self.player_feature_history)
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

    def train_final_model(self, hist_data):
        final_train_mask = hist_data[self.Y].notna()

        X_final_train = hist_data.loc[final_train_mask, self.X]
        Y_final_train = hist_data.loc[final_train_mask, self.Y]

        final_scaler = StandardScaler()
        X_final_scaled = final_scaler.fit_transform(X_final_train)

        final_model = Ridge(alpha=7.0)
        final_model.fit(X_final_scaled, Y_final_train)

        future_data, future_X = self.build_future_roster_features()

        future_X_scaled = final_scaler.transform(future_X)

        contributions = future_X_scaled * final_model.coef_
        contribution_wins = contributions * 82

        for team_index in range(len(future_data)):
            team_name = future_data.iloc[team_index]["TEAM_NAME"]
            team_contributions = pandas.DataFrame({
                "FEATURE": [self.feature_labels[feature] for feature in self.X],
                "CONTRIBUTION_WINS": contribution_wins[team_index]
            })

            positive = (
                team_contributions[
                    team_contributions["CONTRIBUTION_WINS"] > 0
                ]
                .sort_values("CONTRIBUTION_WINS", ascending=False)
                .head(3)
            )

            for contributor_index in range(len(positive)):
                future_data.loc[team_index, f"TOP_POSITIVE_CONTRIBUTOR_{contributor_index+1}"] = positive.iloc[contributor_index]["FEATURE"]
                future_data.loc[team_index, f"TOP_POSITIVE_CONTRIBUTOR_{contributor_index+1}_WINS"] = positive.iloc[contributor_index]["CONTRIBUTION_WINS"]

            negative = (
                team_contributions[
                    team_contributions["CONTRIBUTION_WINS"] < 0
                ]
                .sort_values("CONTRIBUTION_WINS")
                .head(3)
            )

            for contributor_index in range(len(negative)):
                future_data.loc[team_index, f"TOP_NEGATIVE_CONTRIBUTOR_{contributor_index+1}"] = negative.iloc[contributor_index]["FEATURE"]
                future_data.loc[team_index, f"TOP_NEGATIVE_CONTRIBUTOR_{contributor_index+1}_WINS"] = negative.iloc[contributor_index]["CONTRIBUTION_WINS"]
            

            print(f"Top 3 Positive Contributors for The {team_name}:")
            print(positive)
            print()
            print(f"Top 3 Negative Contributors for The {team_name}:")
            print(negative)
            print()

        optimistic_X = future_X.copy()
        pessimistic_X = future_X.copy()

        for feature in self.roster_features:
            delta = future_X[feature].abs() * 0.20
            feature_index = self.X.index(feature)

            if final_model.coef_[feature_index] > 0:
                optimistic_X[feature] += delta
                pessimistic_X[feature] -= delta
            else:
                optimistic_X[feature] -= delta
                pessimistic_X[feature] += delta

        optimistic_scaled = final_scaler.transform(optimistic_X)
        pessimistic_scaled = final_scaler.transform(pessimistic_X)

        optimistic_predictions = final_model.predict(optimistic_scaled)
        pessimistic_predictions = final_model.predict(pessimistic_scaled)

        predictions = final_model.predict(future_X_scaled)

        base_raw_wins = predictions * 82

        optimistic_raw_wins = optimistic_predictions * 82
        pessimistic_raw_wins = pessimistic_predictions * 82

        future_data["OPTIMISTIC_DELTA"] = (optimistic_raw_wins - base_raw_wins)

        future_data["PESSIMISTIC_DELTA"] = (pessimistic_raw_wins - base_raw_wins)

        future_data["PREDICTED_WIN_PCT"] = predictions

        future_data["PREDICTED_WINS"] = (future_data["PREDICTED_WIN_PCT"] * 82)

        league_offset = (future_data["PREDICTED_WIN_PCT"].mean() - 0.500)

        future_data["ADJUSTED_WIN_PCT"] = (future_data["PREDICTED_WIN_PCT"] - league_offset)

        future_data["ADJUSTED_WINS"] = (future_data["ADJUSTED_WIN_PCT"] * 82)

        future_data = future_data.sort_values("ADJUSTED_WINS", ascending=False)

        future_data["OPTIMISTIC_WINS"] = (future_data["ADJUSTED_WINS"] + future_data["OPTIMISTIC_DELTA"])
        
        future_data["PESSIMISTIC_WINS"] = (future_data["ADJUSTED_WINS"] + future_data["PESSIMISTIC_DELTA"])

        print(
            future_data[
                [
                    "TEAM_NAME",
                    "PESSIMISTIC_WINS",
                    "ADJUSTED_WINS",
                    "OPTIMISTIC_WINS",
                    "PESSIMISTIC_DELTA",
                    "OPTIMISTIC_DELTA"
                ]
            ].head(10)
        )

        historical_X = hist_data.loc[hist_data[self.Y].notna(), self.X]

        for feature in self.X:
            hist_min = historical_X[feature].min()
            hist_max = historical_X[feature].max()

            outside = future_data[
                (future_data[feature] < hist_min) |
                (future_data[feature] > hist_max)
            ]

            if len(outside) > 0:
                print(f"\nOUT OF RANGE: {feature}")
                print(
                    outside[
                        ["TEAM_NAME", feature]
                    ]
                )

        bounded_features = [
            "RETAINED_MINUTES",
            "RETURNING_SCORING_SHARE",
            "CORE_AVAILABILITY_STD_DEV"
        ]

        for feature in bounded_features:
            optimistic_X[feature] = optimistic_X[feature].clip(0, 1)
            pessimistic_X[feature] = pessimistic_X[feature].clip(0, 1)

        future_data["ROSTER_SENSITIVITY"] = future_data.apply(
            self.roster_sensitivity, axis = 1
        )
        
        future_data["DISPLAY_WINS"] = (future_data["ADJUSTED_WINS"].round().astype(int))

        future_data["DISPLAY_LOSSES"] = (82 - future_data["DISPLAY_WINS"])

        future_data["DISPLAY_OPTIMISTIC_WINS"] = (
            future_data["OPTIMISTIC_WINS"].round().astype(int)
        )

        future_data["DISPLAY_PESSIMISTIC_WINS"] = (
            future_data["PESSIMISTIC_WINS"].round().astype(int)
        )

        return future_data

    def build_future_roster_features(self):
        training_ground = pandas.read_csv(self.team_training_ground_path)
        player_feature_history = pandas.read_csv(self.player_feature_history)

        players = commonallplayers.CommonAllPlayers(
            is_only_current_season=1,
            league_id="00",
            season="2026-27"
        ).get_data_frames()[0]


        all_rosters = players[players["TEAM_ID"] != 0][["TEAM_ID", "PERSON_ID", "DISPLAY_FIRST_LAST", "ROSTERSTATUS"]].copy()

        all_rosters.rename(
            columns={
                "PERSON_ID": "PLAYER_ID",
                "DISPLAY_FIRST_LAST": "PLAYER_NAME"
            },
            inplace=True
        )

        all_rosters["SEASON"] = "2026-27"

        team_ids = [1610612737, 1610612738, 1610612751, 1610612766, 1610612741, 1610612739, 1610612742, 1610612743, 1610612765, 1610612744, 1610612745, 1610612746, 1610612747, 1610612763, 1610612748, 1610612749, 1610612750, 1610612752, 1610612753, 1610612754, 1610612755, 1610612756, 1610612757, 1610612758, 1610612759, 1610612760, 1610612761, 1610612762, 1610612764, 1610612740]

        roster_changes = []

        for team_id in team_ids:

            old_roster = set(
                player_feature_history[
                    (player_feature_history["SEASON"] == "2025-26") &
                    (player_feature_history["TEAM_ID"] == team_id)
                ]["PLAYER_ID"]
            )

            new_roster = set(
                all_rosters[
                    all_rosters["TEAM_ID"] == team_id
                ]["PLAYER_ID"]
            )

            returning = old_roster & new_roster
            outgoing = old_roster - new_roster
            incoming = new_roster - old_roster

            roster_changes.append({
                "TEAM_ID": team_id,
                "OLD_SEASON": "2025-26",
                "NEW_SEASON": "2026-27",
                "RETURNING": returning,
                "OUTGOING": outgoing,
                "INCOMING": incoming
            })

        roster_changes = pandas.DataFrame(roster_changes)

        player_feature_history["SCORING_LOAD"] = (
            player_feature_history["PPG"] * player_feature_history["MPG"]
        )

        player_feature_history["EFFICIENCY_LOAD"] = (
            player_feature_history["TS_PCT"] * player_feature_history["MPG"]
        )

        player_feature_history["USAGE_LOAD"] = (
            player_feature_history["USG_PCT"] * player_feature_history["MPG"]
        )

        player_feature_history["PLUS_MINUS_LOAD"] = (
            player_feature_history["PLUS_MINUS"] * player_feature_history["MPG"]
        )

        for index, row in roster_changes.iterrows():
        
                    SEASON = row["OLD_SEASON"]
                    outgoing_players = row["OUTGOING"]
                    returning_players = row["RETURNING"]
                    incoming_players = row["INCOMING"]
                    TEAM_ID = row["TEAM_ID"]
        
                    outgoing_stats = player_feature_history[
                        (player_feature_history["SEASON"] == SEASON) &
                        (player_feature_history["TEAM_ID"] == TEAM_ID) &
                        (player_feature_history["PLAYER_ID"].isin(outgoing_players))
                    ]
        
                    returning_stats = player_feature_history[
                        (player_feature_history["SEASON"] == SEASON) &
                        (player_feature_history["TEAM_ID"] == TEAM_ID) &
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
        
                    returning_scoring_load = returning_stats["SCORING_LOAD"].sum()
                    roster_changes.loc[index, "RETURNING_SCORING_LOAD"] = returning_scoring_load
        
                    returning_efficiency_load = returning_stats["EFFICIENCY_LOAD"].sum()
                    roster_changes.loc[index, "RETURNING_EFFICIENCY_LOAD"] = returning_efficiency_load
        
                    returning_plus_minus_load = returning_stats["PLUS_MINUS_LOAD"].sum()
                    roster_changes.loc[index, "RETURNING_PLUS_MINUS_LOAD"] = returning_plus_minus_load
        
                    returning_usage_load = returning_stats["USAGE_LOAD"].sum()
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
        
                    old_team_scoring_load = old_team_stats["SCORING_LOAD"].sum()

                    returning_scoring_share = (
                        returning_scoring_load / old_team_scoring_load
                    )

                    roster_changes.loc[index, "RETURNING_SCORING_SHARE"] = returning_scoring_share

                    team_gp = (team_stats["W"] + team_stats["L"]).iloc[0]

                    old_team_stats = old_team_stats.copy()

                    old_team_stats["PLAYER_AVAILABILITY"] = (
                        old_team_stats["GP"] / team_gp
                    )

                    core = old_team_stats.nlargest(8, "MPG")

                    core_availability_std_dev = (core["PLAYER_AVAILABILITY"].std())

                    roster_changes.loc[index, "CORE_AVAILABILITY_STD_DEV"] = core_availability_std_dev

                    incoming_with_stats = set(incoming_stats["PLAYER_ID"])
                    incoming_without_stats = incoming_players - incoming_with_stats

                    roster_changes.loc[index, "INCOMING_COUNT"] = len(incoming_players)
                    roster_changes.loc[index, "INCOMING_WITH_STATS"] = len(incoming_with_stats)
                    roster_changes.loc[index, "INCOMING_WITHOUT_STATS"] = len(incoming_without_stats)

        roster_changes["NET_PPG_CHANGE"] = (roster_changes["INCOMING_PPG"] - roster_changes["OUTGOING_PPG"])

        roster_changes["RETAINED_MINUTES"] = (roster_changes["RETURNING_TOTAL_MINS"] / (roster_changes["RETURNING_TOTAL_MINS"] + roster_changes["OUTGOING_TOTAL_MINS"]))

        roster_changes["NET_SCORING_LOAD"] = (roster_changes["INCOMING_SCORING_LOAD"] - roster_changes["OUTGOING_SCORING_LOAD"])

        roster_changes["NET_EFFICIENCY_LOAD"] = (roster_changes["INCOMING_EFFICIENCY_LOAD"] - roster_changes["OUTGOING_EFFICIENCY_LOAD"])

        roster_changes["NET_USAGE_LOAD"] = (roster_changes["INCOMING_USAGE_LOAD"] - roster_changes["OUTGOING_USAGE_LOAD"])

        roster_changes["NET_PLUS_MINUS_LOAD"] = (roster_changes["INCOMING_PLUS_MINUS_LOAD"] - roster_changes["OUTGOING_PLUS_MINUS_LOAD"])

        future_team_base = training_ground[training_ground["FEATURE_SEASON"] == "2025-26"].copy()
        
        future_data = future_team_base.merge(
            roster_changes[[
                "TEAM_ID",
                "NET_PPG_CHANGE",
                "RETAINED_MINUTES",
                "NET_SCORING_LOAD",
                "NET_EFFICIENCY_LOAD",
                "NET_USAGE_LOAD",
                "NET_PLUS_MINUS_LOAD",
                "CORE_AVAILABILITY_STD_DEV",
                "RETURNING_SCORING_SHARE", 
                "INCOMING_COUNT",
                "INCOMING_WITH_STATS",
                "INCOMING_WITHOUT_STATS"
            ]],
            on="TEAM_ID", how="left", validate="one_to_one"
        )

        future_data["INCOMING_STAT_COVERAGE"] = (
            future_data["INCOMING_WITH_STATS"] /
            future_data["INCOMING_COUNT"]
        )

        future_data["ROSTER_CONFIDENCE"] = future_data.apply(
            self.roster_confidence, axis = 1
        )

        future_X = future_data[self.X]

        return future_data, future_X

    def roster_confidence(self, row):
        coverage = row["INCOMING_STAT_COVERAGE"]
        missing = row["INCOMING_WITHOUT_STATS"]

        if coverage < 0.40 and missing > 3:
            return "LOW"
        elif coverage < 0.70:
            return "MEDIUM"
        else:
            return "HIGH"

    def roster_sensitivity(self, row):
        delta = row["OPTIMISTIC_DELTA"]

        if delta < 3.0:
            return "LOW"
        elif delta < 5.0:
            return "MEDIUM"
        else:
            return "HIGH"

    def new_file(self):
        result, hist_data = self.predict_season("2023-24")
        future_data = self.train_final_model(hist_data)

        new_future_data = future_data[["TEAM_NAME", "TEAM_ID", "ADJUSTED_WINS", "DISPLAY_WINS", "DISPLAY_LOSSES", "DISPLAY_OPTIMISTIC_WINS", "DISPLAY_PESSIMISTIC_WINS", "ROSTER_CONFIDENCE", "ROSTER_SENSITIVITY", "INCOMING_STAT_COVERAGE", "TOP_POSITIVE_CONTRIBUTOR_1", "TOP_POSITIVE_CONTRIBUTOR_1_WINS", "TOP_POSITIVE_CONTRIBUTOR_2", "TOP_POSITIVE_CONTRIBUTOR_2_WINS", "TOP_POSITIVE_CONTRIBUTOR_3", "TOP_POSITIVE_CONTRIBUTOR_3_WINS", "TOP_NEGATIVE_CONTRIBUTOR_1", "TOP_NEGATIVE_CONTRIBUTOR_1_WINS", "TOP_NEGATIVE_CONTRIBUTOR_2", "TOP_NEGATIVE_CONTRIBUTOR_2_WINS", "TOP_NEGATIVE_CONTRIBUTOR_3", "TOP_NEGATIVE_CONTRIBUTOR_3_WINS"]]

        new_future_data.to_csv("data/display/engine_display_file.csv", index=False)

        return new_future_data

    def _2027_roster(self):
        players = commonallplayers.CommonAllPlayers(
            is_only_current_season=1,
            league_id="00",
            season="2026-27"
        ).get_data_frames()[0]

        player_positions = playerindex.PlayerIndex(season="2026-27").get_data_frames()[0]

        player_positions = player_positions[
            [
                "PERSON_ID",
                "TEAM_ID",
                "POSITION"
            ]
        ].rename(
            columns={
                "PERSON_ID": "PLAYER_ID"
            }
        )
        all_rosters = players[players["TEAM_ID"] != 0][["TEAM_ID", "PERSON_ID", "DISPLAY_FIRST_LAST", "ROSTERSTATUS"]].copy()

        all_rosters.rename(
            columns={
                "PERSON_ID": "PLAYER_ID",
                "DISPLAY_FIRST_LAST": "PLAYER_NAME"
            },
            inplace=True
        )

        all_rosters["SEASON"] = "2026-27"

        future_roster = all_rosters.merge(
            player_positions[
                ["PLAYER_ID", "POSITION"]
            ],
            on="PLAYER_ID",
            how="left"
        )
        
        injuries = pandas.read_csv("C:\\Users\\kidam\\OneDrive\\Documents\\pythonstuff\\NBA-Prophet\\gear3\\data\\rosters\\injuries.csv")

        injuries = injuries.merge(future_roster[["PLAYER_ID", "PLAYER_NAME"]], on = "PLAYER_NAME", how = "left")
        injuries.to_csv("C:\\Users\\kidam\\OneDrive\\Documents\\pythonstuff\\NBA-Prophet\\gear3\\data\\rosters\\injuries.csv", index = False)
        
predictor = PredictorV5()
result, hist_data = predictor.predict_season("2023-24")

future_predictions = predictor.train_final_model(hist_data)

