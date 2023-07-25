#!/usr/bin/env python
# coding: utf-8

# plot the stations after new ones are added

import os
import geopandas as gpd
from collections import OrderedDict
from datetime import datetime
import calendar
import pandas as pd
import matplotlib.pyplot as plt
from osgeo import gdal
import gc
#import geodatasets
import contextily as cx

from shapely.geometry import shape

all_stations = gpd.read_file("all_vejvejr_stations_2023.shp")

nwz_pol = gpd.read_file("polygons/around_nw_zealand.geojson")
mju_pol = gpd.read_file("polygons/somewhere_midjutland.geojson")
fyn_pol = gpd.read_file("polygons/around_fyn.geojson")

gdal.SetConfigOption('SHAPE_RESTORE_SHX', 'YES')
dk_pol = gpd.read_file("~/data/my_repos/learning/GIS/data/DK/DNK_adm1.shp")

sel_fyn = OrderedDict()
stations=OrderedDict()

#for f in sorted(Path(".").glob("stations_added*shp")):
#    fname = str(f)
#    when = fname.split("_")[2].replace(".shp","")
#    st_read = gpd.read_file(f)
#    stations[when] = st_read
#    print(when)
#
#for yyyymm in stations.keys():
#    match = gpd.sjoin(stations[yyyymm],fyn_pol,op="within")
#    size = match.shape[0]
#    print(f"{yyyymm} has {size}")
#    sel_fyn[yyyymm] = match
    
#select math with all stations in the selected regions
stations_fyn = gpd.sjoin(all_stations,fyn_pol,predicate="within")
stations_mju = gpd.sjoin(all_stations,mju_pol,predicate="within")
stations_nwz = gpd.sjoin(all_stations,nwz_pol,predicate="within")

#chicago.plot(ax=ax, color='white', edgecolor='black')
#groceries.plot(ax=ax, marker='o', color='red', markersize=5)
#plt.show();
#set the date of creation
for st in [stations_fyn,stations_mju,stations_nwz]:
    st["datecreated"] = [datetime.strptime(str(d),"%Y%m%d%H%M") for d in st.creation_d]

#change here to plot other stations
process_region = stations_fyn
reg_pref = "fyn"
for year in ["2022","2023"]:
    for month in [1,2,3]:
        lday = calendar.monthrange(int(year), month)[1]
        beg_month = datetime(int(year),month,1)
        end_month = datetime(int(year),month,lday)
        for day in pd.date_range(beg_month,end_month,freq="1D"):
            str_date = datetime.strftime(day,"%Y%m%d")

            #sel_stations = stations_fyn[stations_fyn["datecreated"] > day]
            #to_plot = stations_fyn[~stations_fyn["datecreated"].isin(date_list)]

            #drop those stations that did not exist today
            drop_stations = process_region[process_region["datecreated"] > day]
            date_list_drop = drop_stations["datecreated"].to_list()
            #selects what is not in date_list_drop from selected stations
            to_plot = process_region[~process_region["datecreated"].isin(date_list_drop)] 
            n_drop = drop_stations.shape[0]
            n_left = to_plot.shape[0]
            #print(f"Dropping {n_drop} stations on {str_date}")
            #print(date_list_drop)
            #Make a plot only if there is a difference in stations 
            # or if it is the first day of the month
            if day == beg_month:
                print(f"Making a plot on {str_date}, because it is the first day of the month")
                n_change = n_left
                fig, ax = plt.subplots()
                ax.set_title(f"On {str_date} {n_left} stations in {reg_pref}")
                pol_plot = dk_pol.plot(ax=ax,color='white', edgecolor='black')
                cx.add_basemap(pol_plot,zoom=10,crs=fyn_pol.crs.to_string())
                to_plot.plot(ax=ax,marker="o",color="red")
                #cx.add_basemap(pol_plot,source=cx.providers.Stamen.TonerLite,zoom=20,crs=fyn_pol.crs.to_string())
                minx, miny, maxx, maxy = process_region.total_bounds
                ax.set_xlim(minx-0.25, maxx+0.25)
                ax.set_ylim(miny-0.25, maxy+0.25)
                fname="_".join(["stations",reg_pref,str_date])+".png"
                fig.savefig(fname)
                fig.clf()
                plt.close(fig)
                gc.collect()
                #just to print stations on the screen
                #print(to_plot["SID"].to_list())
            elif n_change != n_left:
                print(f"Making a plot on {str_date} because there was a change")
                n_change = n_left
                fig, ax = plt.subplots()
                ax.set_title(f"On {str_date} {n_left} stations in {reg_pref}")
                pol_plot=dk_pol.plot(ax=ax,color='white', edgecolor='black')
                cx.add_basemap(pol_plot,zoom=10,crs=fyn_pol.crs.to_string())
                to_plot.plot(ax=ax,marker="o",color="red")
                minx, miny, maxx, maxy = process_region.total_bounds
                ax.set_xlim(minx-0.25, maxx+0.25)
                ax.set_ylim(miny-0.25, maxy+0.25)
                fname="_".join(["stations",reg_pref,str_date])+".png"
                fig.savefig(fname)
                fig.clf()
                plt.close(fig)
                gc.collect()
                #just to print the stations on the screen
                #print(to_plot["SID"].to_list())
            #plt.show()

