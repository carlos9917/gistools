from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import argparse
from argparse import RawTextHelpFormatter
import sys
import numpy as np

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

def check_coord(lon,lat,polygon):
    point = Point(lon,lat)
    if polygon.contains(point):
        return True
    else:
        return False



if __name__=="__main__":
    parser = argparse.ArgumentParser(description='''
             Example usage: ./check_point.py -coords 8,56 (lon,lat) -poly ./dk_country_border.txt''', formatter_class=RawTextHelpFormatter)

    parser.add_argument('-coords', metavar='lon and lat of station, separated by comma',
            help ="lat and lon of station",
           type=str,
           default=None,
           required=True)

    parser.add_argument('-poly', metavar="File with country border",
            help ="File with country border",
           type=str,
           default="dk_country_border.txt",
           required=False)

    args = parser.parse_args()
    polygon = read_polygon(args.poly)

    if "," in args.coords:
        lon,lat = args.coords.split(",")
    elif "," not in args.coords:
        print("Please provide lon and lat separated by comma")
        sys.exit(1)
    #print(args)
    if check_coord(float(lon),float(lat),polygon):
        print(f"{lon},{lat} coordinates ok")
    else:    
        print(f"{lon},{lat} outside the border defined by {args.poly}!")

