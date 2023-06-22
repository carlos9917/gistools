#!/usr/bin/env bash
# Examples to run the processing
PY=/data/users/cap/miniconda3/envs/py38/bin/python

eval "$(/data/users/cap/miniconda3/bin/conda shell.bash hook)"
conda activate py38
i=137
#for ST in $(awk -v count=$i -F "|" 'NR%10==0 {print $3","$1","$2}' ../latlon_UTM/vejvejr_stations_utm.csv > tmp_list_${i}.csv); do
CSV=vejvejr_stations_utm.csv
#split files
#split -d -a 4 -l 10 $CSV vv --additional-suffix ".csv"
for F in vv*.csv; do
echo "Doing file $i: $F"
#python ./get_height.py -st $ST -out nh_$i.csv
python ./get_height.py -sl $F -out nh_$i.csv
let i++
done

#python ./get_height.py -sl $1 -out vejvejr_all_heights.csv  #station_data_test_utm.csv 
#$PY ./get_height.py -sl station_data_all_utm.csv > out_cron
#$PY ./get_height.py -sl missing_stations_utm.csv
##$PY ./get_height.py -sl ../../shadow_calcs/local_processing/station_noshadow_20211220_utm.csv

#$PY ./get_height.py -sl ../../shadow_calcs/local_processing/station_noshadow_20220208_utm.csv -out stations_height.csv
#$PY ./get_height.py -st 3011,519379.289172,6123006.457084 -out test.csv


#i=0
#for SHADOW in `ls -1 ../../data_shadows/shadows_new_stations/coord_lists/*_utm.csv`;do
#let i++
#$PY ./get_height.py -sl $SHADOW -out new_heights_$i.csv
#done
