#!/usr/bin/env bash
#This  one is to filter Danish characters
#cat $1 | iconv -f iso8859-1 -t utf-8  > $1_clean

#this example assumes station data in "road_strecht" format (station,name,lat,lon)
python calcUTM.py -ifile vejvejr_stations.csv
