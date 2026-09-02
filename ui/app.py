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

west["LOGO"] = west["TEAM_ID"].apply(
    lambda team_id:
        f"https://cdn.nba.com/logos/nba/{int(team_id)}/primary/L/logo.svg"
)

east["LOGO"] = east["TEAM_ID"].apply(
    lambda team_id:
        f"https://cdn.nba.com/logos/nba/{int(team_id)}/primary/L/logo.svg"
)

col1, col2 = st.columns(2)

if "reveal_stage" not in st.session_state:
    st.session_state.reveal_stage = 0

if st.session_state.reveal_stage == 0:
    if st.button("Reveal Predictions"):
        st.session_state.reveal_stage = 1
        st.rerun()
else:
    if st.button("Hide Predictions"):
        st.session_state.reveal_stage = 0
        st.rerun()

if st.session_state.reveal_stage >= 1:
    with col1:
        st.subheader("Eastern Conference")
        east_display = east[
                [
                    "SEED",
                    "LOGO",
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
            )
        east_event = st.dataframe(
            east_display,
            hide_index=True,
            use_container_width=True,
            on_select="rerun",
            selection_mode="single-row",
            column_config={
                "LOGO": st.column_config.ImageColumn(
                    "Logo",
                    width="small"
                )
            }
        )

    with col2:
        st.subheader("Western Conference")
        west_display = west[
                [
                    "SEED",
                    "LOGO",
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
            )
        west_event = st.dataframe(
            west_display,
            hide_index=True,
            use_container_width=True,
            on_select="rerun",
            selection_mode="single-row",
            column_config={
                "LOGO": st.column_config.ImageColumn(
                    "Logo",
                    width="small"
                )
            }
        )

    if east_event.selection.rows:
        selected_index = east_event.selection.rows[0]

        st.session_state.selected_team = (
            east.iloc[selected_index]["TEAM_NAME"]
        )
        st.switch_page("pages/team_details.py")

    elif west_event.selection.rows:
        selected_index = west_event.selection.rows[0]

        st.session_state.selected_team = (
            west.iloc[selected_index]["TEAM_NAME"]
        )
        st.switch_page("pages/team_details.py")
