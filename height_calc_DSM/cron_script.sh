#!/usr/bin/env bash

# quick script to process station list if there were any new stations
# generated that day
PY=/data/users/cap/miniconda3/envs/py38/bin/python
WRK=/data/users/cap/glatmodel/gistools/height_calc_DSM
TODAY=`date +'%Y%m%d'`
NOSHADOWSPATH=/data/users/cap/glatmodel/shadow_calcs/local_processing
NEWMSG=${NOSHADOWSPATH}/deliver_station_data_${TODAY}.txt
if [ -s $NEWMSG ]; then
	echo "New data generated. Calculating station heights"
	CSV=${NOSHADOWSPATH}/station_noshadow_${TODAY}_utm.csv
	OUT=noshadows_heights_${TODAY}.dat
	[ -f $CSV ] && $PY ./get_height.py -sl $CSV -out $OUT
        #Append the data to the all_heights.csv file
	echo "appending data to all_heights.csv"
	awk 'NR>1' $OUT >> ../../data_shadows/all_heights.csv
else
	echo "No new shadows data on $TODAY"
fi

