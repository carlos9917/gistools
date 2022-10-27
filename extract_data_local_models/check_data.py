import sqlite3
import pandas as pd
from datetime import datetime
from collections import OrderedDict
import os

import stations_inside_circle as sic
also_data = OrderedDict()
for key in ["dtg","value","station"]:
    also_data[key]=[]

def process_data(df:pd.DataFrame)  -> OrderedDict:
    data = OrderedDict()
    for key in ["dtg","leadtime","timestamp","value","station"]:
        data[key]=[]
    the_station = df.SID.values[0]  #all the same
    for k,timestamp in enumerate(df.fcdate):
        ltime = df.leadtime.values[k]
        dt_object = datetime.fromtimestamp(timestamp)
        date_str = datetime.strftime(dt_object,"%Y%m%d")
        dtg=date_str+str(ltime).zfill(2)
        val = df.nea40h11_det.values[k]
        if val >= speed_thr:
            print(f"Found a value {val} on {dtg} and {timestamp}")
            data["dtg"].append(dtg)
            data["leadtime"].append(ltime)
            data["timestamp"].append(timestamp)
            data["value"].append(val)
            data["station"].append(the_station)
        #data["val"].append(val)
        #data["date"].append(dtg)
    return data

if __name__=="__main__":
    stations_dk=pd.read_csv("stations_dk_reduced.csv")
    stations_dk=pd.read_csv("stations_ulrik.csv")
    stations_ulrik=pd.read_csv("stations_ulrik.csv")
    dbase_path="/data/projects/nckf/danra/verification/FCTABLE"
    speed_thr = 17
    pref="FCTABLE"
    var="Gmax"
    var="S10m"
    year="2018"
    hh="12"
    model="nea40h11"
    for year in ["2021","2022"]:
        for hh in [str(i).zfill(2) for i in range(0,22,3)]:
            for date in [year+str(d).zfill(2) for d in range(1,13)]:
                month = date[4:6]
                dbase = os.path.join(dbase_path,model,year,month,"_".join([pref,var,date,hh])+".sqlite")
                if os.path.isfile(dbase):
                    print(f"Opening dbase {dbase}")
                else:
                    print(f">>>> No file {dbase}!!!!")
                    continue
                conn = sqlite3.connect(dbase)
                #Special case: select only the 6181:
                #stations_ulrik = stations_ulrik[stations_ulrik["id"] == 6181]
                for k,SID in enumerate(stations_ulrik.id):
                    find_station = f"SELECT * FROM FC WHERE (SID={SID});"
                    df=pd.read_sql(find_station, conn)
                    if df.empty:
                        print("Station not found")
                    else:
                        data=process_data(df) #finds the time series that fits the threshold
                        df_out = pd.DataFrame(data)

                        station_data=dict()
                        station_data["lat"] = stations_ulrik.lat.values[k]
                        station_data["lon"] = stations_ulrik.lon.values[k]
                        station_data["id"] = SID
                        #this checks which stations surround station with SID
                        nearby_stations = sic.check_around(station_data, stations_dk,50)
                        #search again, with all these:
                        all_of_the_rest=[] #dict()
                        #for ns in nearby_stations:
                        #    all_of_the_rest[ns]=[]
                        for ns in nearby_stations:
                            find_station = f"SELECT * FROM FC WHERE (SID={ns});"
                            df=pd.read_sql(find_station, conn)
                            if not df.empty:
                                data=process_data(df)
                                del df
                            #all_of_the_rest[ns].append(pd.DataFrame(data))
                            all_of_the_rest.append(pd.DataFrame(data))
                        all_of_the_rest.append(df_out)    
                        for check_dtg in df_out.dtg:
                            for this_df in all_of_the_rest:
                                find_dtg = this_df[this_df.dtg == check_dtg]
                                if not find_dtg.empty:
                                    print(f"Found matching in {check_dtg}")
                                    also_data["station"].append(find_dtg.station.values[0])
                                    also_data["dtg"].append(find_dtg.dtg.values[0])
                                    also_data["value"].append(find_dtg.value.values[0])
                        #merge_all = pd.concat(all_of_the_rest)
                        #then merge the dataframes and see how it looks?
                        df_comp = pd.DataFrame(also_data)
                        if not df_comp.empty:
                            out_file=str(SID)+"_"+date+"_"+hh+"_"+var+".csv"
                            df_comp.to_csv(out_file,index=False)
                        #if not df_out.empty:
                        #    print(f"Found data for {date}. Writing to disk")
                        #    out_file=str(SID)+"_"+date+"_"+hh+"_"+var+".csv"
                        #    df_out.to_csv(out_file,index=False)
                conn.close()
