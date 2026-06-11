# ⚽ 2026 World Cup Scouter & Match Predictor Dashboard

![Streamlit App](https://img.shields.io/badge/Streamlit-App-red?logo=streamlit)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

AI-powered analytics dashboard for the 2026 FIFA World Cup, featuring player performance analysis through K-Means clustering and match outcome prediction.

## 🌐 Live Demo

**[Launch Dashboard →](https://dongyaohua-sport-task.share.streamlit.io)**

> Deployed on Streamlit Cloud • Free Forever • Always Online

---

## ✨ Features

### Player Performance Dashboard

| Feature | Description |
|---------|-------------|
| 📊 **KPI Matrix** | Total players, average age, max market value, top team |
| 🎯 **Scatter Plot** | Interactive visualization of Passing vs Defending skills |
| 👤 **Player Deep Dive** | Search players, view radar charts, explore attributes |
| 🤖 **AI Recommendations** | Find 3 similar players based on playstyle |
| 🎨 **Dark Theme** | Glassmorphism design with Mint Green accents |

### Match Prediction System

- Dual team selection interface
- Match type selector
- Win probability visualization

---

## 🧠 AI Clustering

The K-Means algorithm assigns players to 4 roles:

| Cluster | Role | Typical Attributes |
|---------|------|-------------------|
| 0 | 🎯 Clinical Finisher | High Shooting, lower Defending |
| 1 | 🎪 Midfield Maestro | Balanced Passing & Dribbling |
| 2 | 🛡️ Defensive Anchor | High Defending & Physicality |
| 3 | 💪 Physical Engine | High Physicality & Defending |

---

## 🚀 Quick Start

### Running Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

### One-Click Launch

**Windows:** Double-click `启动仪表盘.bat`

---

## 📦 Project Structure

```
dongyaohua-sport-task/
├── app.py                      # Main Streamlit app
├── requirements.txt            # Python dependencies
├── src/
│   ├── data_pipeline.py        # ETL & feature engineering
│   └── model_pipeline.py       # K-Means clustering engine
└── .streamlit/
    ├── config.toml            # Theme configuration
    └── secrets.toml           # App secrets
```

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| Frontend | Streamlit |
| Visualization | Plotly (Express & Graph Objects) |
| ML/Clustering | Scikit-learn (K-Means) |
| Data Processing | Pandas, NumPy |

---

## 📊 Data Pipeline

### ETL Process

1. **Name Standardization** - Unicode normalization for fuzzy matching
2. **Left Join** - Preserve complete World Cup roster
3. **Positional Mean Imputation** - Fill missing values by position
4. **Feature Scaling** - StandardScaler for clustering

---

## 🎨 Theme

| Element | Color |
|---------|-------|
| Primary | `#00E676` (Mint Green) |
| Background | `#0B0F19` (Midnight Blue) |
| Card | `#1E2530` |
| Text | `#FFFFFF` |

---

## 📖 Documentation

- [使用说明.md](使用说明.md) - 中文快速指南
- [部署指南.md](部署指南.md) - 部署教程
- [GitHub上传指南.md](GitHub上传指南.md) - GitHub 上传步骤

---

## 🤝 Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

---

## 📄 License

This project is for educational and demonstration purposes.

---

## 🙏 Acknowledgments

- Data sources: FIFA 24 & World Cup 2026 datasets
- Built with ❤️ using [Streamlit](https://streamlit.io)

---

**Deployed on Streamlit Cloud • Built by tommydyh**