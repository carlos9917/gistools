#!/usr/bin/env python3
'''
Save the details of the zip files contents in a json file
'''
import json
import os
from collections import OrderedDict
if __name__=="__main__":
    zipfiles = "zip_files_list.txt" #all the zip files
    zipfilescontents = "list_zip_contents" #tif files on each zip file
    zipcontlist = os.listdir(zipfilescontents)
    with open(zipfiles,"r") as f:
        rlines = f.readlines()
    ziplist = [line.rstrip() for line in rlines]
    zip_contents = OrderedDict()
    for zfile in ziplist:
        tile = "_".join([zfile.split("_")[1],zfile.split("_")[2]])
        czip = os.path.join(zipfilescontents,"tif_files_DSM_"+tile+".txt")
        with open(czip,"r") as f:
            rlines = f.readlines()
        ziplist = [line.rstrip() for line in rlines]
        zip_contents[zfile] = ziplist
    with open("zip_contents.json","w") as f:
        json.dump(zip_contents,f,indent=4)


