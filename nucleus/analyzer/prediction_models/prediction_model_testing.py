from prediction_model import PredictorV4
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge

def main():
    predictor = PredictorV4()

    _, hist_data = predictor.predict_season(
        "2024-25",
        use_oof=False,
        rookie_weight=0.0,
    )

    X_final = hist_data[predictor.X]
    Y_final = hist_data[predictor.Y]

    valid_mask = Y_final.notna()

    X_final = X_final[valid_mask]
    Y_final = Y_final[valid_mask]

    final_scaler = StandardScaler()

    X_final_scaled = final_scaler.fit_transform(X_final)

    final_model = Ridge(alpha=2.0)

    final_model.fit(
        X_final_scaled,
        Y_final
    )

    future_data, future_X = predictor.build_future_roster_features()

    future_X_scaled = final_scaler.transform(future_X)

    future_predictions = final_model.predict(
        future_X_scaled
    )

    predictions_2027 = future_data[
        ["TEAM_ID", "TEAM_NAME"]
    ].copy()

    predictions_2027["PREDICTED_WIN_PCT"] = future_predictions
    predictions_2027["PREDICTED_WINS"] = (
        predictions_2027["PREDICTED_WIN_PCT"] * 82
    )

    predictions_2027 = predictions_2027.sort_values(
        "PREDICTED_WINS",
        ascending=False
    ).reset_index(drop=True)

    league_win_target = 1230

    win_adjustment = (
        predictions_2027["PREDICTED_WINS"].sum()
        - league_win_target
    ) / len(predictions_2027)

    predictions_2027["ADJUSTED_WINS"] = (
        predictions_2027["PREDICTED_WINS"]
        - win_adjustment
    )

    predictions_2027["ADJUSTED_WIN_PCT"] = (
        predictions_2027["ADJUSTED_WINS"] / 82
    )
        
    #median_error = 6.1243
    error_80 = 10.8174
    error_90 = 13.3883
    error_95 = 15.6014

    predictions_2027["LOW_80"] = (
        predictions_2027["ADJUSTED_WINS"] - error_80
    ).clip(lower=0)

    predictions_2027["HIGH_80"] = (
        predictions_2027["ADJUSTED_WINS"] + error_80
    ).clip(upper=82)

    predictions_2027["LOW_90"] = (
        predictions_2027["ADJUSTED_WINS"] - error_90
    ).clip(lower=0)

    predictions_2027["HIGH_90"] = (
        predictions_2027["ADJUSTED_WINS"] + error_90
    ).clip(upper=82)

    predictions_2027["LOW_95"] = (
        predictions_2027["ADJUSTED_WINS"] - error_95
    ).clip(lower=0)

    predictions_2027["HIGH_95"] = (
        predictions_2027["ADJUSTED_WINS"] + error_95
    ).clip(upper=82)

    final_predictions = predictions_2027[
        [
            "TEAM_ID",
            "TEAM_NAME",
            "ADJUSTED_WIN_PCT",
            "ADJUSTED_WINS",
            "LOW_80",
            "HIGH_80",
            "LOW_90",
            "HIGH_90",
            "LOW_95",
            "HIGH_95"
        ]
    ].copy()

    final_predictions = final_predictions.sort_values(
        "ADJUSTED_WINS",
        ascending=False
    ).reset_index(drop=True)

    final_predictions["RANK"] = (
        final_predictions.index + 1
    )

    final_predictions = final_predictions[
        [
            "RANK",
            "TEAM_ID",
            "TEAM_NAME",
            "ADJUSTED_WIN_PCT",
            "ADJUSTED_WINS",
            "LOW_80",
            "HIGH_80",
            "LOW_90",
            "HIGH_90",
            "LOW_95",
            "HIGH_95"
        ]
    ]

    print(
        final_predictions.round({
            "ADJUSTED_WIN_PCT": 3,
            "ADJUSTED_WINS": 1,
            "LOW_80": 1,
            "HIGH_80": 1,
            "LOW_90": 1,
            "HIGH_90": 1,
            "LOW_95": 1,
            "HIGH_95": 1
        }).to_string(index=False)
    )

    final_predictions.to_csv(
        r"C:\Users\kidam\OneDrive\Documents\pythonstuff\NBA-Prophet\gear4\data\display\nba_prophet_2026_27_predictions.csv",
        index=False
    )
    
if __name__ == "__main__":
    main()