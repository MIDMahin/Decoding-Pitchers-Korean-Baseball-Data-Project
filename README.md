## KBO Pitching Analytics Dashboard

Data analysis and interactive visualization project for Korean Baseball Organization (KBO) pitching data.  
This project explores pitching performance trends, engineers core metrics, trains a simple ERA prediction model, and presents insights in a Streamlit dashboard.

## Project Highlights

- Cleaned and analyzed KBO pitching dataset with Python and pandas
- Engineered key pitching metrics (`strikeout_rate`, `walk_rate`, `k_bb_ratio`)
- Built visual analysis (leaderboards, distributions, heatmaps, scatter plots)
- Applied KMeans clustering to identify pitching archetypes
- Trained a Linear Regression model to predict ERA
- Delivered an interactive Streamlit app for quick exploration

## Dashboard Screenshots

### ERA Leaderboard
![ERA Leaderboard](screenshots/ERA%20Leaderboard.png)

### Strikeout Rate vs ERA
![Strikeout Rate vs ERA](screenshots/Strikeout%20Rate%20vs%20ERA.png)

## Tech Stack

- Python
- pandas, numpy
- matplotlib, seaborn, plotly
- scikit-learn
- Streamlit

## Project Structure

- `app.py` - Streamlit dashboard app
- `notebooks/analysis.ipynb` - end-to-end data analysis and modeling notebook
- `dataset/` - source dataset files
- `screenshots/` - dashboard screenshots

## Run Locally

1. Launch app:
   ```bash
   python -m streamlit run app.py
   ```

## Requirements

- Python 3.10+
- `streamlit`
- `pandas`
- `plotly`
- `matplotlib`
- `seaborn`
- `scikit-learn`
- `numpy`
    