from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import argparse
from argparse import RawTextHelpFormatter
import sys
import numpy as np
import pandas as pd

def read_polygon(polyfile) -> list:
    """
    Returns polygon with country border
    """

    coords = np.genfromtxt(polyfile)
    Poly=[]
    for lon,lat in coords:
        Poly.append((lon,lat))
    polygon = Polygon(Poly)
    return polygon

def check_coords(lon,lat,polygon) -> bool:
    point = Point(lon,lat)
    if polygon.contains(point):
        return True
    else:
        return False    

def read_coords_list(filepath)  -> pd.DataFrame:
    df = pd.read_csv(filepath,sep=" ",header=None)
    df.columns = ["lat","lon","station","qc"]
    df.dtypes
    convert_dict = {'lat': float,'lon': float,"station":int,"qc":int}
    df = df.astype(convert_dict)
    return df[["lat","lon","station"]]

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='''
             Example usage: ./check_point.py -coords 8,56 (lon,lat) -poly ./dk_country_border.txt''', formatter_class=RawTextHelpFormatter)

    parser.add_argument('-coords', metavar='lon and lat of station, separated by comma',
            help ="lat and lon of station",
           type=str,
           default=None,
           required=False)

    parser.add_argument('-poly', metavar="File with country border",
            help ="File with country border",
           type=str,
           default="dk_country_border.txt",
           required=False)

    parser.add_argument('-stations', metavar="File with coords list",
            help ="File that contains the list of stations with coordinates",
           type=str,
           default=None,
           required=False)

    args = parser.parse_args()
    polygon = read_polygon(args.poly)

    if args.stations is not None:
        coords = read_coords_list(args.stations)
        save_list=[]
        lats=[]
        lons=[]
        for k,lat in enumerate(coords["lat"]):
            lon = coords["lon"].values[k]
            station = coords["station"].values[k]
            if check_coords(lon,lat,polygon):
                save_list.append(str(station))
                lats.append(lat)
                lons.append(lon)
        with open("stations_inside_dk.txt","w") as f:
            f.write(",".join(save_list))        
        df_save = pd.DataFrame({"lat":lats,"lon":lons,"station":save_list})    
        import sqlite3
        conn = sqlite3.connect("stations_dk.sqlite")
        df_save.to_sql(name="stations_dk",con=conn)
        conn.close()
    else:
        print("Please provide file with the stations")
        sys.exit(1)
