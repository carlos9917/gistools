import numpy as np
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')


def get_circle(lat:float,
               lon:float,
               d:float) -> Polygon:
    """
    Using this example to get a few points
    and define a circle around the lat lon 
    https://stackoverflow.com/questions/7222382/get-lat-long-given-current-point-distance-and-bearing
    """
    import geopy
    from geopy.distance import geodesic
    origin = geopy.Point(lat,lon) #according to docs, define using lat and lon
    polAround=[]
    for b in range(0,361,30):
        destination = geodesic(kilometers=d).destination(origin, b)
        lat2, lon2 = destination.latitude, destination.longitude
        polAround.append((lon2,lat2))
    polygon = Polygon(polAround)   
    return polygon

def check_inside(stations:pd.DataFrame,pol:Polygon) -> list:
    """
    check if any of the stations is inside the list
    """
    import geopy
    inside = []
    for i,st in enumerate(stations.id):
        lon = stations.lon.values[i]
        lat = stations.lat.values[i]
        point = Point(lon,lat)
        #print(f"Checking station {st}")
        if pol.contains(point):
            print(f"{st} with {lon} {lat} is inside the polygon")
            inside.append(st)
    return inside
        

def check_around_all(stations_ulrik,stations_dk,radius_in_km) -> dict:
    all_around = dict()
    for k,st in enumerate(stations_ulrik.name):
        print(f"Going throug station {st}")
        lat = stations_ulrik.lat.values[k]
        lon = stations_ulrik.lon.values[k]
        pol=get_circle(lat,lon,radius_in_km)
        print(f"Polygon around {lon,lat}: {pol}")
        inside=check_inside(stations_dk,pol)
        #plot to compare
        #x,y = pol.exterior.xy
        #plt.plot(x,y)
        #plt.plot(lon,lat,marker="o",markersize=10)
        #plt.show()
        this_id = stations_ulrik.id.values[k]
        all_around[str(this_id)] = inside
    return all_around

def check_around(this_station:dict,
                 stations:pd.DataFrame,
                 radius:float) -> list:
    #all_around = dict()
    lat = this_station["lat"]
    lon = this_station["lon"]
    pol = get_circle(lat,lon,radius)
    inside=check_inside(stations,pol)
    this_id = this_station["id"]
    if this_id in inside:
        inside.remove(this_id)
    #all_around[this_id] = inside
    return inside
        
        

if __name__=="__main__":
    stations_ulrik=pd.read_csv("stations_ulrik.csv")
    stations_dk=pd.read_csv("stations_dk.csv")

    #check all around
    #all_around = check_around(stations_ulrik,stations_dk)

    #check the stations surrounding 6181
    sel_6181=stations_ulrik[stations_ulrik["id"] == 6181]
    this_station = dict()
    this_station ["id"] = sel_6181["id"].values[0]
    this_station ["lat"] = sel_6181["lat"].values[0]
    this_station ["lon"] = sel_6181["lon"].values[0]
    all_around_6181 = check_around(this_station,stations_dk,50)
    all_around_6181 = list(set(all_around_6181))
    selected_stations = stations_dk[stations_dk['id'].isin(all_around_6181)]
    selected_stations.drop_duplicates(subset=["id"],inplace=True)
    selected_stations.to_csv("stations_30km_around_6181.dat",sep=" ",index=False)
    #with open("stations_30km_around_6181.dat","w") as f:
    #    for l in all_around_6181:
    #        f.write(l+"\n")
