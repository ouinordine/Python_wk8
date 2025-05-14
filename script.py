import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime  # Import datetime
import ipywidgets as widgets #new
from IPython.display import display #new

# 1️⃣ Data Collection
# Goal: Obtain a reliable COVID-19 dataset.
# ✅ Data Sources:
#   - Our World in Data COVID-19 Dataset (CSV & API)
#   - Johns Hopkins University GitHub Repository
# 👉 Recommended for beginners: Use the cleaned CSV from Our World in Data (easy to load with pandas).
# ✅ Action:
#   - Download owid-covid-data.csv from the above link.
#   - Save in your working folder.
#
#   For demonstration, I'll use a direct link.
data_url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"

try:
    df = pd.read_csv(data_url)
    print("Data successfully loaded from URL.")
except Exception as e:
    print(f"Error loading data: {e}")
    print("Please download the CSV file and update the file path.")
    exit()



# 2️⃣ Data Loading & Exploration
# Goal: Load the dataset and explore its structure.
# ✅ Tasks:
#   - Load data using pandas.read_csv().
#   - Check columns: df.columns.
#   - Preview rows: df.head().
#   - Identify missing values: df.isnull().sum().
# ✅ Tools:
#   - pandas
# 📌 Key columns:
#   date, location, total_cases, total_deaths, new_cases, new_deaths, total_vaccinations, etc.

print("\n--- 2. Data Loading & Exploration ---")
print("Columns:")
print(df.columns)
print("\nFirst 5 rows:")
print(df.head())
print("\nMissing values:")
print(df.isnull().sum())



# 3️⃣ Data Cleaning
# Goal: Prepare data for analysis.
# ✅ Tasks:
#   - Filter countries of interest (e.g., Kenya, USA, India).
#   - Drop rows with missing dates/critical values.
#   - Convert date column to datetime: pd.to_datetime().
#   - Handle missing numeric values with fillna() or interpolate().
# ✅ Tools:
#   - pandas

print("\n--- 3. Data Cleaning ---")
# Get all unique countries from the dataset
all_countries = df['location'].unique()

# Create widgets for user input
country_dropdown = widgets.Dropdown(options=all_countries, description='Select Country:')
date_start_input = widgets.DatePicker(description='Start Date:')
date_end_input = widgets.DatePicker(description='End Date:')

# Display the widgets
display(country_dropdown)
display(date_start_input)
display(date_end_input)


def filter_and_analyze(country, start_date, end_date):
    """
    Filters the data based on user-selected country and date range, and performs the analysis.

    Args:
        country (str): The country to filter for.
        start_date (datetime.date): The start date for the analysis.
        end_date (datetime.date): The end date for the analysis.
    """
    print(f"\n--- Analysis for {country} from {start_date} to {end_date} ---")
    df_filtered = df[df['location'] == country].copy()  # Make a copy

    # Convert to datetime for comparison
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    df_filtered = df_filtered[(df_filtered['date'] >= start_date) & (df_filtered['date'] <= end_date)]

    if df_filtered.empty:
        print("No data available for the selected country and date range.")
        return

    # Drop rows where 'date' or 'total_cases' is missing
    df_filtered.dropna(subset=['date', 'total_cases'], inplace=True)

    df_filtered['date'] = pd.to_datetime(df_filtered['date'])

    # Handle missing numeric values - interpolate for some, fill with 0 for others
    numeric_cols_to_interpolate = ['total_cases', 'total_deaths', 'new_cases', 'new_deaths', 'total_vaccinations']
    for col in numeric_cols_to_interpolate:
        df_filtered[col] = df_filtered[col].interpolate()

    numeric_cols_to_fill_zero = ['new_cases_smoothed', 'new_deaths_smoothed', 'new_vaccinations']
    for col in numeric_cols_to_fill_zero:
        df_filtered[col] = df_filtered[col].fillna(0)



    # 4️⃣ Exploratory Data Analysis (EDA)
    # Goal: Generate descriptive statistics & explore trends.
    # ✅ Tasks:
    #   - Plot total cases over time for selected countries.
    #   - Plot total deaths over time.
    #   - Compare daily new cases between countries.
    #   - Calculate the death rate: total_deaths / total_cases.
    # ✅ Visualizations:
    #   - Line charts (cases & deaths over time).
    #   - Bar charts (top countries by total cases).
    #   - Heatmaps (optional for correlation analysis).
    # ✅ Tools:
    #   - matplotlib
    #   - seaborn

    print("\n--- 4. Exploratory Data Analysis (EDA) ---")
    plt.figure(figsize=(12, 6))
    plt.plot(df_filtered['date'], df_filtered['total_cases'], label=country)
    plt.title(f'Total COVID-19 Cases Over Time in {country}')
    plt.xlabel('Date')
    plt.ylabel('Total Cases')
    plt.legend()
    plt.grid(True)
    plt.show()

    plt.figure(figsize=(12, 6))
    plt.plot(df_filtered['date'], df_filtered['total_deaths'], label=country)
    plt.title(f'Total COVID-19 Deaths Over Time in {country}')
    plt.xlabel('Date')
    plt.ylabel('Total Deaths')
    plt.legend()
    plt.grid(True)
    plt.show()

    plt.figure(figsize=(12, 6))
    plt.plot(df_filtered['date'], df_filtered['new_cases'], label=country)
    plt.title(f'Daily New COVID-19 Cases in {country}')
    plt.xlabel('Date')
    plt.ylabel('New Cases')
    plt.legend()
    plt.grid(True)
    plt.show()

    df_filtered['death_rate'] = df_filtered['total_deaths'] / df_filtered['total_cases']
    print("\nDeath Rate Calculation (Example - First 5 rows):")
    print(df_filtered[['date', 'location', 'total_deaths', 'total_cases', 'death_rate']].head())



    # 5️⃣ Visualizing Vaccination Progress
    # Goal: Analyze vaccination rollouts.
    # ✅ Tasks:
    #   - Plot cumulative vaccinations over time for selected countries.
    #   - Compare % vaccinated population.
    # ✅ Charts:
    #   - Line charts.
    #   - Optional: Pie charts for vaccinated vs. unvaccinated.
    # ✅ Tools:
    #   - matplotlib
    #   - seaborn

    print("\n--- 5. Visualizing Vaccination Progress ---")
    plt.figure(figsize=(12, 6))
    plt.plot(df_filtered['date'], df_filtered['total_vaccinations'], label=country)
    plt.title(f'Cumulative COVID-19 Vaccinations Over Time in {country}')
    plt.xlabel('Date')
    plt.ylabel('Total Vaccinations')
    plt.legend()
    plt.grid(True)
    plt.show()



    # 6️⃣ Optional: Build a Choropleth Map
    # Goal: Visualize cases or vaccination rates by country on a world map.
    # ✅ Tools:
    #   - Plotly Express
    #   - Or geopandas (advanced)
    # ✅ Tasks:
    #   - Prepare a dataframe with iso_code, total_cases for the latest date.
    #   - Plot a choropleth showing case density or vaccination rates.

    print("\n--- 6. Optional: Choropleth Map (Requires Plotly) ---")
    try:
        import plotly.express as px
        # Get the latest data for each country
        latest_data = df.groupby('location').last().reset_index()
        latest_data = latest_data[['iso_code', 'total_cases', 'location']] #added location

        # Need iso_alpha for countries.
        choropleth_data = latest_data[latest_data['location'] == country] #changed to df_filtered

        if not choropleth_data['iso_code'].isnull().any():
            fig = px.choropleth(choropleth_data,
                                locations="iso_code",
                                color="total_cases",
                                hover_name="location",
                                title=f"Total COVID-19 Cases in {country} (Latest Data)",
                                color_continuous_scale=px.colors.sequential.Plasma)
            fig.show()
        else:
            print("Choropleth map cannot be displayed because of missing iso_code. Please ensure iso_code column is present and complete")

    except ImportError:
        print("Plotly is not installed. Skipping choropleth map.")
        print("To install plotly, run: pip install plotly")



    # 7️⃣ Insights & Reporting
    # Goal: Summarize findings.
    # ✅ Tasks:
    #   - Write 3-5 key insights from the data (e.g., "X country had the fastest vaccine rollout").
    #   - Highlight anomalies or interesting patterns.
    #   - Use markdown cells in Jupyter Notebook to write your narrative.
    # ✅ Deliverables:
    #   - A well-documented Jupyter Notebook combining:
    #     - Code
    #     - Visualizations
    #     - Narrative explanations
    #   - Optional export: Notebook → PDF or a PowerPoint with screenshots.

    print("\n--- 7. Insights & Reporting ---")
    print(f"\nKey Insights for {country}:")
    print(f"1.  Analysis of total cases and deaths over time reveals the progression of the pandemic in {country} from {start_date} to {end_date}.")
    print(f"2.  Comparing daily new cases highlights the peaks and valleys of infection rates, indicating the effectiveness of implemented measures in {country} during the selected period.")
    print(f"3.  The cumulative vaccination trends illustrate the pace of vaccine rollout in {country}.")
    print(f"4.  The relationship between total deaths and total cases (death rate) provides insight into the severity of the virus impact in {country} and how it changed over time.")
    print("\nAnomalies and Interesting Patterns:")
    print("Anomalies or interesting patterns, such as sudden spikes in cases or deaths, or rapid accelerations in vaccination rates, should be further investigated to understand the underlying reasons (e.g., new variants, policy changes).")



# Call the function when the user changes the input
def on_change(change):
    if all([country_dropdown.value, date_start_input.value, date_end_input.value]):
        filter_and_analyze(country_dropdown.value, date_start_input.value, date_end_input.value)

country_dropdown.observe(on_change, names='value')
date_start_input.observe(on_change, names='value')
date_end_input.observe(on_change, names='value')

# Initial call in case default values are set
if all([country_dropdown.value, date_start_input.value, date_end_input.value]):
    filter_and_analyze(country_dropdown.value, date_start_input.value, date_end_input.value)