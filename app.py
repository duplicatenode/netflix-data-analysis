import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page title
st.title("Netflix Data Analysis Dashboard")

# Load dataset
df = pd.read_csv("netflix_titles.csv")

st.write("Dataset Preview")
st.dataframe(df.head())

# Clean data
df = df.dropna(subset=['country','rating'])

# -----------------------------
# Movies vs TV Shows
# -----------------------------

st.subheader("Movies vs TV Shows")

fig1, ax1 = plt.subplots()
sns.countplot(x='type', data=df, ax=ax1)
ax1.set_title("Movies vs TV Shows on Netflix")

st.pyplot(fig1)

# -----------------------------
# Top Countries
# -----------------------------

st.subheader("Top Countries Producing Netflix Content")

top_countries = df['country'].value_counts().head(10)

fig2, ax2 = plt.subplots()
top_countries.plot(kind='bar', ax=ax2)

ax2.set_title("Top Countries Producing Netflix Content")
ax2.set_xlabel("Country")
ax2.set_ylabel("Number of Titles")

st.pyplot(fig2)

# -----------------------------
# Content Growth Over Years
# -----------------------------

st.subheader("Content Growth Over Years")

content_year = df['release_year'].value_counts().sort_index()

fig3, ax3 = plt.subplots()
content_year.plot(ax=ax3)

ax3.set_title("Netflix Content Growth Over Years")
ax3.set_xlabel("Year")
ax3.set_ylabel("Number of Titles")

st.pyplot(fig3)

# -----------------------------
# Top Genres
# -----------------------------

st.subheader("Top Genres on Netflix")

genres = df['listed_in'].str.split(',', expand=True).stack()

top_genres = genres.value_counts().head(10)

fig4, ax4 = plt.subplots()
top_genres.plot(kind='bar', ax=ax4)

ax4.set_title("Top Genres on Netflix")
ax4.set_xlabel("Genre")
ax4.set_ylabel("Count")

st.pyplot(fig4)

st.success("Dashboard Created Successfully")