import sqlite3
import pandas as pd
dbase="data/stations_coords_height.db"
con=sqlite3.connect(dbase)
com="SELECT * FROM roadstations"
df_stations = pd.read_sql(com,con)
con.close()

df_stations["SID_partial"] = [int(str(sid)[0:4]) for sid in df_stations.SID]

from collections import OrderedDict
list_before=OrderedDict()
list_after=OrderedDict()


list_before["nwz"]=[2000, 2001, 2005, 2026, 2030, 2031, 2038, 2100, 2140, 2142]
list_after["nwz"]=[2000, 2001, 2005, 2026, 2030, 2031, 2038, 2100, 2101, 2102, 2103, 2104, 2105, 2106, 2107, 2108, 2109, 2110, 2111, 2112, 2113, 2114, 2115, 2116, 2117, 2118, 2119, 2140, 2142, 2400]

list_before["mju"] = [4006, 4011, 4013, 4023, 4025, 4026, 4029, 4140, 4143, 4180, 4181, 4183, 4220, 5006, 5031, 5164, 5165, 5167]
list_after["mju"] = [4006, 4011, 4013, 4023, 4025, 4026, 4029, 4140, 4143, 4180, 4181, 4183, 4184, 4185, 4186, 4187, 4188, 4189, 4190, 4191, 4192, 4220, 5006, 5031, 5164, 5165, 5167]

list_before["fyn"]=[3024, 3025, 3026, 3027, 3029, 3030, 3031, 3032, 3036, 3038, 3039, 3040, 3041, 3043, 3280, 3300, 3301, 3320, 3340, 3341, 3342, 3344, 3345, 3346, 3347, 3348, 3349, 3350, 3351, 3360, 3361, 3362, 3363, 3420, 3421, 9909, 9910]
list_after["fyn"]=[3024, 3025, 3026, 3027, 3029, 3030, 3031, 3032, 3036, 3038, 3039, 3040, 3041, 3043, 3280, 3300, 3301, 3320, 3340, 3341, 3342, 3344, 3345, 3346, 3347, 3348, 3349, 3350, 3351, 3360, 3361, 3362, 3363, 3364, 3365, 3366, 3367, 3368, 3369, 3370, 3371, 3372, 3373, 3374, 3375, 3376, 3377, 3378, 3379, 3380, 3381, 3382, 3383, 3384, 3385, 3386, 3387, 3388, 3420, 3421, 9909, 9910]


for key in list_before.keys():
    lookup=list_before[key]
    sel_st = df_stations[df_stations["SID_partial"].isin(lookup)]["SID"].to_list()
    print(f"Stations before {key}")
    print(sel_st)

for key in list_after.keys():
    lookup=list_after[key]
    sel_st = df_stations[df_stations["SID_partial"].isin(lookup)]["SID"].to_list()
    print(f"Stations after {key}")
    print(sel_st)
