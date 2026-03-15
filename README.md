# Netflix Data Analysis
## Live Demo:
https://netflix-data-analysis01.streamlit.app/

This project performs Exploratory Data Analysis (EDA) on the Netflix dataset to uncover trends in content distribution, release patterns, and genre popularity.
The project also includes a Python web application (app.py) that allows users to explore the dataset interactively.

## Project Overview

This project analyzes Netflix’s content catalog to answer questions such as:
How many Movies vs TV Shows are available?
Which years saw the most content releases?
What are the most common genres?
Which countries produce the most Netflix content?
The project combines data analysis and interactive visualization.

## Tech Stack:
Python
Pandas
NumPy
Jupyter Notebook
Matplotlib / Seaborn
Streamlit / Flask (via app.py)

## Project Structure
netflix-data-analysis

├── app.py                  # Web application for interactive analysis

├── netflix_analysis.ipynb  # Exploratory data analysis notebook

├── netflix_titles.csv      # Dataset

├── README.md               # Project documentation

## Key Analysis Performed
Data cleaning and preprocessing

Handling missing values

Distribution of Movies vs TV Shows

Content release trends over the years

Genre popularity analysis

Country-wise content distribution

## Running the Project
1️⃣ Clone the repository
git clone https://github.com/duplicatenode/netflix-data-analysis.git
2️⃣ Navigate to the project directory
cd netflix-data-analysis
3️⃣ Install dependencies
pip install pandas numpy matplotlib seaborn streamlit
4️⃣ Run the application

If using Streamlit:
streamlit run app.py

If using Flask:
python app.py

## Example Insights
Netflix contains significantly more movies than TV shows.
The number of titles increased rapidly after 2015.
Certain genres dominate the platform’s catalog.

## Future Improvements
Add interactive dashboards
Implement recommendation system
Deploy the application online
