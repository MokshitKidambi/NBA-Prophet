import streamlit as st
import pandas as pd
import ast
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

player_feature_history = pd.read_csv(BASE_DIR / "gear3" / "data" / "features" / "player_feature_history.csv")
predictions = pd.read_csv(BASE_DIR / "gear3" / "data" / "display" / "engine_display_file.csv")
roster_changes = pd.read_csv(BASE_DIR / "gear3" / "data" / "rosters" / "2025-26_to_2026-27_roster_changes.csv")
old_roster = pd.read_csv(BASE_DIR / "gear3" / "data" / "rosters" / "2025-26_roster.csv")
future_roster = pd.read_csv(BASE_DIR / "gear3" / "data" / "rosters" / "2026-27_rosters.csv")
injuries = pd.read_csv(BASE_DIR / "gear3" / "data" / "rosters" / "injuries.csv")

def player_image_url(player_id):
    return (
        f"https://cdn.nba.com/headshots/nba/latest/260x190/"
        f"{int(player_id)}.png"
    )
    
def display_player_status(player):
    status = str(player["STATUS"]).strip()

    if status in ["Out", "Doubtful"]:
        st.error("Injured")
        
        if st.button("View injury details", key=f"injury_{int(player['PLAYER_ID'])}"):
            st.session_state.selected_injured_player = int(player["PLAYER_ID"])
            st.switch_page("pages/injury_details.py")

    elif status in ["Monitoring", "Recovering"]:
        st.warning(status)

    elif status == "Healthy":
        st.success("Healthy")

st.set_page_config(page_title="NBA Prophet - Team Details", layout="wide")

if "selected_team" not in st.session_state:
    st.warning("No team selected.")
    st.stop()

team_name = st.session_state.selected_team

team = predictions[predictions["TEAM_NAME"] == team_name].iloc[0]

if st.button("← Back to Standings"):
    st.switch_page("app.py")

logo_url = (
    f"https://cdn.nba.com/logos/nba/"
    f"{int(team['TEAM_ID'])}/primary/L/logo.svg"
)

top_left, top_right = st.columns([1,1])

with top_left:
    st.image(
        logo_url,
        width=140
    )

    st.title(team["TEAM_NAME"])

    team["PROJECTED_RECORD"] = (
        f"{team['DISPLAY_WINS']} - {team['DISPLAY_LOSSES']}"
    )

    st.subheader(
        f"Projected Record: {team['PROJECTED_RECORD']}"
    )

    st.write(
        f"• Roster Confidence: {team['ROSTER_CONFIDENCE']}"
    )

    st.write(
        f"• Roster Sensitivity: {team['ROSTER_SENSITIVITY']}"
    )
    
with top_right:

    st.header("What Drives the Prediction?")

    positive_col, negative_col = st.columns(2)

    with positive_col:
        st.subheader("Top 3 Positive Contributors")

        for i in range(1, 4):
            feature = team[
                f"TOP_POSITIVE_CONTRIBUTOR_{i}"
            ]

            wins = team[
                f"TOP_POSITIVE_CONTRIBUTOR_{i}_WINS"
            ]

            st.write(
                f"▲ {feature}"
            )

            st.caption(
                f"+{wins:.2f} wins"
            )

    with negative_col:
        st.subheader("Top 3 Negative Contributors")

        for i in range(1, 4):
            feature = team[
                f"TOP_NEGATIVE_CONTRIBUTOR_{i}"
            ]

            wins = team[
                f"TOP_NEGATIVE_CONTRIBUTOR_{i}_WINS"
            ]

            st.write(
                f"▼ {feature}"
            )

            st.caption(
                f"{wins:.2f} wins"
            )

for column in ["RETURNING", "OUTGOING", "INCOMING"]:
    roster_changes[column] = roster_changes[column].apply(ast.literal_eval)

team_id = int(team["TEAM_ID"])

team_roster_changes = roster_changes[roster_changes["TEAM_ID"] == team_id].iloc[0]

returning_ids = team_roster_changes["RETURNING"]
outgoing_ids = team_roster_changes["OUTGOING"]
incoming_ids = team_roster_changes["INCOMING"]

future_roster["PLAYER_ID"] = future_roster["PLAYER_ID"].astype(int)
old_roster["PLAYER_ID"] = old_roster["PLAYER_ID"].astype(int)

incoming_names = future_roster[
    future_roster["PLAYER_ID"].isin(incoming_ids)
][["PLAYER_ID", "PLAYER_NAME"]]

returning_names = future_roster[
    future_roster["PLAYER_ID"].isin(returning_ids)
][["PLAYER_ID", "PLAYER_NAME"]]

outgoing_names = old_roster[
    old_roster["PLAYER_ID"].isin(outgoing_ids)
][["PLAYER_ID", "PLAYER_NAME"]]


team_future_roster = future_roster[
    future_roster["TEAM_ID"] == team_id
].copy()

player_2025_26 = player_feature_history[
    player_feature_history["SEASON"] == "2025-26"
]

team_lineup = team_future_roster.merge(
    player_2025_26[
        [
            "PLAYER_ID",
            "PPG",
            "PLUS_MINUS",
            "TS_PCT",
            "GP",
            "MPG"
        ]
    ],
    on="PLAYER_ID",
    how="left"
)

team_lineup["MPG"] = team_lineup["MPG"].fillna(0)

team_lineup = team_lineup.sort_values(
    "MPG",
    ascending=False
)

team_lineup["PLAYER_IMAGE"] = team_lineup["PLAYER_ID"].apply(
    lambda player_id:
        f"https://cdn.nba.com/headshots/nba/latest/260x190/{int(player_id)}.png"
)

team_lineup = team_lineup.merge(
    injuries[
        [
            "PLAYER_ID",
            "STATUS",
            "INJURY",
            "EXPECTED_RETURN"
        ]
    ],
    on="PLAYER_ID",
    how="left"
)

team_lineup["STATUS"] = team_lineup["STATUS"].fillna("Healthy")

scoring_leader = team_lineup.sort_values(
    "PPG",
    ascending=False
).iloc[0]

minutes_leader = team_lineup.sort_values(
    "MPG",
    ascending=False
).iloc[0]

impact_leader = team_lineup.sort_values(
    "PLUS_MINUS",
    ascending=False
).iloc[0]

efficiency_leader = team_lineup.sort_values(
    "TS_PCT",
    ascending=False
).iloc[0]

availability_leader = team_lineup.sort_values(
    "GP",
    ascending=False
).iloc[0]

unavailable_statuses = ["Out", "Doubtful"]

available_players = team_lineup[team_lineup["STATUS"] == "Healthy"]

projected_starters = available_players.head(5).copy()

bench = team_lineup[
    ~team_lineup["PLAYER_ID"].isin(
        projected_starters["PLAYER_ID"]
    )
].copy()

position_order = {
    "G": 1,
    "G-F": 2,
    "F-G": 2,
    "F": 3,
    "F-C": 4,
    "C-F": 4,
    "C": 5
}

projected_starters["POSITION_ORDER"] = (
    projected_starters["POSITION"].map(position_order)
)

projected_starters = projected_starters.sort_values(
    ["POSITION_ORDER", "MPG"],
    ascending=[True, False]
)

lineup_positions = ["PG", "SG", "SF", "PF", "C"]


bench["POSITION_ORDER"] = (
    bench["POSITION"].map(position_order)
)

bench = bench.sort_values(
    ["POSITION_ORDER", "MPG"],
    ascending=[True, False]
)

projected_starters["LINEUP_POSITION"] = lineup_positions

st.subheader("Projected Starters")

starter_columns = st.columns(len(projected_starters))

for column, (_, player) in zip(
    starter_columns,
    projected_starters.iterrows()
):
    with column:
        st.image(player["PLAYER_IMAGE"], width=120)
        st.markdown(f"### {player['LINEUP_POSITION']}")
        st.write(player["PLAYER_NAME"])
        
        display_player_status(player)

st.subheader("Projected Bench")

players_per_row = 6

for start in range(0, len(bench), players_per_row):

    bench_group = bench.iloc[
        start:start + players_per_row
    ]

    bench_columns = st.columns(
        len(bench_group)
    )

    for column, (_, player) in zip(
        bench_columns,
        bench_group.iterrows()
    ):
        with column:
            st.image(player["PLAYER_IMAGE"], width=120)
            st.markdown(f"### {player['POSITION']}")
            st.write(player["PLAYER_NAME"])
            
            display_player_status(player)

st.header("Projected Leaders")

scoring_col, minutes_col, impact_col, efficiency_col, availability_col = st.columns(5)

with scoring_col:
    st.subheader("Scoring")

    st.image(
        scoring_leader["PLAYER_IMAGE"],
        width=120
    )

    st.write(
        scoring_leader["PLAYER_NAME"]
    )

    st.metric(
        "PPG",
        f"{scoring_leader['PPG']:.1f}"
    )
    
with minutes_col:
    st.subheader("Minutes")

    st.image(
        minutes_leader["PLAYER_IMAGE"],
        width=120
    )

    st.write(
        minutes_leader["PLAYER_NAME"]
    )

    st.metric(
        "MPG",
        f"{minutes_leader['MPG']:.1f}"
    )
    
with impact_col:
    st.subheader("Impact")

    st.image(
        impact_leader["PLAYER_IMAGE"],
        width=120
    )

    st.write(
        impact_leader["PLAYER_NAME"]
    )

    if int(impact_leader["PLUS_MINUS"]) > 0:    
        st.metric(
            "PLUS_MINUS",
            f"+{impact_leader['PLUS_MINUS']:.1f}"
        )
    else:
        st.metric(
            "PLUS_MINUS",
            f"{impact_leader['PLUS_MINUS']:.1f}"
        )
        
with efficiency_col:
    st.subheader("Efficiency")

    st.image(
        efficiency_leader["PLAYER_IMAGE"],
        width=120
    )

    st.write(
        efficiency_leader["PLAYER_NAME"]
    )

    st.metric(
        "TS_PCT",
        f"{efficiency_leader['TS_PCT'] * 100}%"
    )

with availability_col:
    st.subheader("Availability")

    st.image(
        availability_leader["PLAYER_IMAGE"],
        width=120
    )

    st.write(
        availability_leader["PLAYER_NAME"]
    )

    st.metric(
        "Games Played",
        f"{round(availability_leader['GP'])}"
    )

st.title("Roster Changes")

st.subheader("Returning Players")
players_per_row = 6

for start in range(0, len(returning_names), players_per_row):

    returning_group = returning_names.iloc[
        start:start + players_per_row
    ]

    returning_columns = st.columns(
        len(returning_group)
    )

    for column, (_, player) in zip(
        returning_columns,
        returning_group.iterrows()
    ):
        with column:
            st.image(
                player_image_url(player["PLAYER_ID"]),
                width=90
            )

            st.write(
                player["PLAYER_NAME"]
            )

st.subheader("New Additions")
incoming_columns = st.columns(len(incoming_names))

for column, (_, player) in zip(
    incoming_columns,
    incoming_names.iterrows()
):
    with column:
        st.image(
            player_image_url(player["PLAYER_ID"]),
            width=90
        )
        st.write(player["PLAYER_NAME"])

st.subheader("Lost Players")
outgoing_columns = st.columns(len(outgoing_names))

for column, (_, player) in zip(
    outgoing_columns,
    outgoing_names.iterrows()
):
    with column:
        st.image(
            player_image_url(player["PLAYER_ID"]),
            width=90
        )

        st.write(player["PLAYER_NAME"])