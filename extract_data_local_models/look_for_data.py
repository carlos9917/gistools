"""
Look for all occurrences of strong (gale strength) wind in
the data
"""
import sqlite3
import pandas as pd
from datetime import datetime
from collections import OrderedDict
import os
import sys

GALE_WIND = 17 #in m/s
import stations_inside_circle as sic
also_data = OrderedDict()
for key in ["dtg","value","station"]:
    also_data[key]=[]

def get_timestamps(period:str) -> list:
    """
    Define timestamps to limit the data output
    """
    from datetime import timezone
    #periods = ["20181126-20181130","20181230-20190103", "20191213-20191216"]
    tstamps=[]
    #for p in periods:
    date1=datetime.strptime(period.split("-")[0],"%Y%m%d")
    date2=datetime.strptime(period.split("-")[1],"%Y%m%d")
    ts1 = date1.replace(tzinfo=timezone.utc).timestamp()
    ts2 = date2.replace(tzinfo=timezone.utc).timestamp()
    tstamps=[int(ts1),int(ts2)]
    return tstamps

def process_data(hh:str, df:pd.DataFrame, model:str, speed_thr:float)  -> OrderedDict:
    """
    Loops all the data in df, checks if any value
    is over the threshold. Dumps the matching dates and leadtimes
    """
    model_label = model + "_det"
    data = OrderedDict()
    for key in ["dtg","leadtime","timestamp","value"]:
        data[key]=[]
    the_station = df.SID.values[0]  #all the same
    for k,timestamp in enumerate(df.fcdate):
        ltime = df.leadtime.values[k]
        dt_object = datetime.fromtimestamp(timestamp)
        date_str = datetime.strftime(dt_object,"%Y%m%d")
        dtg=date_str+hh #str(ltime).zfill(2)
        val = df[model_label].values[k]
        if val >= speed_thr:
            print(f"Found a value {val} on {dtg} and {timestamp}")
            data["dtg"].append(dtg)
            data["leadtime"].append(ltime)
            data["timestamp"].append(timestamp)
            data["value"].append(val)
    return data

if __name__=="__main__":
    outpath="/dmidata/scratch/10day/cap"
    stations_dk=pd.read_csv("stations_dk_reduced.csv")
    stations_dk=pd.read_csv("stations_ulrik.csv")
    stations_ulrik=pd.read_csv("stations_ulrik.csv")
    dbase_path="/data/projects/nckf/danra/verification/FCTABLE"
    #stations=[6180,6181,6183,6188]
    speed_thr = GALE_WIND
    pref="FCTABLE"
    var="Gmax"
    var="S10m"
    year="2018"
    hh="12"
    model="nea40h11"
    years = ["2018","2019","2020","2021","2022"]

    for year in years:
        for hh in [str(i).zfill(2) for i in range(0,22,3)]:
            dates = [year+str(d).zfill(2) for d in range(1,13)]
            for date in dates:
                month = date[4:6]
                dbase = os.path.join(dbase_path,model,year,month,"_".join([pref,var,date,hh])+".sqlite")
                if os.path.isfile(dbase):
                    print(f"Opening dbase {dbase}")
                    conn = sqlite3.connect(dbase)
                    #Look in all stations from Ulrik list
                    for k,SID in enumerate(stations_ulrik.id):
                        find_station = f"SELECT * FROM FC WHERE (SID={SID});"
                        df=pd.read_sql(find_station, conn)
                        if df.empty:
                            print("Station not found")
                            continue
                        else:
                            data=process_data(hh,df,model,speed_thr) #finds the time series that fits the threshold
                            df_out = pd.DataFrame(data)
                            if not df_out.empty:
                              out_file=os.path.join(outpath,"_".join([str(SID),date,hh])+".csv")
                              #ts = get_timestamps("20181230-20190103")
                              #df_out=df_out[(df_out.timestamp >= ts[0])] # & (df_out.timestamp <= ts[1])]
                              df_out.to_csv(out_file,index=False)
                    conn.close()
                else:
                    print(f"{dbase} not available!")
