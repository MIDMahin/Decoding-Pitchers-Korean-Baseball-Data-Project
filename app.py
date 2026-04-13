import re
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(page_title="KBO Pitching Dashboard", layout="wide")

st.markdown(
    """
    <style>
        .stApp {
            background: radial-gradient(circle at 10% 10%, #1e1b4b 0%, #0b1023 45%, #050816 100%);
        }
        .main-title {
            font-size: 2.4rem;
            font-weight: 800;
            margin-bottom: 0.2rem;
            color: #f8fafc;
        }
        .sub-text {
            color: #cbd5e1;
            margin-bottom: 1rem;
        }
        .kpi-card {
            background: linear-gradient(135deg, #312e81, #1d4ed8, #0ea5e9);
            color: white;
            padding: 1rem 1.2rem;
            border-radius: 14px;
            border: 1px solid rgba(148, 163, 184, 0.35);
            box-shadow: 0 8px 24px rgba(14, 165, 233, 0.25);
        }
        .kpi-label {
            font-size: 0.9rem;
            color: #e2e8f0;
        }
        .kpi-value {
            font-size: 1.6rem;
            font-weight: 800;
            margin-top: 0.2rem;
        }
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0f172a 0%, #111827 100%);
        }
    </style>
    """,
    unsafe_allow_html=True,
)
st.markdown('<div class="main-title">KBO Pitching Analysis Dashboard</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-text">Explore KBO pitching performance with interactive filters, colorful charts, and fast scouting insights.</div>',
    unsafe_allow_html=True,
)


@st.cache_data
def load_data() -> pd.DataFrame:
    data_path = Path(__file__).parent / "data" / "kbopitchingdata.csv"
    df = pd.read_csv(data_path)

    df.columns = [
        re.sub(r"[^a-z0-9]+", "_", col.strip().lower()).strip("_")
        for col in df.columns
    ]

    for col in df.columns:
        if df[col].dtype == "object" and col not in ["team", "player", "pitcher"]:
            converted = pd.to_numeric(df[col], errors="coerce")
            if converted.notna().sum() > 0:
                df[col] = converted

    if "strikeout_rate" not in df.columns and {"strikeouts", "innings_pitched"}.issubset(
        df.columns
    ):
        innings = df["innings_pitched"].replace(0, pd.NA)
        df["strikeout_rate"] = df["strikeouts"] / innings

    return df


df = load_data()

if df.empty:
    st.error("Dataset is empty. Please check `data/kbopitchingdata.csv`.")
    st.stop()


st.sidebar.header("Tune Your View")

team_options = sorted(df["team"].dropna().unique().tolist()) if "team" in df.columns else []
selected_teams = st.sidebar.multiselect("Team", options=team_options, default=team_options)

player_col = "player" if "player" in df.columns else ("pitcher" if "pitcher" in df.columns else None)
if player_col:
    player_options = sorted(df[player_col].dropna().unique().tolist())
    selected_players = st.sidebar.multiselect(
        "Player",
        options=player_options,
        default=player_options,
    )
else:
    selected_players = []

filtered_df = df.copy()
if selected_teams and "team" in filtered_df.columns:
    filtered_df = filtered_df[filtered_df["team"].isin(selected_teams)]
if player_col and selected_players:
    filtered_df = filtered_df[filtered_df[player_col].isin(selected_players)]

if filtered_df.empty:
    st.warning("No data matches the selected filters.")
    st.stop()


st.subheader("KPI Metrics")
kpi1, kpi2, kpi3 = st.columns(3)

avg_era = filtered_df["era"].mean() if "era" in filtered_df.columns else None
avg_k_rate = (
    filtered_df["strikeout_rate"].mean() if "strikeout_rate" in filtered_df.columns else None
)

if "era" in filtered_df.columns:
    top_row = filtered_df.loc[filtered_df["era"].idxmin()]
    if player_col:
        top_name = str(top_row.get(player_col, "N/A"))
    else:
        top_name = str(top_row.get("team", "N/A"))
else:
    top_name = "N/A"

kpi1.markdown(
    f"""
    <div class="kpi-card">
        <div class="kpi-label">Avg ERA</div>
        <div class="kpi-value">{f"{avg_era:.3f}" if avg_era is not None else "N/A"}</div>
    </div>
    """,
    unsafe_allow_html=True,
)
kpi2.markdown(
    f"""
    <div class="kpi-card">
        <div class="kpi-label">Top Pitcher/Team</div>
        <div class="kpi-value">{top_name}</div>
    </div>
    """,
    unsafe_allow_html=True,
)
kpi3.markdown(
    f"""
    <div class="kpi-card">
        <div class="kpi-label">Avg Strikeout Rate</div>
        <div class="kpi-value">{f"{avg_k_rate:.3f}" if avg_k_rate is not None else "N/A"}</div>
    </div>
    """,
    unsafe_allow_html=True,
)


tab1, tab2 = st.tabs(["Leaderboard", "Relationship"])

with tab1:
    st.subheader("ERA Leaderboard")
    if "era" in filtered_df.columns:
        leaderboard_cols = ["era"]
        if player_col:
            leaderboard_cols.insert(0, player_col)
        elif "team" in filtered_df.columns:
            leaderboard_cols.insert(0, "team")
        if "year" in filtered_df.columns:
            leaderboard_cols.append("year")

        leaderboard = (
            filtered_df[leaderboard_cols]
            .dropna(subset=["era"])
            .sort_values("era", ascending=True)
            .head(10)
        )

        x_col = player_col if player_col else "team"
        fig_leaderboard = px.bar(
            leaderboard,
            x=x_col,
            y="era",
            color="era",
            color_continuous_scale="Turbo",
            title="Top 10 Lowest ERA",
            labels={x_col: x_col.title(), "era": "ERA"},
        )
        fig_leaderboard.update_layout(
            xaxis_tickangle=-30,
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig_leaderboard, width="stretch")
        st.dataframe(leaderboard, width="stretch")
    else:
        st.info("`era` column not available for leaderboard.")

with tab2:
    st.subheader("Strikeout Rate vs ERA")
    if {"strikeout_rate", "era"}.issubset(filtered_df.columns):
        hover_cols = [c for c in [player_col, "team", "year"] if c]
        fig_scatter = px.scatter(
            filtered_df,
            x="strikeout_rate",
            y="era",
            color="team" if "team" in filtered_df.columns else None,
            hover_data=hover_cols,
            title="K Rate vs ERA",
            labels={
                "strikeout_rate": "Strikeout Rate (SO/IP)",
                "era": "ERA",
            },
        )
        fig_scatter.update_traces(marker=dict(size=11, opacity=0.85, line=dict(width=1, color="#0b1023")))
        fig_scatter.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig_scatter, width="stretch")
    else:
        st.info("Need both `strikeout_rate` and `era` columns for this plot.")
    