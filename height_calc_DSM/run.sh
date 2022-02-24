#!/usr/bin/env bash
PY=/data/users/cap/miniconda3/envs/py38/bin/python
#echo TEST > out_cron
#python ./get_height.py -sl station_data_test_utm.csv
#$PY ./get_height.py -sl station_data_all_utm.csv > out_cron
#$PY ./get_height.py -sl missing_stations_utm.csv
##$PY ./get_height.py -sl ../../shadow_calcs/local_processing/station_noshadow_20211220_utm.csv

$PY ./get_height.py -sl ../../shadow_calcs/local_processing/station_noshadow_20220208_utm.csv -out stations_height.csv
