#!/usr/bin/env python
import subprocess
import pandas as pd

import requests
from requests.auth import HTTPBasicAuth

api_url = "http://vejvejr.dk/glatinfoservice/GlatInfoServlet?command=stationlist&formatter=glatmodel"
response = requests.get(api_url, auth = HTTPBasicAuth("vejvejr","settings"))
print(response)
#df = pd.read_csv(test, dtype= {'F4': str, 'F5': str})
output="out2"
cmd = f'wget -O out --user=vejvejr --password=settings "http://vejvejr.dk/glatinfoservice/GlatInfoServlet?command=stationlist&formatter=glatmodel"; cat out | iconv -f iso8859-1 -t utf-8 > {output}'
try:
    ret=subprocess.check_output(cmd,shell=True)
except subprocess.CalledProcessError as err:    
    print(err)
res_cols = [(i, int) for i in range(7,39)]
res_types=dict([(key, value) for key, value in res_cols])
dtypes={0:int,1:str,2:int,3:int,4:int,5:str,6:str}
header = ["ID","name","s1","s2","s3","lon","lat"]+["col"+str(i).zfill(2) for i in range(7,39)]
dtypes.update(res_types)
df = pd.read_csv(output,sep=",",header=None, dtype=dtypes)
df = df.astype({1:str})
df.columns=header
df["SID"]=[str(ID)+str(df["s1"].values[k]).zfill(2) for k,ID in enumerate(df["ID"])]
df["SID"]=df["SID"].astype(int)
#df = pd.read_csv(output,sep=",")
#df = pd.read_csv(test, dtype= {'F4': str, 'F5': str})
output="vejvejr_stations.csv"
#import csv
#df[["SID","name","lon","lat"]].to_csv(output,index=False,sep=",",quotechar='"',quoting=csv.QUOTE_NONNUMERIC,header=None)

#df["name"] = [f'"{i}"' for i in df["name"]]
#df["name"] = '"' + df["name"].astype(str) + '"'
df['name'].apply(lambda x: '"' +x+ '"')
df[["SID","name","lon","lat"]].to_csv(output,index=False,sep=",",header=None)

