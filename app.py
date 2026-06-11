"""
2026 World Cup Scouter & Match Predictor Dashboard
===================================================
Streamlit frontend for player performance analysis and match prediction.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import euclidean_distances
import os

# Import custom modules
from src.data_pipeline import run_pipeline as run_etl
from src.model_pipeline import PlayerClusterEngine, calculate_kpis

# ============================================================
# CONFIGURATION
# ============================================================
PROCESSED_DATA_PATH = "final_squad_with_skills.csv"
LABELED_DATA_PATH = "final_squad_labeled.csv"

# Data source files
SQUADS_DATA_PATH = "data/world_cup_squads.csv"
PLAYERS_DATA_PATH = "data/world_cup_players.csv"
TEAMS_DATA_PATH = "data/world_cup_teams.csv"

# Feature columns (lowercase to match actual CSV)
FEATURE_COLUMNS = ["shooting", "passing", "dribbling", "defending", "physic"]

# Column name to display title mapping
COLUMN_TITLES = {
    "overall": "Overall",
    "pace": "Pace",
    "shooting": "Shooting",
    "passing": "Passing",
    "dribbling": "Dribbling",
    "defending": "Defending",
    "physic": "Physicality"
}

def get_column_title(col_name: str) -> str:
    """Convert column name to display title."""
    return COLUMN_TITLES.get(col_name, col_name.capitalize())

# Theme colors matching config.toml
THEME_COLORS = {
    "primary": "#00E676",
    "bg": "#0B0F19",
    "card": "#1E2530",
    "text": "#FFFFFF",
    "secondary": "#FF6B6B"
}

# Cluster colors for visualization
CLUSTER_COLORS = {
    0: "#00E676",  # Clinical Finisher - Mint Green
    1: "#00B4D8",  # Midfield Maestro - Cyan
    2: "#FF6B6B",  # Defensive Anchor - Coral Red
    3: "#F4D03F"   # Physical Engine - Yellow Gold
}


# ============================================================
# CUSTOM CSS FOR GLASSMORPHISM EFFECTS
# ============================================================
def load_custom_css():
    """Inject custom CSS for modern UI styling."""
    st.markdown("""
    <style>
    /* Glassmorphism Card Style */
    .glass-card {
        background: rgba(30, 37, 48, 0.8);
        backdrop-filter: blur(10px);
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3),
                    0 1px 3px rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(0, 230, 118, 0.2);
        margin-bottom: 10px;
    }

    /* KPI Metric Card */
    .kpi-card {
        background: linear-gradient(135deg, rgba(30, 37, 48, 0.9), rgba(11, 15, 25, 0.9));
        border-radius: 12px;
        padding: 15px;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.4),
                    inset 0 1px 0 rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(0, 230, 118, 0.3);
        text-align: center;
    }

    .kpi-value {
        font-size: 2.5rem;
        font-weight: bold;
        color: #00E676;
        margin: 10px 0;
    }

    .kpi-label {
        font-size: 0.9rem;
        color: rgba(255, 255, 255, 0.7);
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Similar Player Badge */
    .similar-badge {
        display: inline-flex;
        align-items: center;
        background: linear-gradient(135deg, rgba(0, 230, 118, 0.2), rgba(0, 180, 216, 0.2));
        border: 1px solid #00E676;
        border-radius: 20px;
        padding: 8px 15px;
        margin: 5px;
        color: #FFFFFF;
        font-size: 0.9rem;
    }

    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: rgba(30, 37, 48, 0.5);
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
    }

    /* Progress Bar Customization */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #00E676, #00B4D8);
    }
    </style>
    """, unsafe_allow_html=True)


# ============================================================
# DATA LOADING FUNCTIONS
# ============================================================
@st.cache_data
def load_or_process_data():
    """
    Load processed data or run ETL pipeline if not available.
    Cached to avoid reloading on each interaction.
    """
    # Check if labeled data exists
    if os.path.exists(LABELED_DATA_PATH):
        return pd.read_csv(
            LABELED_DATA_PATH,
            encoding='utf-8',
            quotechar='"',
            skipinitialspace=True,
            on_bad_lines='skip',
            engine='python'
        )

    # Check if source data exists
    if not os.path.exists(SQUADS_DATA_PATH):
        st.error("❌ Data files not found!")
        st.info("Please ensure data files are in the 'data/' folder.")
        return pd.DataFrame()

    # Run ETL pipeline
    with st.spinner("🔄 Processing data..."):
        df = run_etl()

    # Run clustering
    engine = PlayerClusterEngine()
    labeled_df = engine.run_pipeline(
        input_path=PROCESSED_DATA_PATH,
        output_path=LABELED_DATA_PATH
    )

    return labeled_df


@st.cache_data
def load_teams():
    """Load FIFA 24 teams data for match prediction."""
    teams_path = "data/world_cup_teams.csv"
    if os.path.exists(teams_path):
        teams_df = pd.read_csv(
            teams_path,
            encoding='utf-8',
            quotechar='"',
            skipinitialspace=True,
            on_bad_lines='skip',
            engine='python'
        )
        # Get unique team names
        team_names = teams_df["Name"].unique().tolist()
        return sorted(team_names)
    return []


# ============================================================
# DASHBOARD COMPONENTS
# ============================================================
def render_kpi_matrix(df: pd.DataFrame):
    """
    Render KPI matrix with glassmorphism cards.

    Args:
        df: Player data DataFrame
    """
    st.markdown('<h2 style="color: #FFFFFF; margin-bottom: 20px;">📊 Dashboard KPIs</h2>', unsafe_allow_html=True)

    # Calculate KPIs
    total_players = len(df)
    avg_age = df.get("age", pd.Series([0])).mean()
    max_value = df.get("value", pd.Series([0])).max()
    top_team = df.get("nationality", pd.Series(["Unknown"])).mode()[0]

    # 4-column layout
    cols = st.columns(4)

    with cols[0]:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Total Players</div>
            <div class="kpi-value">{total_players}</div>
            <div style="color: rgba(255,255,255,0.5);">🎯 Scouted</div>
        </div>
        """, unsafe_allow_html=True)

    with cols[1]:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Average Age</div>
            <div class="kpi-value">{avg_age:.1f}</div>
            <div style="color: rgba(255,255,255,0.5);">🎂 Years</div>
        </div>
        """, unsafe_allow_html=True)

    with cols[2]:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Max Market Value</div>
            <div class="kpi-value">€{max_value/1e6:.1f}M</div>
            <div style="color: rgba(255,255,255,0.5);">💰 Highest</div>
        </div>
        """, unsafe_allow_html=True)

    with cols[3]:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Top Team</div>
            <div class="kpi-value" style="font-size: 1.5rem;">{top_team}</div>
            <div style="color: rgba(255,255,255,0.5);">🏆 Best Roster</div>
        </div>
        """, unsafe_allow_html=True)


def render_scatter_plot(df: pd.DataFrame):
    """
    Render interactive scatter plot with cluster coloring.

    Args:
        df: Player data DataFrame with cluster labels
    """
    st.markdown('<h2 style="color: #FFFFFF; margin: 30px 0 20px 0;">🎯 Player Performance Map</h2>', unsafe_allow_html=True)

    # Ensure required columns exist
    required_cols = ["passing", "ending", "cluster_label", "name", "nationality", "role"]
    available_cols = [c for c in required_cols if c in df.columns]

    if len(available_cols) < 5:
        st.warning("⚠️ Insufficient columns for visualization. Please ensure data processing is complete.")
        return

    # Determine x and y axes
    x_col = "passing" if "passing" in df.columns else "overall"
    y_col = "ending" if "ending" in df.columns else "shooting"

    # Create scatter plot
    fig = px.scatter(
        df,
        x=x_col,
        y=y_col,
        color="cluster_label",
        hover_data={
            "name": True,
            "nationality": True,
            "role": True,
            "cluster_label": False
        },
        color_discrete_map=CLUSTER_COLORS,
        title="",
        height=500
    )

    # Apply dark theme customization
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor=THEME_COLORS["bg"],
        plot_bgcolor=THEME_COLORS["bg"],
        font=dict(color=THEME_COLORS["text"]),
        xaxis=dict(
            gridcolor="rgba(255,255,255,0.1)",
            title=get_column_title(x_col)
        ),
        yaxis=dict(
            gridcolor="rgba(255,255,255,0.1)",
            title=get_column_title(y_col)
        ),
        hoverlabel=dict(
            bgcolor=THEME_COLORS["card"],
            font_size=13,
            font_family="Arial"
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(l=0, r=0, t=0, b=0)
    )

    st.plotly_chart(fig, use_container_width=True)


def render_radar_chart(player_data: pd.Series, feature_cols: list):
    """
    Render 6-axis radar chart for player attributes.

    Args:
        player_data: Series containing player's attributes
        feature_cols: List of feature column names
    """
    # Add overall if not present
    radar_features = feature_cols.copy()
    if "overall" in player_data.index:
        radar_features.insert(0, "overall")
    else:
        radar_features.insert(0, "overall")
        # Use average if overall missing
        player_data = player_data.copy()
        player_data["overall"] = player_data[feature_cols].mean()

    # Extract values
    values = [player_data.get(f, 70) for f in radar_features]

    # Convert to display titles for the chart
    display_labels = [get_column_title(f) for f in radar_features]

    # Create radar chart
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=display_labels,  # Use display titles for the chart labels
        fill='toself',
        fillcolor=f'rgba(0, 230, 118, 0.3)',
        line=dict(color=THEME_COLORS["primary"], width=2),
        name=player_data.get("name", "Player")
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                gridcolor="rgba(255,255,255,0.1)",
                tickfont=dict(color="rgba(255,255,255,0.7)")
            ),
            angularaxis=dict(
                gridcolor="rgba(255,255,255,0.1)",
                tickfont=dict(color="#FFFFFF", size=12)
            ),
            bgcolor=THEME_COLORS["card"]
        ),
        showlegend=True,
        template="plotly_dark",
        paper_bgcolor=THEME_COLORS["bg"],
        height=400,
        margin=dict(l=0, r=0, t=30, b=0)
    )

    st.plotly_chart(fig, use_container_width=True)


def get_similar_players(df: pd.DataFrame, player_name: str, top_n: int = 3):
    """
    Find similar players using Euclidean distance within same cluster.

    Args:
        df: Player DataFrame
        player_name: Name of reference player
        top_n: Number of similar players

    Returns:
        DataFrame of similar players
    """
    # Find reference player
    player_row = df[df["name"].str.lower() == player_name.lower()]

    if len(player_row) == 0:
        return pd.DataFrame()

    player_row = player_row.iloc[0]
    cluster_id = player_row.get("cluster_label")

    if pd.isna(cluster_id):
        return pd.DataFrame()

    # Get players in same cluster
    feature_cols = FEATURE_COLUMNS
    available_features = [c for c in feature_cols if c in df.columns]

    cluster_players = df[df["cluster_label"] == cluster_id].copy()
    cluster_players = cluster_players[cluster_players["name"] != player_row["name"]]

    # Calculate distances
    ref_features = player_row[available_features].values.reshape(1, -1)
    player_features = cluster_players[available_features].values

    distances = euclidean_distances(ref_features, player_features)[0]
    cluster_players["distance"] = distances

    # Return top N
    return cluster_players.nsmallest(top_n, "distance")


def render_player_analysis(df: pd.DataFrame):
    """
    Render player search, info card, and radar chart in split view.

    Args:
        df: Player data DataFrame
    """
    st.markdown('<h2 style="color: #FFFFFF; margin: 30px 0 20px 0;">👤 Player Deep Dive</h2>', unsafe_allow_html=True)

    # Golden ratio columns: 1 : 2
    col_left, col_right = st.columns([1, 2])

    # ========== LEFT COLUMN ==========
    with col_left:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)

        st.markdown("### 🔍 Search Player")
        player_names = sorted(df["name"].unique().tolist())
        selected_player = st.selectbox(
            "Select a player",
            player_names,
            label_visibility="collapsed"
        )

        st.markdown('</div>', unsafe_allow_html=True)

        # Player Info Card
        if selected_player:
            player_data = df[df["name"] == selected_player].iloc[0]

            st.markdown('<div class="glass-card" style="margin-top: 20px;">', unsafe_allow_html=True)

            # Name and role
            role = player_data.get("role", "Unknown")
            st.markdown(f"<h3 style='color: #00E676;'>{selected_player}</h3>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: rgba(255,255,255,0.7); margin: 5px 0;'>{role}</p>", unsafe_allow_html=True)

            st.markdown("---", unsafe_allow_html=True)

            # Metadata with emojis
            st.markdown("#### 📋 Player Info")
            metadata_cols = [
                ("nationality", "🏳️", "Nationality"),
                ("age", "🎂", "Age"),
                ("position", "⚽", "Position")
            ]

            for col, emoji, label in metadata_cols:
                value = player_data.get(col, "N/A")
                st.markdown(f"**{emoji} {label}:** `{value}`")

            # Club if available
            if "Name_fifa" in player_data.index or "club" in df.columns:
                club = player_data.get("Name_fifa") or player_data.get("club", "N/A")
                st.markdown(f"**🏟️ Club:** `{club}`")

            st.markdown('</div>', unsafe_allow_html=True)

    # ========== RIGHT COLUMN ==========
    with col_right:
        if selected_player:
            player_data = df[df["name"] == selected_player].iloc[0]

            st.markdown('<div class="glass-card">', unsafe_allow_html=True)

            # Radar Chart
            feature_cols = FEATURE_COLUMNS
            available_features = [c for c in feature_cols if c in df.columns]

            if len(available_features) >= 3:
                render_radar_chart(player_data, available_features)
            else:
                st.warning("⚠️ Insufficient features for radar chart")

            # Similar Players (Recommendation Engine)
            similar_players = get_similar_players(df, selected_player, top_n=3)

            if len(similar_players) > 0:
                st.markdown("---", unsafe_allow_html=True)
                st.markdown("#### 🎯 Similar Playstyle Profiles (AI 平替)")

                for _, similar in similar_players.iterrows():
                    name = similar["name"]
                    nationality = similar.get("nationality", "")
                    role = similar.get("role", "")
                    distance = similar["distance"]

                    badge_html = f"""
                    <div class="similar-badge">
                        <strong>{name}</strong>
                        <span style="margin-left: 8px; opacity: 0.8;">
                            {nationality} • {role} • {distance:.1f} similarity
                        </span>
                    </div>
                    """
                    st.markdown(badge_html, unsafe_allow_html=True)
            else:
                st.info("ℹ️ No similar players found in database")

            st.markdown('</div>', unsafe_allow_html=True)


def render_match_prediction():
    """
    Render Match Outcome Prediction UI skeleton.
    """
    st.markdown('<h2 style="color: #FFFFFF; margin: 20px 0;">⚽ Match Prediction System</h2>', unsafe_allow_html=True)

    # Load teams
    teams = load_teams()

    if not teams:
        st.warning("⚠️ Teams data not available")
        return

    # Two columns for team selection
    col_home, col_away = st.columns(2)

    with col_home:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 🏠 Home Team")
        home_team = st.selectbox("Select home team", teams, key="home")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_away:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### ✈️ Away Team")
        away_team = st.selectbox("Select away team", teams, key="away")
        st.markdown('</div>', unsafe_allow_html=True)

    # Match type
    st.markdown('<div class="glass-card" style="margin: 20px 0;">', unsafe_allow_html=True)
    match_type = st.selectbox(
        "Match Type",
        ["Group Stage", "Round of 16", "Quarter-Final", "Semi-Final", "Final"],
        label_visibility="visible"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # Prediction display (simulated)
    st.markdown('<h3 style="color: #FFFFFF; margin: 30px 0 20px 0;">📊 Win Probability</h3>', unsafe_allow_html=True)

    # Generate simulated probabilities
    import random
    random.seed(hash(home_team + away_team + match_type))
    home_prob = random.uniform(25, 55)
    draw_prob = random.uniform(20, 30)
    away_prob = 100 - home_prob - draw_prob

    # 3-column metric blocks
    cols = st.columns(3)

    with cols[0]:
        st.markdown(f"""
        <div class="kpi-card" style="border-color: #00E676;">
            <div class="kpi-label">Home Win</div>
            <div class="kpi-value">{home_prob:.1f}%</div>
            <div style="color: rgba(0,230,118,0.7); font-size: 2rem;">🏠</div>
        </div>
        """, unsafe_allow_html=True)

    with cols[1]:
        st.markdown(f"""
        <div class="kpi-card" style="border-color: #F4D03F;">
            <div class="kpi-label">Draw</div>
            <div class="kpi-value">{draw_prob:.1f}%</div>
            <div style="color: rgba(244,208,63,0.7); font-size: 2rem;">🤝</div>
        </div>
        """, unsafe_allow_html=True)

    with cols[2]:
        st.markdown(f"""
        <div class="kpi-card" style="border-color: #FF6B6B;">
            <div class="kpi-label">Away Win</div>
            <div class="kpi-value">{away_prob:.1f}%</div>
            <div style="color: rgba(255,107,107,0.7); font-size: 2rem;">✈️</div>
        </div>
        """, unsafe_allow_html=True)

    # Stylized progress bar
    st.markdown('<div style="margin: 30px 0 10px 0;">', unsafe_allow_html=True)

    fig = go.Figure(go.Bar(
        x=[home_prob, draw_prob, away_prob],
        y=["Home Win", "Draw", "Away Win"],
        orientation='h',
        marker=dict(
            color=['#00E676', '#F4D03F', '#FF6B6B'],
            line=dict(color='white', width=1)
        ),
        text=[f"{home_prob:.1f}%", f"{draw_prob:.1f}%", f"{away_prob:.1f}%"],
        textposition='inside',
        textfont=dict(color='white', size=12)
    ))

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor=THEME_COLORS["bg"],
        plot_bgcolor=THEME_COLORS["bg"],
        font=dict(color=THEME_COLORS["text"]),
        xaxis=dict(
            title="Probability (%)",
            range=[0, 100],
            gridcolor="rgba(255,255,255,0.1)",
            tickfont=dict(color="rgba(255,255,255,0.7)")
        ),
        yaxis=dict(
            gridcolor="rgba(255,255,255,0.1)",
            tickfont=dict(color="#FFFFFF", size=12)
        ),
        height=200,
        margin=dict(l=80, r=20, t=20, b=40),
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

    st.info("ℹ️ This is a simulated UI skeleton. Real prediction engine integration coming soon.")


# ============================================================
# MAIN APPLICATION
# ============================================================
def main():
    """Main Streamlit application entry point."""

    # Page configuration
    st.set_page_config(
        page_title="2026 World Cup Scouter",
        page_icon="⚽",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Load custom CSS
    load_custom_css()

    # Header
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h1 style="color: #00E676; font-size: 2.5rem; margin: 0;">
            ⚽ 2026 World Cup Scouter & Match Predictor
        </h1>
        <p style="color: rgba(255,255,255,0.6); margin-top: 10px;">
            AI-Powered Player Analysis • K-Means Clustering • Match Outcome Prediction
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Load data
    try:
        df = load_or_process_data()
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        st.info("Please ensure the source CSV files are in the correct locations.")
        return

    # Create tabs for different views
    tab1, tab2 = st.tabs(["📊 Player Performance Dashboard", "⚽ Match Prediction"])

    with tab1:
        # KPI Matrix
        render_kpi_matrix(df)

        # Macro View - Scatter Plot
        render_scatter_plot(df)

        # Micro View - Player Analysis
        render_player_analysis(df)

    with tab2:
        # Match Prediction UI
        render_match_prediction()

    # Footer
    st.markdown("""
    <div style="text-align: center; padding: 30px 0; margin-top: 40px; border-top: 1px solid rgba(255,255,255,0.1);">
        <p style="color: rgba(255,255,255,0.4); font-size: 0.9rem;">
            2026 World Cup Scouter Dashboard • Built with Streamlit, Plotly & Scikit-learn
        </p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()