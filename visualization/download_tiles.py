#download tiles for a given domain from elevation maps

import elevation
import os
from osgeo import gdal

# Define the bounding box for Denmark

#box: minlon,minlat,maxlon,maxlat
bbox = (7.0, 54.5, 13.0, 58.0)  # (min_lon, min_lat, max_lon, max_lat)


#bbox = (7.5, 54.5, 15.75, 58.0)  # (min_lon, min_lat, max_lon, max_lat)
#bbox = (7.0,54.5,17,58.0)

# Split the bounding box into smaller regions
def split_bbox(bbox, rows, cols):
    min_lon, min_lat, max_lon, max_lat = bbox
    lon_step = (max_lon - min_lon) / cols
    lat_step = (max_lat - min_lat) / rows
    
    bboxes = []
    for i in range(rows):
        for j in range(cols):
            bboxes.append((
                min_lon + j * lon_step,
                min_lat + i * lat_step,
                min_lon + (j + 1) * lon_step,
                min_lat + (i + 1) * lat_step
            ))
    return bboxes

# Example: 2 rows and 3 columns
sub_bboxes = split_bbox(bbox, 2, 3)

# Directory to save the individual DEM files
output_dir = "/home/cap/data/my_repos/gistools/visualization/denmark_dem_tiles"
os.makedirs(output_dir, exist_ok=True)

#this is the merged one (optional)
output_file = "denmark_dem_merged.tif"

# Download each sub-region
print("Doing first set")
tile_files = []
for idx, sub_bbox in enumerate(sub_bboxes):
    output_file = os.path.join(output_dir, f"tile_{idx}.tif")
    elevation.clip(bounds=sub_bbox, output=output_file)
    tile_files.append(output_file)
    print(f"Downloaded: {output_file}")
bbox = (13.01, 54.5, 17.0, 58.0)  # (min_lon, min_lat, max_lon, max_lat)
idx_last = idx+1 
print("Doing second set")
for idx, sub_bbox in enumerate(sub_bboxes):
    idx_new = idx_last + idx
    output_file = os.path.join(output_dir, f"tile_{idx_new}.tif")
    elevation.clip(bounds=sub_bbox, output=output_file)
    tile_files.append(output_file)
    print(f"Downloaded: {output_file}")
bbox = (13.01, 54.5, 17.0, 58.0)  # (min_lon, min_lat, max_lon, max_lat)

# Merge the tiles into a single file (optional)
#merged_output_file = output_file

#vrt_options = gdal.BuildVRTOptions(resampleAlg='cubic', addAlpha=True)
#vrt = gdal.BuildVRT("merged.vrt", tile_files, options=vrt_options)
#gdal.Translate(merged_output_file, vrt)
#vrt = None  # Close the VRT file

#print(f"Merged DEM file saved to: {merged_output_file}")

