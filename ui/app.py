import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="NBA Prophet",
    layout="wide"
)

st.title("Welcome to NBA Prophet")
st.subheader("The best prediction engine for the NBA")
st.subheader("2026-27 Season Predictions")

team_conference = {
    "Atlanta Hawks": "East",
    "Boston Celtics": "East",
    "Brooklyn Nets": "East",
    "Charlotte Hornets": "East",
    "Chicago Bulls": "East",
    "Cleveland Cavaliers": "East",
    "Detroit Pistons": "East",
    "Indiana Pacers": "East",
    "Miami Heat": "East",
    "Milwaukee Bucks": "East",
    "New York Knicks": "East",
    "Orlando Magic": "East",
    "Philadelphia 76ers": "East",
    "Toronto Raptors": "East",
    "Washington Wizards": "East",

    "Dallas Mavericks": "West",
    "Denver Nuggets": "West",
    "Golden State Warriors": "West",
    "Houston Rockets": "West",
    "LA Clippers": "West",
    "Los Angeles Lakers": "West",
    "Memphis Grizzlies": "West",
    "Minnesota Timberwolves": "West",
    "New Orleans Pelicans": "West",
    "Oklahoma City Thunder": "West",
    "Phoenix Suns": "West",
    "Portland Trail Blazers": "West",
    "Sacramento Kings": "West",
    "San Antonio Spurs": "West",
    "Utah Jazz": "West"
}

predictions = pd.read_csv(
    "C:\\Users\\kidam\\OneDrive\\Documents\\pythonstuff\\NBA-Prophet\\gear3\\data\\display\\engine_display_file.csv"
)

predictions = predictions.sort_values(
    "ADJUSTED_WINS",
    ascending=False
).reset_index(drop=True)

predictions["RANK"] = predictions.index + 1

predictions["CONFERENCE"] = predictions["TEAM_NAME"].map(
    team_conference
)

east = predictions[
    predictions["CONFERENCE"] == "East"
].sort_values(
    "ADJUSTED_WINS",
    ascending=False
).reset_index(drop=True)

west = predictions[
    predictions["CONFERENCE"] == "West"
].sort_values(
    "ADJUSTED_WINS",
    ascending=False
).reset_index(drop=True)

east["SEED"] = east.index + 1
west["SEED"] = west.index + 1

col1, col2 = st.columns(2)

with col1:
    st.subheader("Eastern Conference")

    st.dataframe(
        east[
            [
                "SEED",
                "TEAM_NAME",
                "DISPLAY_WINS",
                "DISPLAY_LOSSES",
                "ROSTER_CONFIDENCE",
                "ROSTER_SENSITIVITY"
            ]
        ].rename(
            columns={
                "TEAM_NAME": "Team",
                "DISPLAY_WINS": "Projected Wins",
                "DISPLAY_LOSSES": "Projected Losses",
                "ROSTER_CONFIDENCE": "Roster Confidence",
                "ROSTER_SENSITIVITY": "Roster Sensitivity"
            }
        ),
        hide_index=True,
        use_container_width=True
    )

with col2:
    st.subheader("Western Conference")

    st.dataframe(
        west[
            [
                "SEED",
                "TEAM_NAME",
                "DISPLAY_WINS",
                "ROSTER_CONFIDENCE",
                "ROSTER_SENSITIVITY"
            ]
        ].rename(
            columns={
                "TEAM_NAME": "Team",
                "DISPLAY_WINS": "Projected Wins",
                "ROSTER_CONFIDENCE": "Roster Confidence",
                "ROSTER_SENSITIVITY": "Roster Sensitivity"
            }
        ),
        hide_index=True,
        use_container_width=True
    )