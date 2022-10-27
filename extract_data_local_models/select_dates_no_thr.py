"""
Read the data from the csv files I produced and get the time series
for each date
"""

import sqlite3
import pandas as pd
from datetime import datetime
from collections import OrderedDict
import os
import sys
model="nea40h11"

def read_db(dbase:str,stations:list,fcdate:int) -> pd.DataFrame:
    conn = sqlite3.connect(dbase)
    sel_list = ",".join(stations)
    find_station = f"SELECT * FROM FC WHERE SID IN ({sel_list}) AND fcdate = {fcdate};"
    df=pd.read_sql(find_station, conn)
    conn.close()
    return df

def process_data(db:pd.DataFrame,
                 var:str,
                 yyyymm:str,
                 hh:str,
                 out_path:str) -> None:
    """
    Save only the dtg,value and the station
    on separate files for each cycle and a given month
    """
    val_name = model+"_det"
    conts=OrderedDict()
    for label in ["date","fc_init","leadtime","station","fc_value"]:
        conts[label] = []
    for k,fcdate in enumerate(db.fcdate):
        str_date = datetime.strftime(datetime.fromtimestamp(fcdate),"%Y%m%d")
        ltime = str(db.leadtime.values[k]).zfill(2)
        dtg = str_date+ltime
        cur_st = db["SID"].values[k]
        print(f"Doing {cur_st} on {dtg}")
        conts["date"].append(str_date)
        conts["leadtime"].append(ltime)
        conts["fc_value"].append(db[val_name].values[k])
        conts["fc_init"].append(hh)
        conts["station"].append(cur_st)
    df_out=pd.DataFrame(conts)    
    #ofile=os.path.join(out_path,"_".join([var,yyyymm,hh])+".csv")
    ofile=os.path.join(out_path,"_".join([var,str_date,hh])+".csv")
    if os.path.isfile(ofile):
        print(f"File {ofile} already exists!")
        sys.exit(1)
    else:    
        df_out.to_csv(ofile,index=False)

def search_stations(df:pd.DataFrame,stations:list,out_path:str) -> None:
    """
    Read the sqlite dbase and select all the stations for all the variables
    """
    dbase_path="/data/projects/nckf/danra/verification/FCTABLE"
    pref="FCTABLE"
    var="S10m"
    all_vars = ["S10m","D10m","RH2m","Pmsl","T2m","Gmax"]
    for k,dtg in enumerate(df.dtg):
        dtg_str = str(dtg)
        year = dtg_str[0:4]
        month = dtg_str[4:6]
        hh = dtg_str[8:10] #.zfill(2)
        yyyymm = year+month
        ts = df.timestamp.values[k]
        print(f"CYCLE for {dtg_str} ----> {hh}")
        print("---------------------------------------------")
        for var in all_vars:
            dbase = os.path.join(dbase_path,model,year,month,"_".join([pref,var,yyyymm,hh])+".sqlite")
            if os.path.isfile(dbase):
               date = str(dtg)[0:8]
               #date_obj = datetime.strptime(date,"%Y%m%d")
               #ts = date_obj.timestamp()
               print(f"Reading {dbase} for {dtg} {ts}")
               db = read_db(dbase,stations,ts)
               process_data(db,var,yyyymm,hh,out_path)
            else:
                print(f"WARNING: {dbase} not available!")
        print("---------------------------------------------")


if __name__=="__main__":
    stations_df=pd.read_csv("stations_ulrik.csv")
    stations_ulrik = stations_df.id.to_list()
    stations_ulrik = [str(i) for i in stations_ulrik]
    search_path="/data/projects/nckf/danra/storms/ramboll/time_series/SELECTION"
    period="20181129"
    year ="2018"
    this_path = os.path.join(search_path,period)
    f = os.path.join(this_path,"selection.csv")
    print(f"Reading selection file {f}")
    if os.path.isfile(f):
        print(f"Opening {os.path.join(this_path,f)}")
        df = pd.read_csv(os.path.join(this_path,f))
        search_stations(df,stations_ulrik,this_path)
