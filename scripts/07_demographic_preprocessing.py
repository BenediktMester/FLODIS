#!/usr/bin/env python

""" Computation of female population density in %. 
Computation of population aging 0-14 and 65+ years. 
"""
# Import modules   
import rasterio
import numpy as np
import sys

# Make paths
path_local = sys.argv[1]
path_run = sys.argv[2]

def mkdir(dir):
    
    if not os.path.exists(dir):
        os.mkdir(dir)
        
data_path = path_local + 'data/demographic/'
data_processed_path = path_run + 'data_processed/'

crs = {'init' :'epsg:4326'} 

#%%

def main():
    
    # Female population    
    pop = rasterio.open(data_path + 'gpw_v4_basic_demographic_characteristics_rev11_atotpopbt_2010_cntm_30_sec.tif') # total population (female and male)
    pop_profile = pop.profile
    pop_profile['driver'] = 'GTiff'
    pop_profile['count'] = 1
    pop_profile['dtype'] = 'float32'
    pop_profile['crs'] = crs 
    pop_total = pop.read()
    
    pop_female = rasterio.open(data_path + 'gpw_v4_basic_demographic_characteristics_rev11_atotpopft_2010_cntm_30_sec.tif').read() # total population (female only)
    pop_female_perc = np.squeeze(pop_female/pop_total)
    
    with rasterio.open(data_processed_path + f"female_perc.tif", 'w', **pop_profile) as dst:
        dst.write_band(1, pop_female_perc) 
        
    #%%
    
    # Age structure    
    pop_0_14 = rasterio.open(data_path + 'gpw_v4_basic_demographic_characteristics_rev11_a000_014bt_2010_cntm_30_sec.tif').read()
    pop_65_plus = rasterio.open(data_path + 'gpw_v4_basic_demographic_characteristics_rev11_a065plusbt_2010_cntm_30_sec.tif').read()
    pop_0_14_perc = np.squeeze(pop_0_14/pop_total)
    pop_65_plus_perc = np.squeeze(pop_65_plus/pop_total)
    
    with rasterio.open(data_processed_path + f"pop_0_14_perc.tif", 'w', **pop_profile) as dst:
        dst.write_band(1, pop_0_14_perc) 
    
    with rasterio.open(data_processed_path + f"pop_65_plus_perc.tif", 'w', **pop_profile) as dst:
        dst.write_band(1, pop_65_plus_perc) 
    
    #%%
    
    print('job succesfully completed!')

#%%

if __name__ == "__main__":
    main()
