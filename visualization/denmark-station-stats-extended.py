import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import seaborn as sns
import geopandas as gpd
from osgeo import gdal

gdal.SetConfigOption('SHAPE_RESTORE_SHX', 'YES')

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
        return 'NorthWest' if row['lon'] < 10 else 'NorthEast'
    else:
        return 'SouthWest' if row['lon'] < 10 else 'SouthEast'


# this one plots a map
# Define color scheme
color_scheme = {'NorthWest': 'tab:blue', 'SouthEast': 'tab:orange', 'NorthEast': 'tab:green', 'SouthWest': 'tab:red'}


def get_denmark_boundary(shp_file="./shapefiles/ne_110m_admin_0_countries.shp"):
    world = gpd.read_file(shp_file)
    denmark = world[world['NAME'] == 'Denmark']
    return denmark

def get_dk_high_res(shp_file="./shapefiles/dk_1km.shp"):
    from pyproj import CRS
    
    # Load the shapefile
    #shapefile_path = 'path/to/your/shapefile.shp'
    gdf = gpd.read_file(shp_file)
    
    # Check the current coordinate reference system (CRS)
    print(gdf.crs)
    
    # Define the UTM CRS (you need to know the UTM zone, for Denmark it's usually zone 32N or 33N)
    utm_crs = CRS("EPSG:32632")  # or "EPSG:32633" for UTM zone 33N
    
    # Define the WGS 84 CRS
    wgs84_crs = CRS("EPSG:4326")
    
    # Ensure the GeoDataFrame is in the UTM CRS
    gdf = gdf.set_crs(utm_crs, allow_override=True)
    
    # Convert the GeoDataFrame to WGS 84 (lat/lon)
    gdf_wgs84 = gdf.to_crs(wgs84_crs)
    
    # Save the new shapefile
    #output_path = 'path/to/your/output_shapefile.shp'
    #gdf_wgs84.to_file(output_path)
    return gdf_wgs84["geometry"]



# Create a simple map of Denmark showing regions
def create_denmark_map(all_stations, color_scheme):
    # Create a world map and filter for Denmark
    #old style. Doesnt work
    #world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

    #for very coarse res
    #denmark = get_denmark_boundary()
    #for high res (not working(
    #denmark = get_dk_high_res()

    denmark = gpd.read_file("./data/DK/DNK_adm0.shp")

    # Create plot
    fig, ax = plt.subplots(figsize=(10, 10))

    # Plot Denmark
    denmark.plot(ax=ax, color='lightgrey', edgecolor='black')

    # Define region boundaries
    lat_divide = 56
    lon_divide = 10

    # Plot regions
    ax.fill_between([denmark.total_bounds[0], lon_divide], [lat_divide, lat_divide], 
                    [denmark.total_bounds[3], denmark.total_bounds[3]], color=color_scheme['NorthWest'], alpha=0.5)
    ax.fill_between([lon_divide, denmark.total_bounds[2]], [lat_divide, lat_divide], 
                    [denmark.total_bounds[3], denmark.total_bounds[3]], color=color_scheme['NorthEast'], alpha=0.5)
    ax.fill_between([denmark.total_bounds[0], lon_divide], [denmark.total_bounds[1], denmark.total_bounds[1]], 
                    [lat_divide, lat_divide], color=color_scheme['SouthWest'], alpha=0.5)
    ax.fill_between([lon_divide, denmark.total_bounds[2]], [denmark.total_bounds[1], denmark.total_bounds[1]], 
                    [lat_divide, lat_divide], color=color_scheme['SouthEast'], alpha=0.5)

    # Add region labels
    ax.text(8.5, 57, 'NorthWest', fontsize=12, ha='center', va='center')
    ax.text(12, 57, 'NorthEast', fontsize=12, ha='center', va='center')
    ax.text(8.5, 55, 'SouthWest', fontsize=12, ha='center', va='center')
    ax.text(12, 55, 'SouthEast', fontsize=12, ha='center', va='center')

    # Set title and remove axis labels
    ax.set_title('Regions of Denmark for Station Analysis', fontsize=16)
    ax.set_axis_off()

    # Save the figure
    plt.tight_layout()
    plt.savefig('denmark_regions_map.png')
    plt.close()

# Create the map
create_denmark_map(all_stations, color_scheme)


# ... [Rest of the analysis and printing code remains the same] ...







all_stations['region'] = all_stations.apply(assign_region, axis=1)

# Group by year and region, count new stations
stations_by_year_region = all_stations.groupby([all_stations['creation_date'].dt.year, 'region']).size().unstack(fill_value=0)

# Calculate cumulative sum
cumulative_stations = stations_by_year_region.cumsum()

# Plot 1: Bar plot of new stations by year
plt.figure(figsize=(15, 6))
stations_by_year_region.plot(kind='bar', stacked=True)
plt.title('New Weather Stations in Denmark by Year and Region')
plt.xlabel('Year')
plt.ylabel('Number of New Stations')
plt.legend(title='Region')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('new_stations_by_year.png')
plt.close()

# Plot 2: Bar plot of cumulative stations by year
plt.figure(figsize=(15, 6))
cumulative_stations.plot(kind='bar', stacked=True)
plt.title('Cumulative Weather Stations in Denmark by Year and Region')
plt.xlabel('Year')
plt.ylabel('Total Number of Stations')
plt.legend(title='Region')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('cumulative_stations_by_year.png')
plt.close()

# Plot 3: Bar plot of yearly increase in stations
yearly_increase = stations_by_year_region.sum(axis=1)
plt.figure(figsize=(15, 6))
yearly_increase.plot(kind='bar')
plt.title('Yearly Increase in Weather Stations in Denmark')
plt.xlabel('Year')
plt.ylabel('Number of New Stations')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('yearly_increase_stations.png')
plt.close()

# Plot 4: Bar plot of yearly increase by region
plt.figure(figsize=(15, 6))
stations_by_year_region.plot(kind='bar')
plt.title('Yearly Increase in Weather Stations by Region')
plt.xlabel('Year')
plt.ylabel('Number of New Stations')
plt.legend(title='Region')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('yearly_increase_by_region.png')
plt.close()

print("Analysis complete. Check the generated PNG files for visualizations, including the new denmark_regions_map.png.")

# Print summary statistics
print("\nSummary of stations by region:")
print(all_stations['region'].value_counts())

print("\nTotal stations by the end of each year:")
for year in range(all_stations['creation_date'].dt.year.min(), all_stations['creation_date'].dt.year.max() + 1):
    count = all_stations[all_stations['creation_date'].dt.year <= year]['SID'].nunique()
    print(f"By end of {year}: {count}")

print("\nYears with the highest increase in stations:")
top_years = yearly_increase.nlargest(5)
print(top_years)

print("\nRegion with the most stations:")
print(all_stations['region'].value_counts().idxmax())
