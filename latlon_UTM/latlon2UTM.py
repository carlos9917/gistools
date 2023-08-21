#convert UTM to lat lon for the current maps over Denmark
# testing two methods here, seem to give same answer

def UTM2latlon(input_file:str,output_file:str) -> None:
    import pandas as pd
    df=pd.read_csv(input_file,header=None,sep=" ")
    from pyproj import Proj
    #myProj = Proj("+proj=utm +zone=UTM32N, +north +ellps=WGS84 +datum=WGS84 +units=m +no_defs")
    myProj = Proj('EPSG:25832')
    df.columns=["easting","norting","height"]
    lon, lat = myProj(df["easting"].values,df["norting"].values,  inverse=True)
    df_out=pd.DataFrame({"lon":lon,"lat":lat,"height":df["height"]})
    df_out.to_csv(output_file,header=None,sep=" ",index=False)

def UTM2latlon_gpd(input_file:str,output_file:str) -> None:
    df=pd.read_csv(input_file,header=None,sep=" ")
    from geopandas import GeoSeries
    from shapely.geometry import Point
    lons=[];lats=[]
    for posx,posy in zip(df["easting"],df["norting"]):
        lon, lat = GeoSeries([Point(posx, posy)], crs='EPSG:25832').to_crs('epsg:4258')[0].coords[0]
        lons.append(lon)
        lats.append(lat)
    
    df_out=pd.DataFrame({"lon":lons,"lat":lats,"height":df["height"]})
    df_out.to_csv(output_file,header=None,sep=" ",index=False)

