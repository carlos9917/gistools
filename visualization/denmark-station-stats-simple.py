import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# File path and column names
DPATH = "~/sync_laptops/NOTES/RoadWeather/"
FILE = "vejvejr_update_202407.csv"
cols = ["SID", "c2", "c3", "SID_again", "name", "lon", "lat", "creation_date"] + [f"c{i+8}" for i in range(15)]

# Read the CSV file
all_stations = pd.read_csv(os.path.join(DPATH, FILE), encoding='cp865', header=None, names=cols)

# Convert creation_date to datetime
all_stations['creation_date'] = pd.to_datetime(all_stations['creation_date'].astype(str), format='%Y%m%d%H%M')

# Define regions based on latitude and longitude
def assign_region(row):
    if row['lat'] > 56:
        return 'North' if row['lon'] < 10 else 'East'
    else:
        return 'West' if row['lon'] < 10 else 'South'

all_stations['region'] = all_stations.apply(assign_region, axis=1)

# Group by year and region, count new stations
stations_by_year_region = all_stations.groupby([all_stations['creation_date'].dt.year, 'region']).size().unstack(fill_value=0)

# Calculate cumulative sum
cumulative_stations = stations_by_year_region.cumsum()

# Plot 1: Bar plot of new stations by year and region
plt.figure(figsize=(12, 6))
stations_by_year_region.plot(kind='bar', stacked=True)
plt.title('New Weather Stations in Denmark by Region')
plt.xlabel('Year')
plt.ylabel('Number of New Stations')
plt.legend(title='Region')
plt.tight_layout()
plt.savefig('new_stations_by_year_region.png')
plt.close()

# Plot 2: Line plot of cumulative stations by region
plt.figure(figsize=(12, 6))
cumulative_stations.plot(kind='line', marker='o')
plt.title('Cumulative Weather Stations in Denmark by Region')
plt.xlabel('Year')
plt.ylabel('Total Number of Stations')
plt.legend(title='Region')
plt.tight_layout()
plt.savefig('cumulative_stations_by_region.png')
plt.close()

# Plot 3: Heatmap of station density by region and decade
stations_by_decade_region = all_stations.groupby([pd.cut(all_stations['creation_date'].dt.year, bins=range(1980, 2031, 10)), 'region']).size().unstack(fill_value=0)
stations_by_decade_region.index = stations_by_decade_region.index.astype(str)

plt.figure(figsize=(10, 8))
sns.heatmap(stations_by_decade_region, annot=True, fmt='d', cmap='YlOrRd')
plt.title('Weather Station Density by Region and Decade')
plt.xlabel('Region')
plt.ylabel('Decade')
plt.tight_layout()
plt.savefig('station_density_heatmap.png')
plt.close()

print("Analysis complete. Check the generated PNG files for visualizations.")

# Print summary statistics
print("\nSummary of stations by region:")
print(all_stations['region'].value_counts())

print("\nTotal stations by the end of each decade:")
for decade in range(1980, 2021, 10):
    count = all_stations[all_stations['creation_date'].dt.year < decade + 10]['SID'].nunique()
    print(f"By {decade + 9}: {count}")
