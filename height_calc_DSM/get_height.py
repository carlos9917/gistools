'''
Python version of the calculateShadows.sh bash script
originally used to call Grass
'''
import sqlite3
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
#where the tiles are located
import shadowFunctions as sf
from search_zipfiles_nounzip import TIF_files as TIF_files

TILESDIR="/data/users/cap/DSM_DK"
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

def get_height(coords,elevation):
    import rasterio
    #coords = ((147.363,-36.419), (147.361,-36.430))
    #elevation = 'srtm_66_20.tif'
    with rasterio.open(elevation) as src:
        row, col = src.index(coords[0], coords[1])
        dem_data = src.read(1).astype('float64')
        height = dem_data[row,col]
        print(f"Height for this station: {height}")
        #print(dem_band[east,north])
        #vals = src.sample(coords)
        #for val in vals:
        #    print(val)
        #    #print(val[0]) #val is an array of values, 1 element 
        #                  #per band. src is a single band raster 
        #                  #so we only need val[0]
    

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
    stretchlist=args.stretch_list #${1-stretchlist_utm.csv}
    cfile=args.config_file
    shpars=sf.read_conf(cfile)
    tilesDir=TILESDIR
    #The output will be written in this directory
    out_dir="processing_tiles"
    src_dir="." #where the scripts are

    resolution=shpars['resolution']
    horizonstep=shpars['horizonstep']
    tileside=shpars['tileside']
    maxdistance=shpars['maxdistance']
    mindist=shpars['mindist']
    mintiles=shpars['mintiles']

    #This is the directory where I will copy and unpack the zip files:
    tilesdir=os.path.join(out_dir)
    now=datetime.strftime(datetime.now(),'%Y%m%d_%H%M%S')
    print("Starting on %s"%now)
    print("Processing stretch  %s"%stretchlist)
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
        logger.info("Reading data from %s"%stretchlist)    
        stretch_data = sf.read_stretch(stretchlist)
    elif args.station != None:
        stretch_data = sf.read_station(args.station)

    if stretch_data.empty:
        print("Station list %s empty!"%strechlist)
        print("Stopping height calculation for this list")
        sys.exit()
    print("before tiles list")
    tiles_list = sf.calc_tiles(stretch_data)
    tif_files=sf.read_tif_list(os.path.join(src_dir,'list_of_tif_files.txt'))
    tiles_needed = sf.loop_tilelist(tiles_list,tif_files,tilesdir)
    #this_tile = tiles_needed["station_tile"]
    #I want only the tile containing the station
    this_tile= tiles_needed[tiles_needed["station_tile"] == tiles_needed["surrounding_tile"]]

    #locate the files I need
    avail_tifs=TIF_files(zipfiles='zip_files_list.txt',zipdir='list_zip_contents',outdir=out_dir)
    lookup_tifs = [this_tile["tif_file"].values[0].split("/")[-1]]
    zipfile=avail_tifs.find_zipfiles(lookup_tifs)
    #the original function expects a list of files, but here I only need one
    zipfile = "".join(zipfile)
    localfile=os.path.join(TILESDIR,zipfile)
    get_zipfile(localfile,out_dir)
    unzip_file(zipfile,this_tile["tif_file"].values[0],out_dir)
    elevation = this_tile["tif_file"].values[0]
    coords=(float(this_tile.coords.values[0].split("|")[0]),
           float(this_tile.coords.values[0].split("|")[1]))
    get_height(coords,elevation)
    #Clean up
    import shutil
    print(f"Removing {out_dir}")
    #shutil.rmtree(out_dir)

    #sf.call_grass("set_resolution",shpars)
    #SHADOW CALCULATION
    #sf.calc_shadows(stretch_data,tiles_needed,shpars,out_dir,shpars)
    #logger.info("Shadow calculation done")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''If no argument provided it will take the default config file
             Example usage: ./calculateShadows.py -c shadows_conf.ini''', formatter_class=RawTextHelpFormatter)

    parser.add_argument('-c','--config_file',
           metavar='config file to be read',
           type=str,
           default='./shadows_conf.ini',
           required=False)

    parser.add_argument('-sl','--stretch_list',
           metavar='list of stations to be processed',
           type=str,
           default="./stretchlist_utm.csv",
           required=False)

    parser.add_argument('-st','--station',
           metavar='Station name and coordinates, separated by commas (ie, Skagen, lat,lon)',
           type=str,
           default=None,
           required=False)

    parser.add_argument('-lg','--log_file',metavar='Log file name',
                                type=str, default='heights.log', required=False)

    args = parser.parse_args()
    print(args)
    main(args)
