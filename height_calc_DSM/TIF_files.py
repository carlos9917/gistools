from collections import OrderedDict
import os,sys
import subprocess
import json

class TIF_files:
    def __init__(self,zipcontents):
        #Read the available data and setup the dicts
        tiflist=[]
        for key in zipcontents:
            tiflist.extend(zipcontents[key])
        self.alltifs = zipcontents #alltifs
        self.tiflist = tiflist

    def find_zipfiles(self,look_items): #tiflist):
        #find the zip files I need to uncompress
        #according to the tiflist
        found_keys=[]
        for look_item in look_items:
            for zipfile in self.alltifs.keys():
                if look_item in self.alltifs[zipfile]:
                    #print("Found it %s"%zipfile)
                    found_keys.append(zipfile)
        #remove any repeated entries
        found_keys=set(found_keys)
        return found_keys            

if __name__ == '__main__':
    avail_tifs=TIF_files(zipdata)
