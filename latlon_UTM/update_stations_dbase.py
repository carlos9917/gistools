import pandas as pd
import sqlite3

def create_dbase(dbase:str,
                    table:str) -> None:
    """
    Create an empty database for the tables listed in tables
    """
    conn = sqlite3.connect(dbase)
    cursor = conn.cursor()
    create_schema = f"""
    CREATE TABLE IF NOT EXISTS {table} (
           SID INTEGER,
           lon FLOAT,
           lat FLOAT,
           height FLOAT
           )
    """

    cursor.execute(create_schema)
    conn.close()


def update_dbase(dbase:str, 
                 table:str, 
                 df:pd.DataFrame) -> None:
    """
    Update the station data 
    """
    conn = sqlite3.connect(dbase)
    cursor = conn.cursor()
    for k,SID in enumerate(df.station):
        find_station = f"SELECT * FROM {table} WHERE (SID={SID});"
        lat = df["lat"].values[k]
        lon = df["lon"].values[k]
        height = df["height"].values[k]
        entry = cursor.execute(find_station)
        if len(cursor.fetchall()) == 0:
            #insert_row = ",".join([str(SID),"'"+name+"'",str(lat),str(lon),str(height)])
            #com = f'''INSERT OR REPLACE INTO {table} (SID, name, lat, lon ,height) VALUES ('''+insert_row+") "
            insert_row = ",".join([str(SID),str(lat),str(lon),str(height)])
            com = f'''INSERT OR REPLACE INTO {table} (SID, lat, lon ,height) VALUES ('''+insert_row+") "
            cursor.execute(com)
        conn.commit()
    conn.close()


if __name__=="__main__":

    table = "roadstations"
    station_list = "vejvejr_stations.csv"
    height_list = "../height_calc_DSM/all_heights_vejvejr_20230606.csv"

    dbase = "stations_coords_height.db"
    dtypes={"ID":int,"lat":str,"lon":str,"height":str}
    df_ll = pd.read_csv(station_list,dtype={0:int,1:str,2:str,3:str},sep=",")#,header=None)#,
    df_ll.columns=["station","lon","lat"]
    #dtypes={"station":int,"lat":str,"lon":str,"height":str}
    #df_ll["lat"]= df_ll.astype(str)
    #df_ll["lon"]= df_ll.astype(str)

    df_hh = pd.read_csv(height_list,dtype={"station":int,"height":str})
    df = df_ll.merge(df_hh, how='inner', on='station')

    create_dbase(dbase,table)
    update_dbase(dbase,table,df)
