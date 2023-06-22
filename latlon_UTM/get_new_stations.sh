#!/usr/bin/env bash
# get updated list of stations. Since there are so many now,
# I am naming them with ID+sensor1, giving a 6 digits station (the api call also provides s2 and s3). The first 4 is the standard station number
eval "$(/data/users/cap/miniconda3/bin/conda shell.bash hook)"
conda activate py38
./get_new_stations.py
#rm out
#rm out2
