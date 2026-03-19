import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# ─────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────
st.set_page_config(
    page_title="Netflix Data Analysis Dashboard",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 Netflix Data Analysis Dashboard")
st.markdown("Explore trends across **8,800+ Netflix titles** — filter by type, country, rating, and year.")
st.markdown("---")

# ─────────────────────────────────────────
# 1. DATA LOADING
# ─────────────────────────────────────────
@st.cache_data
def load_data(path: str = "netflix_titles.csv") -> pd.DataFrame:
    """Load raw Netflix CSV."""
    return pd.read_csv(path)

# ─────────────────────────────────────────
# 2. DATA CLEANING & FEATURE ENGINEERING
# ─────────────────────────────────────────
def clean_and_engineer(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean missing values, parse dates, and engineer new features.
    Returns a cleaned DataFrame ready for analysis.
    """
    df = df.copy()

    # --- Drop rows missing critical fields ---
    df = df.dropna(subset=["type", "release_year"])

    # --- Fill non-critical nulls ---
    df["country"]  = df["country"].fillna("Unknown")
    df["rating"]   = df["rating"].fillna("Not Rated")
    df["director"] = df["director"].fillna("Unknown")
    df["cast"]     = df["cast"].fillna("Unknown")

    # --- Fix erroneous ratings (some duration values ended up in rating column) ---
    valid_ratings = [
        "G", "PG", "PG-13", "R", "NC-17", "NR", "UR",
        "TV-Y", "TV-Y7", "TV-Y7-FV", "TV-G", "TV-PG", "TV-14", "TV-MA"
    ]
    df.loc[~df["rating"].isin(valid_ratings), "rating"] = "Not Rated"

    # --- Parse date_added to datetime ---
    df["date_added"]  = pd.to_datetime(df["date_added"].str.strip(), format="%B %d, %Y", errors="coerce")
    df["year_added"]  = df["date_added"].dt.year
    df["month_added"] = df["date_added"].dt.month
    df["month_name"]  = df["date_added"].dt.strftime("%b")

    # --- Feature: decade bins ---
    df["decade"] = (df["release_year"] // 10 * 10).astype(str) + "s"

    # --- Feature: audience rating buckets ---
    kids   = ["TV-Y", "TV-Y7", "TV-Y7-FV", "TV-G", "G"]
    family = ["TV-PG", "PG"]
    teen   = ["TV-14", "PG-13"]
    adult  = ["TV-MA", "R", "NC-17"]

    def bucket(r):
        if r in kids:   return "Kids"
        if r in family: return "Family"
        if r in teen:   return "Teen"
        if r in adult:  return "Adult"
        return "Unrated"

    df["rating_bucket"] = df["rating"].apply(bucket)

    # --- Feature: primary country (some entries list multiple) ---
    df["primary_country"] = df["country"].str.split(",").str[0].str.strip()

    # --- Feature: movie duration in minutes (numeric) ---
    df["duration_minutes"] = df.apply(
        lambda r: int(r["duration"].replace(" min", ""))
        if r["type"] == "Movie" and pd.notna(r["duration"]) and "min" in str(r["duration"])
        else np.nan,
        axis=1
    )

    # --- Feature: number of seasons for TV Shows ---
    df["num_seasons"] = df.apply(
        lambda r: int(r["duration"].split(" ")[0])
        if r["type"] == "TV Show" and pd.notna(r["duration"]) and "Season" in str(r["duration"])
        else np.nan,
        axis=1
    )

    return df

# ─────────────────────────────────────────
# 3. GENRE UTILITY
# ─────────────────────────────────────────
def explode_genres(df: pd.DataFrame) -> pd.Series:
    """Split multi-label genre strings and return a flat Series of all genres."""
    return df["listed_in"].str.split(",").explode().str.strip()

# ─────────────────────────────────────────
# LOAD & CLEAN
# ─────────────────────────────────────────
raw_df = load_data()
df     = clean_and_engineer(raw_df)

# ─────────────────────────────────────────
# SIDEBAR FILTERS
# ─────────────────────────────────────────
st.sidebar.header("🔍 Filters")

content_type = st.sidebar.multiselect(
    "Content Type",
    options=df["type"].unique().tolist(),
    default=df["type"].unique().tolist()
)

year_min, year_max = int(df["release_year"].min()), int(df["release_year"].max())
year_range = st.sidebar.slider(
    "Release Year Range",
    min_value=year_min, max_value=year_max,
    value=(2000, year_max)
)

top_n_countries = st.sidebar.slider("Top N Countries to Show", 5, 20, 10)

rating_buckets = st.sidebar.multiselect(
    "Audience Rating",
    options=["Kids", "Family", "Teen", "Adult", "Unrated"],
    default=["Kids", "Family", "Teen", "Adult", "Unrated"]
)

# Apply filters
filtered = df[
    (df["type"].isin(content_type)) &
    (df["release_year"].between(*year_range)) &
    (df["rating_bucket"].isin(rating_buckets))
]

# ─────────────────────────────────────────
# KPI CARDS
# ─────────────────────────────────────────
st.subheader("📊 Dataset Overview")
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Total Titles",       f"{len(filtered):,}")
k2.metric("Movies",             f"{(filtered['type']=='Movie').sum():,}")
k3.metric("TV Shows",           f"{(filtered['type']=='TV Show').sum():,}")
k4.metric("Countries",          f"{filtered['primary_country'].nunique():,}")
k5.metric("Avg Movie Duration",
          f"{filtered['duration_minutes'].mean():.0f} min"
          if not filtered["duration_minutes"].isna().all() else "N/A")
st.markdown("---")

# ─────────────────────────────────────────
# ROW 1: Content type split | Rating buckets
# ─────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("Movies vs TV Shows")
    type_counts = filtered["type"].value_counts()
    fig, ax = plt.subplots(figsize=(5, 3.5))
    ax.pie(type_counts, labels=type_counts.index, autopct="%1.1f%%",
           colors=["#E50914", "#221F1F"], startangle=90,
           textprops={"color": "white"})
    fig.patch.set_facecolor("#141414")
    st.pyplot(fig)
    plt.close()

with col2:
    st.subheader("Content by Audience Rating Bucket")
    rb = filtered["rating_bucket"].value_counts()
    fig, ax = plt.subplots(figsize=(5, 3.5))
    rb.plot(kind="barh", ax=ax, color=sns.color_palette("Reds_r", len(rb)))
    ax.set_xlabel("Number of Titles")
    ax.set_facecolor("#1a1a1a"); fig.patch.set_facecolor("#141414")
    ax.tick_params(colors="white"); ax.xaxis.label.set_color("white")
    for sp in ax.spines.values(): sp.set_visible(False)
    st.pyplot(fig); plt.close()

# ─────────────────────────────────────────
# ROW 2: Content growth | Monthly additions
# ─────────────────────────────────────────
col3, col4 = st.columns(2)

with col3:
    st.subheader("Titles Added to Netflix Over Time")
    yearly = filtered.dropna(subset=["year_added"])
    yearly_counts = yearly.groupby(["year_added", "type"]).size().unstack(fill_value=0)
    fig, ax = plt.subplots(figsize=(6, 3.5))
    yearly_counts.plot(ax=ax, color=["#E50914", "#B81D24"], linewidth=2)
    ax.set_xlabel("Year Added"); ax.set_ylabel("Titles Added")
    ax.set_facecolor("#1a1a1a"); fig.patch.set_facecolor("#141414")
    ax.tick_params(colors="white")
    ax.xaxis.label.set_color("white"); ax.yaxis.label.set_color("white")
    ax.legend(facecolor="#333", labelcolor="white")
    for sp in ax.spines.values(): sp.set_visible(False)
    st.pyplot(fig); plt.close()

with col4:
    st.subheader("Which Month Does Netflix Add Most Content?")
    month_order = ["Jan","Feb","Mar","Apr","May","Jun",
                   "Jul","Aug","Sep","Oct","Nov","Dec"]
    monthly = filtered.dropna(subset=["month_name"])
    monthly_counts = monthly["month_name"].value_counts().reindex(month_order, fill_value=0)
    fig, ax = plt.subplots(figsize=(6, 3.5))
    ax.bar(monthly_counts.index, monthly_counts.values, color="#E50914")
    ax.set_xlabel("Month"); ax.set_ylabel("Titles Added")
    ax.set_facecolor("#1a1a1a"); fig.patch.set_facecolor("#141414")
    ax.tick_params(colors="white")
    ax.xaxis.label.set_color("white"); ax.yaxis.label.set_color("white")
    for sp in ax.spines.values(): sp.set_visible(False)
    st.pyplot(fig); plt.close()

# ─────────────────────────────────────────
# ROW 3: Top countries | Top genres
# ─────────────────────────────────────────
col5, col6 = st.columns(2)

with col5:
    st.subheader(f"Top {top_n_countries} Content-Producing Countries")
    country_counts = (
        filtered[filtered["primary_country"] != "Unknown"]
        ["primary_country"].value_counts().head(top_n_countries)
    )
    fig, ax = plt.subplots(figsize=(5, 4))
    country_counts.plot(kind="barh", ax=ax,
                        color=sns.color_palette("Reds_r", len(country_counts)))
    ax.set_xlabel("Number of Titles"); ax.invert_yaxis()
    ax.set_facecolor("#1a1a1a"); fig.patch.set_facecolor("#141414")
    ax.tick_params(colors="white"); ax.xaxis.label.set_color("white")
    for sp in ax.spines.values(): sp.set_visible(False)
    st.pyplot(fig); plt.close()

with col6:
    st.subheader("Top 10 Genres on Netflix")
    genres    = explode_genres(filtered)
    top_genres = genres.value_counts().head(10)
    fig, ax = plt.subplots(figsize=(5, 4))
    top_genres.plot(kind="barh", ax=ax,
                    color=sns.color_palette("Reds_r", len(top_genres)))
    ax.set_xlabel("Count"); ax.invert_yaxis()
    ax.set_facecolor("#1a1a1a"); fig.patch.set_facecolor("#141414")
    ax.tick_params(colors="white"); ax.xaxis.label.set_color("white")
    for sp in ax.spines.values(): sp.set_visible(False)
    st.pyplot(fig); plt.close()

# ─────────────────────────────────────────
# ROW 4: Decade breakdown | Movie duration
# ─────────────────────────────────────────
col7, col8 = st.columns(2)

with col7:
    st.subheader("Content by Decade of Release")
    decade_counts = filtered.groupby(["decade","type"]).size().unstack(fill_value=0)
    fig, ax = plt.subplots(figsize=(6, 3.5))
    decade_counts.plot(kind="bar", ax=ax, color=["#E50914","#831010"], width=0.7)
    ax.set_xlabel("Decade"); ax.set_ylabel("Number of Titles")
    ax.set_facecolor("#1a1a1a"); fig.patch.set_facecolor("#141414")
    ax.tick_params(colors="white", axis="both")
    ax.xaxis.label.set_color("white"); ax.yaxis.label.set_color("white")
    ax.legend(facecolor="#333", labelcolor="white")
    plt.xticks(rotation=45)
    for sp in ax.spines.values(): sp.set_visible(False)
    st.pyplot(fig); plt.close()

with col8:
    st.subheader("Movie Duration Distribution")
    movie_durations = filtered[filtered["type"] == "Movie"]["duration_minutes"].dropna()
    if len(movie_durations) > 0:
        fig, ax = plt.subplots(figsize=(6, 3.5))
        ax.hist(movie_durations, bins=30, color="#E50914", edgecolor="#141414")
        ax.axvline(movie_durations.mean(), color="white", linestyle="--",
                   linewidth=1.5, label=f"Mean: {movie_durations.mean():.0f} min")
        ax.axvline(movie_durations.median(), color="#aaa", linestyle=":",
                   linewidth=1.5, label=f"Median: {movie_durations.median():.0f} min")
        ax.set_xlabel("Duration (minutes)"); ax.set_ylabel("Number of Movies")
        ax.set_facecolor("#1a1a1a"); fig.patch.set_facecolor("#141414")
        ax.tick_params(colors="white")
        ax.xaxis.label.set_color("white"); ax.yaxis.label.set_color("white")
        ax.legend(facecolor="#333", labelcolor="white")
        for sp in ax.spines.values(): sp.set_visible(False)
        st.pyplot(fig); plt.close()

# ─────────────────────────────────────────
# RAW DATA TABLE (collapsible)
# ─────────────────────────────────────────
st.markdown("---")
with st.expander("🗂 View Filtered Dataset"):
    display_cols = [
        "title", "type", "primary_country", "release_year",
        "decade", "rating", "rating_bucket", "duration_minutes",
        "num_seasons", "listed_in", "date_added"
    ]
    st.dataframe(filtered[display_cols].reset_index(drop=True), use_container_width=True)
    st.caption(f"Showing {len(filtered):,} titles after applying filters.")

st.success("✅ Dashboard loaded successfully.")
