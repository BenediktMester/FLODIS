#!/usr/bin/env python

""" All GFD IDs are looped, and passed into this script. For each entry all available .shp files are collected, and converted from .tif to .shp. 

If several .shp files are available for one GFD ID, the flood extent is merged ("counter" variable > 1).
"""
# Import modules 
import sys
import os
import geopandas as gpd
import pandas as pd
import numpy as np
import rasterio
import fiona
import shapely
from shapely.geometry import shape
from datetime import datetime
import rasterio.mask
from pyproj import Proj, transform

# Make paths
path_local = sys.argv[1]
path_run = sys.argv[2]
DFO_ID = sys.argv[3]

path_satellite_shape_files = path_run + 'satellite_shape_files/'
path_satellite_shape_files_final = path_run + 'satellite_shape_files_final/'
path_satellite_tif_files = path_run + 'satellite_tif_files/'
path_satellite = path_local + 'data/disaster/DFO/gfd_v1_4/tif_files/'
DFO_shape = gpd.read_file(path_local + 'data/disaster/DFO/gfd_v1_4/shp_files/dfo_polys_20191203.shp')
DFO_shape = DFO_shape[DFO_shape['ID'] == int(DFO_ID)]
began = datetime.strptime(DFO_shape['Began'].iloc[0],"%Y-%m-%d")
ended = datetime.strptime(DFO_shape['Ended'].iloc[0],"%Y-%m-%d")
middle_year = (began.date() + ((ended-began) / 2)).year  

#%%

def main():

    counter = 0
    
    for filename in os.listdir(path_satellite):   
        filename_cut = filename.split("DFO_")[1]
        filename_cut = filename_cut.split("_From")[0]
    
        if filename_cut == DFO_ID:  
            DFO_satellite = rasterio.open(path_satellite + filename)
            DFO_satellite_profile = DFO_satellite.profile
            DFO_satellite_profile['count'] = 1
            DFO_satellite_profile['dtype'] = 'float32'
            DFO_satellite = DFO_satellite.read(1).astype(float)
            DFO_satellite = np.float32(DFO_satellite)
            DFO_satellite[DFO_satellite == 0] = np.nan
            path_DFO_satellite_tif = f"{path_satellite_tif_files}DFO_{filename_cut}_{counter}.tif" 
    
            with rasterio.open(path_DFO_satellite_tif, 'w', **DFO_satellite_profile) as dst:
                dst.write_band(1, DFO_satellite)  
                            
            # tif to shp    
            path_DFO_satellite_shape = f"{path_satellite_shape_files}DFO_{filename_cut}_{counter}.shp"    
            mask = None
    
            from rasterio.features import shapes
    
            with rasterio.Env():
                with rasterio.open(path_DFO_satellite_tif) as src:
                    image = src.read()
    
                results = (
                {'properties': {'raster_val': v}, 'geometry': s}
                for i, (s, v)
                in enumerate(
                shapes(image, mask=mask, transform=src.transform)))
    
                with fiona.open(
                path_DFO_satellite_shape, 'w',
                driver='Shapefile',
                crs=src.crs,
                schema={'properties': [('raster_val', 'int')],
                'geometry': 'Polygon'}) as dst:
                    dst.writerecords(results)
    
            satellite_shape_dissolved = gpd.read_file(path_DFO_satellite_shape)
            satellite_shape_dissolved = satellite_shape_dissolved[satellite_shape_dissolved['raster_val'] == 1]    
            satellite_shape_dissolved = satellite_shape_dissolved.dissolve(by='raster_val')
            satellite_shape_dissolved.to_file(path_DFO_satellite_shape)
            counter += 1
    
    #%%
    
    if counter > 1:
        
        for counter_2 in range(counter):        
            DFO_satellite_shape = gpd.read_file(f"{path_satellite_shape_files}DFO_{DFO_ID}_{counter_2}.shp")
            
            if counter_2 == 0:            
                union = DFO_satellite_shape
                
            else:            
                union = gpd.overlay(union, DFO_satellite_shape, how='union')
                union['unit'] = 0
                union = union.dissolve(by='unit')            
    
        union.to_file(f"{path_satellite_shape_files_final}DFO_{DFO_ID}_final_{middle_year}.shp")
    
    else:    
        DFO_satellite_shape = gpd.read_file(f"{path_satellite_shape_files}DFO_{DFO_ID}_0.shp")
        DFO_satellite_shape.to_file(f"{path_satellite_shape_files_final}DFO_{DFO_ID}_final_{middle_year}.shp")
    
    #%%
    
    print('job succesfully completed!')

#%%

if __name__ == "__main__":
    main()
