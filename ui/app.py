import streamlit as st
import pandas as pd
import time

st.set_page_config(
    page_title="NBA Prophet",
    layout="wide"
)

def type_text(placeholder, text, tag="h1", speed=0.04):
    typed_text = ""

    for character in text:
        typed_text += character

        placeholder.markdown(
            f"""
            <{tag} style="text-align: center;">
                {typed_text}
            </{tag}>
            """,
            unsafe_allow_html=True
        )

        time.sleep(speed)

st.markdown(
    """
    <style>
    /* Make tertiary buttons look like clickable team names */
    div[data-testid="stButton"] button[kind="tertiary"] {
        border: none;
        background: transparent;
        padding: 0;
        font-size: 16px;
        font-weight: 500;
    }

    div[data-testid="stButton"] button[kind="tertiary"]:hover {
        text-decoration: underline;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def sort_conference(conference, sort_by):

    conference = conference.copy()

    if sort_by == "Projected Wins":

        return conference.sort_values(
            "ADJUSTED_WINS",
            ascending=False
        )

    elif sort_by == "Roster Confidence":

        confidence_order = {
            "HIGH": 3,
            "MEDIUM": 2,
            "LOW": 1
        }

        conference["CONFIDENCE_ORDER"] = (
            conference["ROSTER_CONFIDENCE"]
            .map(confidence_order)
        )

        return conference.sort_values(
            ["CONFIDENCE_ORDER", "ADJUSTED_WINS"],
            ascending=[False, False]
        )

    elif sort_by == "Roster Sensitivity":

        sensitivity_order = {
            "LOW": 1,
            "MEDIUM": 2,
            "HIGH": 3
        }

        conference["SENSITIVITY_ORDER"] = (
            conference["ROSTER_SENSITIVITY"]
            .map(sensitivity_order)
        )

        return conference.sort_values(
            ["SENSITIVITY_ORDER", "ADJUSTED_WINS"],
            ascending=[True, False]
        )

if "intro_finished" not in st.session_state:
    st.session_state.intro_finished = False

if not st.session_state.intro_finished:

    title_placeholder = st.empty()
    subtitle_placeholder = st.empty()
    season_placeholder = st.empty()

    type_text(
        title_placeholder,
        "Welcome to NBA Prophet",
        "h1",
        0.05
    )
    
    time.sleep(0.3)

    type_text(
        subtitle_placeholder,
        "The best prediction engine for the NBA",
        "h2",
        0.03
    )
    
    time.sleep(0.5)

    type_text(
        season_placeholder,
        "2026–27 Regular Season Predictions",
        "h2",
        0.03
    )

    st.session_state.intro_finished = True

else:
    st.markdown(
        """
        <div style="text-align: center;">
            <h1>Welcome to NBA Prophet</h1>
            <h2>The best prediction engine for the NBA</h2>
            <h2>2026–27 Season Predictions</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

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

def display_conference(conference, conference_name):

    st.subheader(conference_name)

    column_widths = [0.35, 0.55, 1.8, 0.65, 0.65, 0.9, 1.0]    
    
    header = st.columns(column_widths)

    header[0].markdown("**Seed**")
    header[1].write("")
    header[2].markdown("**Team**")
    header[3].markdown("**Projected Wins**")
    header[4].markdown("**Projected Losses**")
    header[5].markdown("**Roster Confidence**")
    header[6].markdown("**Roster Sensitivity**")

    for _, team in conference.iterrows():

        seed_col, logo_col, team_col, wins_col, losses_col, confi_col, sens_col = st.columns(
            column_widths
        )

        seed_col.write(int(team["SEED"]))

        logo_col.image(team["LOGO"], width = 45)

        with team_col:
            if st.button(team["TEAM_NAME"], key = f"team_{int(team['TEAM_ID'])}", type = "tertiary"):
                st.session_state.selected_team = team["TEAM_NAME"]
                st.switch_page("pages/team_details.py")

        wins_col.write(int(team["DISPLAY_WINS"]))
        losses_col.write(int(team["DISPLAY_LOSSES"]))
        confi_col.write(team["ROSTER_CONFIDENCE"])
        sens_col.write(team["ROSTER_SENSITIVITY"])

predictions = pd.read_csv(
    r"C:\Users\kidam\OneDrive\Documents\pythonstuff\NBA-Prophet\gear3\data\display\engine_display_file.csv"
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

if "reveal_stage" not in st.session_state:
    st.session_state.reveal_stage = 0

left, center, right = st.columns([2, 1, 2])

with center:

    if st.session_state.reveal_stage == 0:

        if st.button(
            "Reveal Predictions",
            use_container_width=True
        ):
            st.session_state.reveal_stage = 1
            st.session_state.animate_reveal = True

    else:

        if st.button(
            "Hide Predictions",
            use_container_width=True
        ):
            st.session_state.reveal_stage = 0
            st.session_state.animate_reveal = False
            st.rerun()
    
left, center, right = st.columns([2, 1, 2])

with center:
    if st.button("How NBA Prophet Works", use_container_width=True):
        st.switch_page("pages/logic.py")

if st.session_state.reveal_stage >= 1:
    sort_by = st.selectbox(
        "Rank teams by",
        [
            "Projected Wins",
            "Roster Confidence",
            "Roster Sensitivity"
        ]
    )
    
    east_display = sort_conference(east, sort_by)
    west_display = sort_conference(west, sort_by)
    
    east_tab, west_tab = st.tabs([
        "Eastern Conference",
        "Western Conference"
    ])

    if st.session_state.animate_reveal:
        with east_tab:
            display_conference(
                east_display,
                "Eastern Conference"
            )

        time.sleep(1.5)

        with west_tab:
            display_conference(
                west_display,
                "Western Conference"
            )

        st.session_state.animate_reveal = False

    else:
        with east_tab:
            display_conference(
                east_display,
                "Eastern Conference"
            )

        with west_tab:
            display_conference(
                west_display,
                "Western Conference"
            )