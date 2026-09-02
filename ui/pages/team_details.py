import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="NBA Prophet - Team Details",
    layout="wide"
)

predictions = pd.read_csv(
    "C:\\Users\\kidam\\OneDrive\\Documents\\pythonstuff\\NBA-Prophet\\gear3\\data\\display\\engine_display_file.csv"
)

if "selected_team" not in st.session_state:
    st.warning("No team selected.")
    st.stop()

team_name = st.session_state.selected_team

team = predictions[
    predictions["TEAM_NAME"] == team_name
].iloc[0]

logo_url = (
    f"https://cdn.nba.com/logos/nba/"
    f"{int(team['TEAM_ID'])}/primary/L/logo.svg"
)

st.image(
    logo_url,
    width=140
)

st.title(team["TEAM_NAME"])

st.metric(
    "Projected Wins",
    int(team["DISPLAY_WINS"])
)

st.metric(
    "Projected Losses",
    int(team["DISPLAY_LOSSES"])
)

st.write(
    "Roster Confidence:",
    team["ROSTER_CONFIDENCE"]
)

st.write(
    "Roster Sensitivity:",
    team["ROSTER_SENSITIVITY"]
)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Top Positive Contributors")

    for i in range(1, 4):
        feature = team[f"TOP_POSITIVE_CONTRIBUTOR_{i}"]
        wins = team[f"TOP_POSITIVE_CONTRIBUTOR_{i}_WINS"]

        st.write(f"▲ {feature}: +{wins:.2f} wins")


with col2:
    st.subheader("Top Negative Contributors")

    for i in range(1, 4):
        feature = team[f"TOP_NEGATIVE_CONTRIBUTOR_{i}"]
        wins = team[f"TOP_NEGATIVE_CONTRIBUTOR_{i}_WINS"]

        st.write(f"▼ {feature}: {wins:.2f} wins")

if st.button("← Back to Standings"):
    st.switch_page("app.py")