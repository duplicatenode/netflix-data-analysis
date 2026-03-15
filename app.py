import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page config
st.set_page_config(page_title="Netflix Data Analysis", layout="wide")

st.title("📺 Netflix Data Analysis Dashboard")

# Load dataset
df = pd.read_csv("netflix_titles.csv")

# Sidebar filters
st.sidebar.header("Filters")

type_filter = st.sidebar.multiselect(
    "Select Type",
    options=df["type"].unique(),
    default=df["type"].unique()
)

country_filter = st.sidebar.multiselect(
    "Select Country",
    options=df["country"].dropna().unique(),
)

# Apply filters
filtered_df = df[df["type"].isin(type_filter)]

if country_filter:
    filtered_df = filtered_df[filtered_df["country"].isin(country_filter)]

# Dataset overview
st.subheader("Dataset Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Total Titles", len(filtered_df))
col2.metric("Movies", len(filtered_df[filtered_df["type"] == "Movie"]))
col3.metric("TV Shows", len(filtered_df[filtered_df["type"] == "TV Show"]))

# Content Type Chart
st.subheader("Content Type Distribution")

fig1, ax1 = plt.subplots()
sns.countplot(data=filtered_df, x="type", palette="Set2")
st.pyplot(fig1)

# Release Year Analysis
st.subheader("Content Released Over Time")

release_counts = filtered_df["release_year"].value_counts().sort_index()

fig2, ax2 = plt.subplots(figsize=(10,4))
release_counts.plot(ax=ax2)
ax2.set_xlabel("Year")
ax2.set_ylabel("Number of Titles")
st.pyplot(fig2)

# Top Countries
st.subheader("Top Content Producing Countries")

top_countries = (
    filtered_df["country"]
    .dropna()
    .value_counts()
    .head(10)
)

fig3, ax3 = plt.subplots()
top_countries.plot(kind="bar")
st.pyplot(fig3)

# Show dataset
st.subheader("Raw Dataset")

st.dataframe(filtered_df)
