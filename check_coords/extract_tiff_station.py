'''
Extract the tif file for a particular station
'''
from datetime import datetime
import argparse
from argparse import RawTextHelpFormatter
import configparser
from collections import OrderedDict
import os
import pandas as pd
import sys
import logging
import shutil
import subprocess
import numpy as np
import shutil

root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath('../'))
from height_calc_DSM import helperFunctions as sf
#where the tiles are located
from height_calc_DSM.TIF_files import TIF_files as TIF_files

TILESDIR="/data/users/cap/DSM_DK"
ZIPDATA="../height_calc_DSM/zip_contents.json"

def get_zipfile(filepath,localpath):
    """
    filepath
    """
    filedest = os.path.join(localpath,filepath.split("/")[-1])
    if not os.path.isfile(filedest):
        try:
            #cmd=f"cp {original}"
            shutil.copy2(filepath,localpath)
            #out=subprocess.check_output(cmd,stderr=subprocess.STDOUT,shell=True)
        except OSError as err:
        #except subprocess.CalledProcessError as err:
            print(f"Error copying {filepath} to {localpath}: {err}")
    else:
        print(f"{filepath} already copied to {filedest}")

def unzip_file(zip_file,tif_file,dest):

    if not os.path.isfile(tif_file):
        try:
            local=os.getcwd()
            os.chdir(dest)
            cmd=f"unzip {zip_file}"
            out=subprocess.check_output(cmd,stderr=subprocess.STDOUT,shell=True)
            os.chdir(local)
        except subprocess.CalledProcessError as err:
            print(f"Error unzipping {zip_file} to {dest}: {err}")

def get_height(coords,elevation) -> float:
    import rasterio
    #coords = ((147.363,-36.419), (147.361,-36.430))
    #elevation = 'srtm_66_20.tif'
    with rasterio.open(elevation) as src:
        row, col = src.index(coords[0], coords[1])
        dem_data = src.read(1).astype('float64')
        height = dem_data[row,col]
        print(f"Height for this station: {height}")
        return height

#logger = logging.getLogger(__name__)
def setup_logger(logFile,outScreen=False):
    '''
    Set up the logger output
    '''
    global logger
    global fmt
    global fname
    logger = logging.getLogger(__name__)
    fmt_debug = logging.Formatter('%(levelname)s:%(name)s %(message)s - %(asctime)s -  %(module)s.%(funcName)s:%(lineno)s')
    fmt_default = logging.Formatter('%(levelname)-8s:  %(asctime)s -- %(name)s: %(message)s')
    fmt = fmt_default
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    fname = logFile
    fh = logging.FileHandler(fname, mode='w')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(fmt)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(fmt)

    logger.addHandler(fh)
    if outScreen:
        logger.addHandler(ch) # Turn on to also log to screen


def main(args):
    stretchlist=args.stretch_list
    tilesDir=TILESDIR
    #The output will be written in this directory
    out_dir="processing_tiles"
    src_dir="." #where the scripts are
    #This is the directory where I will copy and unpack the zip files:
    tilesdir=os.path.join(out_dir)
    now=datetime.strftime(datetime.now(),'%Y%m%d_%H%M%S')
    print("Starting on %s"%now)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    else:
        print("Output directory %s already exists"%out_dir)
    logFile=args.log_file
    setup_logger(logFile,outScreen=False)
    logger.info("Starting height calculation")
    #PRE-PROCESSING
    if os.path.isfile(args.stretch_list):
        print(f"Using list of stations {args.stretch_list}")
        if not "utm" in args.stretch_list: print(f"WARNING: File must contain UTM coordinates!")
        logger.info("Reading data from %s"%stretchlist)    
        stretch_data = sf.read_stretch(stretchlist)
    elif args.station != None:
        stretch_data = sf.read_station(args.station)
    #locate the files I need
    import json
    with open(ZIPDATA,"r") as f:
        zipcontents = json.load(f)
    avail_tifs=TIF_files(zipcontents)

    if stretch_data.empty:
        print("Station list %s empty!"%strechlist)
        print("Stopping height calculation for this list")
        sys.exit()

    tiles_list = sf.calc_tiles(stretch_data)
    tif_files = np.array(avail_tifs.tiflist)
    tiles_needed = sf.loop_tilelist(tiles_list,tif_files,tilesdir)
    #I want only the tile containing the station
    tiles_selected= tiles_needed[tiles_needed["station_tile"] == tiles_needed["surrounding_tile"]]
    if tiles_selected.empty:
        print("No tiles found for station(s) provided!")
        sys.exit(1)

    #TODO: if the stretch list is more than one station 
    # do a loop here where tiles_selected is one of each in the list above
    allData=OrderedDict()
    for label in ["station","height"]:
        allData[label] = []
    for k in range(len(tiles_selected)):
        this_tile=tiles_selected.iloc[k]
        #lookup_tifs = [this_tile["tif_file"].values[0].split("/")[-1]]
        lookup_tifs = [this_tile["tif_file"].split("/")[-1]]
        zipfile = avail_tifs.find_zipfiles(lookup_tifs)
        #the original function expects a list of files, but here I only need one
        zipfile = "".join(zipfile)
        localfile = os.path.join(TILESDIR,zipfile)
        get_zipfile(localfile,out_dir)
        #unzip_file(zipfile,this_tile["tif_file"].values[0],out_dir)
        #elevation = this_tile["tif_file"].values[0]
        unzip_file(zipfile,this_tile["tif_file"],out_dir)
        elevation = this_tile["tif_file"]
        coords = (float(this_tile.coords.split("|")[0]),
                  float(this_tile.coords.split("|")[1]))

        stdata= this_tile.coords.split("|")
        station_id = stdata[3]+stdata[2].zfill(2)+stdata[4].zfill(2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''
             Example usage: ./get_height.py -sl coords_utm.csv''', formatter_class=RawTextHelpFormatter)

    parser.add_argument('-sl','--stretch_list',
           metavar='list of stations to be processed',
           type=str,
           default="./stretchlist_utm.csv",
           required=False)

    parser.add_argument('-st','--station',
           metavar='Station name and UTM coordinates, separated by commas (ie, 3011,519379.289172,6123006.457084)',
           type=str,
           default=None,
           required=False)

    parser.add_argument('-lg','--log_file',metavar='Log file name',
                                type=str, default='heights.log', required=False)

    args = parser.parse_args()
    print(args)
    main(args)
