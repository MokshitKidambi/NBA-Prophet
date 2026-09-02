import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="NBA Prophet",
    layout="wide"
)

st.title("Welcome to NBA Prophet")
st.subheader("The best prediction engine for the NBA")
st.subheader("2026-27 Season Predictions")

predictions = pd.read_csv(
    "data/display/display_engine_file.csv"
)

predictions = predictions.sort_values(
    "ADJUSTED_WINS",
    ascending=False
).reset_index(drop=True)

predictions["RANK"] = predictions.index + 1

rankings = predictions[
    [
        "RANK",
        "TEAM_NAME",
        "DISPLAY_WINS",
        "ROSTER_CONFIDENCE",
        "ROSTER_SENSITIVITY"
    ]
]

rankings = rankings.rename(
    columns={
        "TEAM_NAME": "Team",
        "DISPLAY_WINS": "Projected Wins",
        "ROSTER_CONFIDENCE": "Roster Confidence",
        "ROSTER_SENSITIVITY": "Roster Sensitivity"
    }
)

st.dataframe(
    rankings,
    hide_index=True,
    use_container_width=True
)