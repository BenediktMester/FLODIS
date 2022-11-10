#!/usr/bin/env python

""" Interpolation of GPW population count data. """
# Import modules
import rasterio
import numpy as np
import sys
import os
from numpy import inf

# Create paths
 
def mkdir(dir):    
    if not os.path.exists(dir):
        os.mkdir(dir)

path_local = sys.argv[1]
path_run = sys.argv[2]

pop_new_path = path_local + 'data/population/GPW_population_interpolated/'
pop_new_path_creator = mkdir(pop_new_path)
path_pop = path_local + 'data/population/'
pop_2000 = rasterio.open(path_pop + 'gpw_v4_population_count_rev11_2000_30_sec.tif')
pop_2005 = rasterio.open(path_pop + 'gpw_v4_population_count_rev11_2005_30_sec.tif')
pop_2010 = rasterio.open(path_pop + 'gpw_v4_population_count_rev11_2010_30_sec.tif')
pop_2015 = rasterio.open(path_pop + 'gpw_v4_population_count_rev11_2015_30_sec.tif')
pop_2020 = rasterio.open(path_pop + 'gpw_v4_population_count_rev11_2020_30_sec.tif')
pop_profile = pop_2000.profile
pop_2000_np = np.float32(pop_2000.read(1))
pop_2005_np = np.float32(pop_2005.read(1))
pop_2010_np = np.float32(pop_2010.read(1))
pop_2015_np = np.float32(pop_2015.read(1))
pop_2020_np = np.float32(pop_2020.read(1))
pop_2000_np[np.isnan(pop_2000_np)] = 0
pop_2005_np[np.isnan(pop_2005_np)] = 0
pop_2010_np[np.isnan(pop_2010_np)] = 0
pop_2015_np[np.isnan(pop_2015_np)] = 0
pop_2020_np[np.isnan(pop_2020_np)] = 0
pop_2000_np[pop_2000_np < 0] = 0
pop_2000_np[pop_2000_np > 1_000_000_000] = 0
pop_2005_np[pop_2005_np < 0] = 0
pop_2005_np[pop_2005_np > 1_000_000_000] = 0
pop_2010_np[pop_2010_np < 0] = 0
pop_2010_np[pop_2010_np > 1_000_000_000] = 0
pop_2015_np[pop_2015_np < 0] = 0
pop_2015_np[pop_2015_np > 1_000_000_000] = 0
pop_2020_np[pop_2020_np < 0] = 0
pop_2020_np[pop_2020_np > 1_000_000_000] = 0

#%%

def main():

    # 2000
    
    pop_temp_np = np.float32(pop_2000_np * 5 + pop_2005_np * 0)/5
    
    with rasterio.open(pop_new_path + 'gpw_population_2000_30_sec.tif', 'w', **pop_profile) as dst:
        dst.write_band(1, pop_temp_np) 
        
    # 2001
    
    pop_temp_np = np.float32(pop_2000_np * 4 + pop_2005_np * 1)/5
    
    with rasterio.open(pop_new_path + 'gpw_population_2001_30_sec.tif', 'w', **pop_profile) as dst:
        dst.write_band(1, pop_temp_np) 
        
    # 2002
    
    pop_temp_np = np.float32(pop_2000_np * 3 + pop_2005_np * 2)/5
    
    with rasterio.open(pop_new_path + 'gpw_population_2002_30_sec.tif', 'w', **pop_profile) as dst:
        dst.write_band(1, pop_temp_np) 
        
    # 2003
    
    pop_temp_np = np.float32(pop_2000_np * 2 + pop_2005_np * 3)/5
    
    with rasterio.open(pop_new_path + 'gpw_population_2003_30_sec.tif', 'w', **pop_profile) as dst:
        dst.write_band(1, pop_temp_np) 
    
    # 2004
    
    pop_temp_np = np.float32(pop_2000_np * 1 + pop_2005_np * 4)/5
    
    with rasterio.open(pop_new_path + 'gpw_population_2004_30_sec.tif', 'w', **pop_profile) as dst:
        dst.write_band(1, pop_temp_np) 
    
    # 2005
    
    pop_temp_np = np.float32(pop_2000_np * 0 + pop_2005_np * 5)/5
    
    with rasterio.open(pop_new_path + 'gpw_population_2005_30_sec.tif', 'w', **pop_profile) as dst:
        dst.write_band(1, pop_temp_np) 
    
    #%%
    
    # 2006
    
    pop_temp_np = np.float32(pop_2005_np * 5 + pop_2010_np * 0)/5
    
    with rasterio.open(pop_new_path + 'gpw_population_2006_30_sec.tif', 'w', **pop_profile) as dst:
        dst.write_band(1, pop_temp_np) 
        
    # 2007
    
    pop_temp_np = np.float32(pop_2005_np * 4 + pop_2010_np * 1)/5
    
    with rasterio.open(pop_new_path + 'gpw_population_2007_30_sec.tif', 'w', **pop_profile) as dst:
        dst.write_band(1, pop_temp_np) 
        
    # 2008
    
    pop_temp_np = np.float32(pop_2005_np * 3 + pop_2010_np * 2)/5
    
    with rasterio.open(pop_new_path + 'gpw_population_2008_30_sec.tif', 'w', **pop_profile) as dst:
        dst.write_band(1, pop_temp_np) 
        
    # 2009
    
    pop_temp_np = np.float32(pop_2005_np * 2 + pop_2010_np * 3)/5
    
    with rasterio.open(pop_new_path + 'gpw_population_2009_30_sec.tif', 'w', **pop_profile) as dst:
        dst.write_band(1, pop_temp_np) 
    
    # 2010
    
    pop_temp_np = np.float32(pop_2005_np * 1 + pop_2010_np * 4)/5
    
    with rasterio.open(pop_new_path + 'gpw_population_2010_30_sec.tif', 'w', **pop_profile) as dst:
        dst.write_band(1, pop_temp_np) 
     
    #%%
        
    # 2011
    
    pop_temp_np = np.float32(pop_2010_np * 4 + pop_2015_np * 1)/5
    
    with rasterio.open(pop_new_path + 'gpw_population_2011_30_sec.tif', 'w', **pop_profile) as dst:
        dst.write_band(1, pop_temp_np) 
        
    # 2012
    
    pop_temp_np = np.float32(pop_2010_np * 3 + pop_2015_np * 2)/5
    
    with rasterio.open(pop_new_path + 'gpw_population_2012_30_sec.tif', 'w', **pop_profile) as dst:
        dst.write_band(1, pop_temp_np) 
        
    # 2013
    
    pop_temp_np = np.float32(pop_2010_np * 2 + pop_2015_np * 3)/5
    
    with rasterio.open(pop_new_path + 'gpw_population_2013_30_sec.tif', 'w', **pop_profile) as dst:
        dst.write_band(1, pop_temp_np) 
    
    # 2014
    
    pop_temp_np = np.float32(pop_2010_np * 1 + pop_2015_np * 4)/5
    
    with rasterio.open(pop_new_path + 'gpw_population_2014_30_sec.tif', 'w', **pop_profile) as dst:
        dst.write_band(1, pop_temp_np) 
    
    # 2015
    
    pop_temp_np = np.float32(pop_2010_np * 0 + pop_2015_np * 5)/5
    
    with rasterio.open(pop_new_path + 'gpw_population_2015_30_sec.tif', 'w', **pop_profile) as dst:
        dst.write_band(1, pop_temp_np) 
       
    # 2016
    
    pop_temp_np = np.float32(pop_2015_np * 4 + pop_2020_np * 1)/5
    
    with rasterio.open(pop_new_path + 'gpw_population_2016_30_sec.tif', 'w', **pop_profile) as dst:
        dst.write_band(1, pop_temp_np) 
        
    # 2017
    
    pop_temp_np = np.float32(pop_2015_np * 3 + pop_2020_np * 2)/5
    
    with rasterio.open(pop_new_path + 'gpw_population_2017_30_sec.tif', 'w', **pop_profile) as dst:
        dst.write_band(1, pop_temp_np) 
        
    # 2018
    
    pop_temp_np = np.float32(pop_2015_np * 2 + pop_2020_np * 3)/5
    
    with rasterio.open(pop_new_path + 'gpw_population_2018_30_sec.tif', 'w', **pop_profile) as dst:
        dst.write_band(1, pop_temp_np) 
    
    # 2019
    
    pop_temp_np = np.float32(pop_2015_np * 1 + pop_2020_np * 4)/5
    
    with rasterio.open(pop_new_path + 'gpw_population_2019_30_sec.tif', 'w', **pop_profile) as dst:
        dst.write_band(1, pop_temp_np) 
    
    # 2020
    
    pop_temp_np = np.float32(pop_2015_np * 0 + pop_2020_np * 5)/5
    
    with rasterio.open(pop_new_path + 'gpw_population_2020_30_sec.tif', 'w', **pop_profile) as dst:
        dst.write_band(1, pop_temp_np) 
    
    #%%
    
    print('job succesfully completed!')

#%%

if __name__ == "__main__":
    main()

