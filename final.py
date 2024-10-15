# Install necessary libraries
!pip install geocoder folium

# Import required libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geocoder
import folium
from folium import plugins

# Load the COVID-19 Global and India Data
global_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
india_url = 'https://api.covid19india.org/csv/latest/state_wise.csv'

global_df = pd.read_csv(global_url)
india_df = pd.read_csv(india_url).iloc[1:36, :]  # Limit to Indian states

# Get latitudes and longitudes for Indian states
india_df['Latitude'] = india_df['State'].apply(lambda x: geocoder.osm(x).lat)
india_df['Longitude'] = india_df['State'].apply(lambda x: geocoder.osm(x).lng)

# Function to create a line plot for global or country-specific data
def plot_covid_cases(country=None):
    if country:
        country_data = global_df[global_df['Country/Region'] == country].iloc[:, 4:].sum()
    else:
        country_data = global_df.iloc[:, 4:].sum()

    country_data.index = pd.to_datetime(country_data.index)
    plt.figure(figsize=(10, 6))
    plt.plot(country_data.index, country_data, label=country or 'Global')
    plt.title(f"COVID-19 Cases in {country or 'Global'}")
    plt.xlabel("Date")
    plt.ylabel("Total Cases")
    plt.xticks(rotation=45)
    plt.legend()
    plt.show()

# Function to create a folium map for India with circles representing cases
def map_covid_india():
    india_map = folium.Map(location=[22.3511148, 78.6677428], zoom_start=5)

    for i in india_df.index:
        folium.Circle(
            location=[india_df.loc[i, 'Latitude'], india_df.loc[i, 'Longitude']],
            radius=int(india_df.loc[i, 'Confirmed']) / 25,
            popup=f"{india_df.loc[i, 'State']} - {india_df.loc[i, 'Confirmed']} cases",
            color="blue", fill=True
        ).add_to(india_map)

    return india_map

# Function to create a bar plot for the top 10 countries with most cases
def plot_top_countries():
    total_cases = global_df.groupby('Country/Region').sum().iloc[:, -1].sort_values(ascending=False)
    top_countries = total_cases.head(10)

    plt.figure(figsize=(10, 6))
    sns.barplot(x=top_countries.values, y=top_countries.index, palette="Blues_d")
    plt.title("Top 10 Countries by COVID-19 Cases")
    plt.xlabel("Total Cases")
    plt.show()

# Example usage:
# 1. Line plot for global cases
plot_covid_cases()

# 2. Line plot for specific country (e.g., India)
plot_covid_cases('India')

# 3. Folium map for India
india_map = map_covid_india()
india_map.save("india_covid_map.html")  # Save map to an HTML file

# 4. Bar plot for top 10 countries
plot_top_countries()
