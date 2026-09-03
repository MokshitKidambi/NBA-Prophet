import streamlit as st
import pandas as pd
from pathlib import Path

st.markdown("""
<style>
    [data-testid="stSidebar"] {
        display: none;
    }

    [data-testid="stSidebarCollapsedControl"] {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

BASE_DIR = Path(__file__).resolve().parent.parent.parent

injuries = pd.read_csv(
    BASE_DIR / "data" / "rosters" / "injuries.csv"
)

future_roster = pd.read_csv(
    BASE_DIR / "data" / "rosters" / "2026-27_rosters.csv"
)

injuries = injuries.merge(future_roster[["POSITION", "PLAYER_ID"]], on = "PLAYER_ID", how = "left")

if "selected_injured_player" not in st.session_state:
    st.warning("No injured player selected.")
    st.stop()

player_id = st.session_state.selected_injured_player

player_image = (
    f"https://cdn.nba.com/headshots/nba/latest/260x190/"
    f"{int(player_id)}.png"
)

if st.button("← Back to Team"):
    st.switch_page("pages/team_details.py")

st.image(player_image, width = 180)

injury = injuries[
    injuries["PLAYER_ID"] == player_id
].iloc[0]

st.title(f"{injury["PLAYER_NAME"]} - {injury["POSITION"]}")

st.error("🔴 Injured")

st.subheader("Injury")
st.write(injury["INJURY"])

st.subheader("Expected Return")
st.write(injury["EXPECTED_RETURN"])

if "NOTE" in injury.index and pd.notna(injury["NOTE"]):
    st.subheader("Latest Update")
    st.write(injury["NOTE"])