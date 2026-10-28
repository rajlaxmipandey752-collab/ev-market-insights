# Electric Vehicle Market Performance & Insights

Tableau analytics project analysing 300,000 electric vehicle models across 15 categories, 5 battery chemistries and global
manufacturing hubs. It gives market-strategy, business-intelligence and sustainability users interactive dashboards and a data story,
embedded in a Flask web app.

**Live demo (Tableau Public):** `<paste your Tableau Public link>`

## Business questions

- Which vehicle categories contribute most to annual sales? Which manufacturers lead in market share?
- How is battery technology (LFP, NMC, NCA, Sodium-Ion, Solid-State) adopted, and how does it affect range and charging?
- Where are EVs manufactured, and how does customer satisfaction vary by category, price and battery?

## Repository structure

```
├── app.py                       Flask app (Home / Dashboard / Story / About)
├── data_preparation.py          Cleans + enriches the Kaggle CSVs -> data/ev_market_clean.csv
├── requirements.txt
├── templates/                   Jinja2 templates (Tableau Embedding API v3)
├── static/style.css
├── tableau/TABLEAU_BUILD_GUIDE.md   Calculated fields, sheets, dashboards, story
├── tableau/EVMarketPerformanceInsights.twbx   (add your workbook here)
└── docs/                        Project documentation, video script, screenshots
```

## Dataset

[Electric Vehicle Market Classification Dataset](https://www.kaggle.com/datasets/tharishreddy22/electric-vehicle-market-classification-dataset) (MIT).
Synthetic, 37 columns, manufacturer/model names are fictional. Download both CSVs into `data/` (not committed, since they total about 70 MB).

## Run it

```bash
pip install -r requirements.txt
python data_preparation.py          # creates data/ev_market_clean.csv for Tableau
# set your Tableau Public URLs in app.py (or env vars TABLEAU_DASHBOARD_URL, TABLEAU_DASHBOARD_2_URL, TABLEAU_STORY_URL)
python app.py                       # http://127.0.0.1:5000
```

## Tableau components

- 13 calculated fields + 2 parameters (Top N, Metric selector)
- 16 visualizations: bar, line, donut, 100% area, box plot, scatter, filled map, heatmap, treemap, bubble
- 2 responsive dashboards (desktop + phone layouts) with filter and highlight actions
- 1 story with 7 scenes

## Tech

Tableau Public, Python (pandas), Flask, HTML/CSS.
