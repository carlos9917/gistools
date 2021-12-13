
#https://gis.stackexchange.com/questions/228920/getting-elevation-at-particular-coordinate-lat-lon-programmatically-but-offli
import rasterio

coords = ((147.363,-36.419), (147.361,-36.430))
elevation = 'srtm_66_20.tif'

with rasterio.open(elevation) as src:
    vals = src.sample(coords)
    for val in vals:
        print(val[0]) #val is an array of values, 1 element 
                      #per band. src is a single band raster 
                      #so we only need val[0]
