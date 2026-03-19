# Netflix Data Analysis Dashboard

An interactive data analysis dashboard built with Python and Streamlit, analyzing 8,800+ Netflix titles.

🔗 **Live Demo:** https://netflix-data-analysis01.streamlit.app/

---

## What It Does

- Loads and cleans a real-world Netflix dataset (handles missing values, fixes malformed rating entries)
- Engineers new features: decade bins, audience rating buckets, parsed date fields, numeric movie duration, season counts
- Renders 8 interactive charts across content type, country, genre, release decade, and duration
- Sidebar filters let users drill down by content type, release year range, and audience rating
- KPI cards show live metrics that update with every filter change

## Features

| Feature | Details |
|---|---|
| Content type breakdown | Pie chart: Movies vs TV Shows |
| Rating buckets | Kids / Family / Teen / Adult — engineered from raw rating strings |
| Content added over time | Line chart by year, split by type |
| Monthly additions | Bar chart showing which months Netflix adds most content |
| Top countries | Configurable top-N bar chart (5–20 countries) |
| Top genres | Multi-label genre splitting and aggregation |
| Decade breakdown | Grouped bar chart by decade of release |
| Movie duration distribution | Histogram with mean/median annotations |
| Filterable data table | View raw filtered records |

## Tech Stack

- **Python** — data pipeline and backend logic
- **Pandas** — data cleaning, feature engineering, aggregation
- **NumPy** — numeric type handling
- **Streamlit** — interactive dashboard and filter widgets
- **Matplotlib / Seaborn** — all chart rendering

## How to Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Make sure `netflix_titles.csv` is in the same directory as `app.py`.

---

## Resume Bullets (what you can honestly say)

- Built and deployed an end-to-end interactive analytics dashboard processing 8,800+ Netflix titles with real-time sidebar filters for content type, release year, and audience rating.
- Performed data cleaning and feature engineering: handled missing values, fixed malformed rating entries, parsed date strings, and created 5 new analytical columns including decade bins, audience rating buckets, and numeric duration fields.
- Engineered a genre breakdown by splitting multi-label strings and aggregating individual genre counts across the full dataset.
- Structured codebase with modular load_data(), clean_and_engineer(), and explode_genres() functions, separating data transformation from rendering logic.
