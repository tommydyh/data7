# ⚽ 2026 World Cup Scouter & Match Predictor Dashboard

An AI-powered analytics dashboard for the 2026 FIFA World Cup, featuring player performance analysis through K-Means clustering and match outcome prediction simulation.

## 📁 Project Structure

```
d:\cursor data 2\
├── .streamlit/
│   └── config.toml              # Global UI Theme Configuration
├── src/
│   ├── __init__.py              # Module initialization
│   ├── data_pipeline.py         # ETL, Fuzzy Matching, Feature Engineering
│   └── model_pipeline.py        # K-Means Clustering & Prediction Engine
├── app.py                       # Main Streamlit Application
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## 🎨 Theme Configuration

| Element | Color Code |
|---------|------------|
| Primary (Accent) | `#00E676` (Fluorescent Green / Mint) |
| Background | `#0B0F19` (Midnight Dark Blue) |
| Card Background | `#1E2530` |
| Text | `#FFFFFF` |

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Steps

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Verify source data files are in place:**
   - `archive (3)\fifa_world_cup_2026_golden_dataset.csv`
   - `archive (2)\male_players.csv`
   - `archive (2)\male_teams.csv`

## 🚀 Running the Application

### 📌 One-Click Launch (推荐 / Recommended)

**双击 `启动仪表盘.bat` 文件即可直接启动！**

仪表盘会自动在浏览器中打开。

---

### 🌐 Public Internet Deployment

**Option 1: Streamlit Cloud (Recommended)**

1. Upload code to GitHub
2. Visit https://share.streamlit.io
3. Connect your GitHub repository
4. Click "Deploy"

**Free forever! Get a permanent public URL like:**
```
https://your-app.share.streamlit.io
```

📖 See [`部署指南.md`](部署指南.md) for detailed instructions.

**Option 2: ngrok (Quick Sharing)**

Download ngrok from https://ngrok.com/download, then run:

```bash
streamlit run app.py
ngrok http 8501
```

Or use the provided script: **双击 `一键公网分享.bat`**

**Option 3: Railway / Render**

See [`部署指南.md`](部署指南.md) for professional hosting options.

---

### Manual Start (Local Only)

**Start the Streamlit App**
```bash
streamlit run app.py
```

The dashboard will open in your browser at `http://localhost:8501`

### Run Data Processing Only

To run the ETL pipeline separately:
```bash
python -c "from src.data_pipeline import run_pipeline; run_pipeline()"
```

To run the clustering pipeline:
```bash
python -c "from src.model_pipeline import PlayerClusterEngine; PlayerClusterEngine().run_pipeline()"
```

## 📊 Features

### View A: Player Performance Dashboard

1. **KPI Matrix** - Glassmorphism cards displaying:
   - Total Scouted Players
   - Average Age
   - Maximum Market Value
   - Top Rated Team

2. **Macro View (Scatter Plot)** - Interactive visualization:
   - X-Axis: Passing Attribute
   - Y-Axis: Defending Attribute
   - Color-coded by AI-generated cluster labels
   - Hover tooltips showing player details

3. **Micro View (Player Deep Dive)** - Split-screen analysis:
   - **Left Column:** Player search with autocomplete, player info card
   - **Right Column:** 6-axis Radar Chart with attribute visualization

4. **Recommendation Engine (AI 平替)**:
   - Finds 3 most similar players based on Euclidean distance
   - Similarity calculated within the same cluster
   - Displays as horizontal UI badges

### View B: Match Outcome Prediction System

- Dual dropdowns for Home/Away team selection
- Match type selector (Group Stage, Knockout rounds, Final)
- Win probability visualization with stylized progress bars
- *Note: Currently simulated UI skeleton for demonstration*

## 🧠 Player Clustering Roles

The K-Means algorithm (4 clusters) automatically assigns players to roles:

| Cluster | Role | Typical Attributes |
|---------|------|-------------------|
| 0 | Clinical Finisher | High Shooting, lower Defending |
| 1 | Midfield Maestro | Balanced Passing & Dribbling |
| 2 | Defensive Anchor | High Defending & Physicality |
| 3 | Physical Engine | High Physicality & Defending |

## 🔧 Technical Details

### Data Pipeline (Milestone 1)
- Name standardization using Unicode normalization
- Left join preserving complete World Cup roster
- Positional mean imputation for missing values
- CSV serialization at `final_squad_with_skills.csv`

### Model Pipeline (Milestone 2)
- Feature selection: Shooting, Passing, Dribbling, Defending, Physicality
- StandardScaler for feature parity
- K-Means clustering (n=4, random_state=42, n_init=10)
- Automatic centroid-based role mapping
- Silhouette score evaluation

### Frontend (Milestone 3)
- Streamlit for UI framework
- Plotly Express & Graph Objects for visualizations
- Custom CSS for glassmorphism effects
- Tab-based navigation between dashboards

## 📝 Development Notes

- All processing is cached using Streamlit's `@st.cache_data`
- No local image dependencies - uses system fonts and Unicode emojis
- Fully responsive layout with golden-ratio column splits
- Dark theme integration across all Plotly charts

## 🐛 Troubleshooting

### ModuleNotFoundError
Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Data loading errors
Verify source CSV files exist at the specified paths in `src/data_pipeline.py`.

### Port already in use
Change Streamlit port:
```bash
streamlit run app.py --server.port 8502
```

## 📄 License

This project is for educational and demonstration purposes.

---

Built with ❤️ using Streamlit, Plotly, and Scikit-learn