#!/usr/bin/env python

# Import modules
import sys
import os
import numpy as np
import geopandas as gpd
import pandas as pd
from rasterstats import zonal_stats
from datetime import datetime

# Pass run detail
path_local = sys.argv[1]
path_run = sys.argv[2]
filename_temp = sys.argv[3]
filename_temp_cut = filename_temp.split('.shp')[0]

#%%

"""Compute affected entities (mean/sum) and socio-economic properties."""

def compute_affected(path_entity,zonal_stats_function,flood_shape):
    
    stat = zonal_stats(flood_shape,
        path_entity, 
        all_touched = True, 
        stats = [zonal_stats_function])                           
    stat = pd.DataFrame(stat).sum()
    
    try:                    
        stat = round(stat,5)                                                                  
    except:                
        stat = 0
        
    return(stat[0]) 
        
#%%                    

"""Main analysis function. 

Loading and preparing the data, perform matching process, and compute affected entities and socio-economic properties.
"""    
def main():
    
    # Load and prepare data  
    # Load country & province (state) data    
    countries = gpd.read_file(path_local + '/data/states/gadm36_levels_shp/gadm36_0.shp')
    provinces = gpd.read_file(path_local + '/data/states/gadm36_levels_shp/gadm36_1.shp')
    districts = gpd.read_file(path_local + '/data/states/gadm36_levels_shp/gadm36_2.shp')
    subdistricts = gpd.read_file(path_local + '/data/states/gadm36_levels_shp/gadm36_3.shp')
    
    # Prepare EMDAT data    
    EMDAT = gpd.read_file(path_local + 'data/disaster/EMDAT/GDIS_processed/' + filename_temp)
    EMDAT.loc[:,'idx'] = EMDAT.index
    
    # Load DFO flood hazard data    
    path_satellite_shape_files_final = f"{path_local}cluster_jobs/FLODIS_GFD_preprocessing/satellite_shape_files_final/"  
    DFO = gpd.read_file(f"{path_local}data/disaster/DFO/gfd_v1_4/shp_files/dfo_polys_20191203.shp")
    
    # Reduce DFO files to actually available flood shapes    
    found_DFO_ID_list = []    
    for filename in sorted(os.listdir(path_satellite_shape_files_final)):        
        if "shp" in filename:            
            filename_split = filename.split('DFO_')[1]
            filename_split = filename_split.split('_final')[0]            
            found_DFO_ID_list.append(filename_split)   
    DFO = DFO[DFO['ID'].isin(found_DFO_ID_list)].reset_index()    
    DFO_began_year_list = []
    
    for i in range(len(DFO)):    
        DFO_began_year_list.append(datetime.strptime(DFO.loc[i,'Began'],"%Y-%m-%d").strftime('%Y'))
     
    DFO['began_year'] = DFO_began_year_list
    
    #%%
    
    # Start analysis with preparing lists to be filled    
    max_day_difference = 30 # initialize time difference between EMDAT and DFO    
    DFO_match_list = []
    DFO_match_nr_list = []
    DFO_match_time_dif_list = []
    DFO_duration_list = []
    matching_type_list = []
    geometry_list = []    
    DFO_match_nr_temp_list = []
    DFO_match_time_dif_temp_list = []
    DFO_middle_year_temp_list = []
    DFO_began_temp_list = []
    DFO_end_temp_list = []
    DFO_duration_temp_list = []
    EMDAT_year = 0
    matching_type = 0     
    DFO_match_counter = 0
    
    affected_sum_dict = {
        "GDP_affected_sum":f"{path_local}data/gdp/kummu_etal/GDP/GDP_{EMDAT_year}.tif",
        "cable_affected_sum":f"{path_local}data/CISI/cable.tif",              
        "plant_affected_sum":f"{path_local}data/CISI/plant.tif",               
        "power_pole_affected_sum":f"{path_local}data/CISI/power_pole.tif",              
        "power_tower_affected_sum":f"{path_local}data/CISI/power_tower.tif",  
        "line_affected_sum":f"{path_local}data/CISI/line.tif",               
        "mast_affected_sum":f"{path_local}data/CISI/mast.tif",   
        "communication_tower_affected_sum":f"{path_local}data/CISI/communication_tower.tif",                
        "doctors_affected_sum":f"{path_local}data/CISI/doctors.tif",               
        "hospital_affected_sum":f"{path_local}data/CISI/hospital.tif",                            
        "pharmacy_affected_sum":f"{path_local}data/CISI/pharmacy.tif",                            
        "primary_road_affected_sum":f"{path_local}data/CISI/primary.tif",
        "tertiary_road_affected_sum":f"{path_local}data/CISI/tertiary.tif",
        "reservoir_affected_sum":f"{path_local}data/CISI/reservoir.tif",              
        "school_affected_sum":f"{path_local}data/CISI/school.tif",               
        "university_affected_sum":f"{path_local}data/CISI/university.tif"}
                
    affected_mean_dict = {
        "GDP_affected_mean":f"{path_local}data/gdp/kummu_etal/GDP/GDP_{EMDAT_year}.tif",
        "education_affected_mean":f"{path_local}data/CISI/education.tif",              
	    "energy_affected_mean":f"{path_local}data/CISI/energy.tif",              
        "health_affected_mean":f"{path_local}data/CISI/health.tif",              
        "telecommunication_affected_mean":f"{path_local}data/CISI/telecommunication.tif",              
        "transportation_affected_mean":f"{path_local}data/CISI/transportation.tif",              
        "water_affected_mean":f"{path_local}data/CISI/water.tif",      
        "CISI_global_affected_mean":f"{path_local}data/CISI/CISI_global.tif",
        "cable_affected_mean":f"{path_local}data/CISI/cable.tif",              
        "plant_affected_mean":f"{path_local}data/CISI/plant.tif",               
        "power_pole_affected_mean":f"{path_local}data/CISI/power_pole.tif",              
        "power_tower_affected_mean":f"{path_local}data/CISI/power_tower.tif",  
        "line_affected_mean":f"{path_local}data/CISI/line.tif",               
        "mast_affected_mean":f"{path_local}data/CISI/mast.tif",   
        "communication_tower_affected_mean":f"{path_local}data/CISI/communication_tower.tif",                
        "doctors_affected_mean":f"{path_local}data/CISI/doctors.tif",               
        "hospital_affected_mean":f"{path_local}data/CISI/hospital.tif",                            
        "pharmacy_affected_mean":f"{path_local}data/CISI/pharmacy.tif",                            
        "primary_road_affected_mean":f"{path_local}data/CISI/primary.tif",
        "tertiary_road_affected_mean":f"{path_local}data/CISI/tertiary.tif",
        "reservoir_affected_mean":f"{path_local}data/CISI/reservoir.tif",              
        "school_affected_mean":f"{path_local}data/CISI/school.tif",               
        "university_affected_mean":f"{path_local}data/CISI/university.tif",   
        "GDPpc_mean":f"{path_local}data/gdp/kummu_etal/GDPpc/GDPpc_{EMDAT_year}.tif",
        "HDI_mean":f"{path_local}data/gdp/kummu_etal/HDI/HDI_{EMDAT_year}.tif",
        "urbanization_mean":f"{path_local}data/landuse/urbanization/urbanization_{EMDAT_year}.tif",
        "landuse_total_mean":f"{path_local}data/landuse/landuse_total/landuse_total_{EMDAT_year}.tif",               
        "elevation_mean":f"{path_local}data/earthenv_topography/elevation_1KMmn_GMTEDmn.tif",                       
        "roughness_mean":f"{path_local}data/earthenv_topography/roughness_1KMmn_GMTEDmd.tif",                       
        "slope_mean":f"{path_local}data/earthenv_topography/slope_1KMmn_GMTEDmd.tif",         
        "female_mean":f"{path_local}data/demographic/female_perc.tif",               
        "pop_0_14_mean":f"{path_local}data/demographic/pop_0_14_perc.tif",               
        "pop_65_plus_mean":f"{path_local}data/demographic/pop_65_plus_perc.tif",               
        "FLOPROS_merged_mean":f"{path_local}data/FLOPROS/FLOPROS_merged.tif",                
        "FLOPROS_modeled_mean":f"{path_local}data/FLOPROS/FLOPROS_modeled.tif"}
    
    affected_sum_list = []
    affected_sum_list_len = 16
    
    for variable_single in range(affected_sum_list_len):            
        affected_sum_list.append(np.nan)
    
    affected_mean_list = []
    affected_mean_list_len = 35
    
    for variable_single in range(affected_mean_list_len):          
        affected_mean_list.append(np.nan)
    
    #%%
    
    #%%
    
    # Prepare EMDAT affected shape    
    EMDAT_affected_shape = EMDAT.copy()
    
    try:
        EMDAT_date_day = int(EMDAT['Start Mont'].iloc[0])
    except:
        EMDAT_date_day = 15
    
    EMDAT_date = str(EMDAT['Start Year'].iloc[0])+','+str(int(EMDAT['Start Mont'].iloc[0]))+','+str(EMDAT_date_day) #Month is too long for .shp
    EMDAT_date = datetime.strptime(EMDAT_date, "%Y,%m,%d")        
    EMDAT_year = EMDAT['Start Year'].iloc[0] #.split('T')[0], "%Y-%m-%d").strftime('%Y')
           
    if EMDAT_affected_shape.empty != True: 
        DFO_match_list = []        
        DFO_match_nr_list = []
        DFO_match_time_dif_list = []
        DFO_duration_list = []  
        
        # Iterate over all DFO entries and check for spatial and temporal overlap    
        DFO_satellite_shape = gpd.GeoDataFrame()
        
        for DFO_temp_nr in range(len(DFO)):  
            DFO_temp_began = datetime.strptime(str(DFO.loc[DFO_temp_nr,'Began']), "%Y-%m-%d")
            DFO_temp_ended = datetime.strptime(str(DFO.loc[DFO_temp_nr,'Ended']), "%Y-%m-%d")
            DFO_temp_middle_year = (DFO_temp_began.date() + ((DFO_temp_ended-DFO_temp_began) / 2)).year 
    
            if abs((EMDAT_date - DFO_temp_began).days) <= max_day_difference:                
                DFO_match_nr = DFO.loc[DFO_temp_nr,'ID']
                DFO_ID = DFO_match_nr                
                DFO_satellite_shape_temp = gpd.read_file(f"{path_satellite_shape_files_final}DFO_{DFO_ID}_final_{DFO_temp_middle_year}.shp")                        
                DFO_satellite_shape_temp = DFO_satellite_shape_temp.buffer(0)                        
                DFO_satellite_shape_temp = gpd.GeoDataFrame(geometry=DFO_satellite_shape_temp)
                
                try:
                    DFO_satellite_shape_temp = gpd.overlay(EMDAT_affected_shape,DFO_satellite_shape_temp,how='intersection')
                    
                    if (EMDAT_affected_shape.unary_union).intersects(DFO_satellite_shape_temp.unary_union) == True:                                        
                        DFO_match_nr_temp_list.append(DFO_ID)
                        DFO_match_time_dif_temp_list.append(abs((EMDAT_date - DFO_temp_began).days))
                        DFO_middle_year_temp_list.append(DFO_temp_middle_year)
                        DFO_began_temp_list.append(DFO_temp_began)
                        DFO_end_temp_list.append(DFO_temp_ended)
                        DFO_duration_temp_list.append(abs((DFO_temp_began - DFO_temp_ended).days))
                                    
                except:
                    DFO_satellite_shape_temp = gpd.GeoDataFrame()
                    print('intersection not possible')
                    
        #%%
        print(DFO_match_nr_temp_list)
        print(DFO_match_time_dif_temp_list)
         
        # If overlap is present, follow matching procedure, see flowchart and text in the paper                   
        if len(DFO_match_nr_temp_list) > 1:
           print(DFO_match_nr_temp_list,DFO_match_time_dif_temp_list)
            
           DFO_match_nr_single_list = []
           DFO_match_time_dif_single_list = []
           DFO_duration_single_list = []
           
           print("Match list greater than 1")
           
           for j in range(len(DFO_match_nr_temp_list)):
           
               if DFO_match_time_dif_temp_list[j] <= 14:
                   
                   print("time dif less equal 14 d")
                   
                   print(DFO_match_time_dif_temp_list[j],DFO_match_nr_temp_list[j])
                   
                   DFO_satellite_shape_temp = gpd.read_file(f"{path_satellite_shape_files_final}DFO_{DFO_match_nr_temp_list[j]}_final_{DFO_middle_year_temp_list[j]}.shp")                        
                   DFO_satellite_shape_temp = DFO_satellite_shape_temp.buffer(0)                        
                   DFO_satellite_shape_temp = gpd.GeoDataFrame(geometry=DFO_satellite_shape_temp)
                   DFO_satellite_shape_temp = gpd.overlay(EMDAT_affected_shape,DFO_satellite_shape_temp,how='intersection')                                            
                   DFO_satellite_shape = DFO_satellite_shape.append(DFO_satellite_shape_temp)    
                   DFO_match_nr_single_list.append(DFO_match_nr_temp_list[j])
                   DFO_match_time_dif_single_list.append(DFO_match_time_dif_temp_list[j])
                   DFO_duration_single_list.append(DFO_duration_temp_list[j])   
                   DFO_match_counter += 1            
               
           if DFO_match_nr_single_list == []:
               
               print("time dif events only over 14 d")
                          
               DFO_time_dif_temp_list_min = np.min(DFO_match_time_dif_temp_list)
               
               print("min:",DFO_time_dif_temp_list_min)
               
               for j in range(len(DFO_match_nr_temp_list)):
               
                       if DFO_match_time_dif_temp_list[j] <= DFO_time_dif_temp_list_min:
                           
                           print("greater than 14 d and appended as min")
               
                           print(DFO_match_time_dif_temp_list[j],DFO_match_nr_temp_list[j])

                           DFO_satellite_shape_temp = gpd.read_file(f"{path_satellite_shape_files_final}DFO_{DFO_match_nr_temp_list[j]}_final_{DFO_middle_year_temp_list[j]}.shp")                        
                           DFO_satellite_shape_temp = DFO_satellite_shape_temp.buffer(0)                        
                           DFO_satellite_shape_temp = gpd.GeoDataFrame(geometry=DFO_satellite_shape_temp)
                           DFO_satellite_shape_temp = gpd.overlay(EMDAT_affected_shape,DFO_satellite_shape_temp,how='intersection')                                            
                           DFO_satellite_shape = DFO_satellite_shape.append(DFO_satellite_shape_temp) 
                           DFO_match_nr_single_list.append(DFO_match_nr_temp_list[j])
                           DFO_match_time_dif_single_list.append(DFO_match_time_dif_temp_list[j])
                           DFO_duration_single_list.append(DFO_duration_temp_list[j])   
                           DFO_match_counter += 1    

           matching_type = 2                      
           DFO_match_nr_list.append(DFO_match_nr_single_list)  
           DFO_match_time_dif_list.append(np.mean(DFO_match_time_dif_single_list))
           DFO_duration_list.append(np.mean(DFO_duration_single_list)) 
              
        elif len(DFO_match_nr_temp_list) == 1:                
            DFO_satellite_shape = gpd.read_file(f"{path_satellite_shape_files_final}DFO_{DFO_match_nr_temp_list[0]}_final_{DFO_middle_year_temp_list[0]}.shp") 
            DFO_satellite_shape = DFO_satellite_shape.buffer(0)                        
            DFO_satellite_shape = gpd.GeoDataFrame(geometry=DFO_satellite_shape)
            DFO_satellite_shape = gpd.overlay(EMDAT_affected_shape,DFO_satellite_shape,how='intersection')                 
            DFO_match_nr_list.append(DFO_match_nr_temp_list[0])
            DFO_match_time_dif_list.append(abs((EMDAT_date - DFO_began_temp_list[0]).days))
            DFO_duration_list.append(DFO_duration_temp_list[0])   
            DFO_match_counter += 1                      
            matching_type = 1
                                            
        #%%
        
        # Compute affected entities and socio-economic properties                
        if len(DFO_satellite_shape) > 0:   
            DFO_satellite_shape_area_list = [] 
            affected_GPW_sum_list = []
            affected_GPW_mean_list = []
            affected_GHSL_sum_list = []
            affected_GHSL_mean_list = []
            DFO_satellite_shape_pop_density_GHSL_list = [] 
            DFO_satellite_shape_pop_density_GPW_list = []
            forest_mean_DFO_satellite_shape_list = []  
            DFO_satellite_shape_area = DFO_satellite_shape['geometry'].to_crs({'proj':'cea'}) 
            print(DFO_satellite_shape_area.unary_union.area)
            DFO_satellite_shape_area = round((DFO_satellite_shape_area.unary_union.area) / (10**6),5) # in km2
            DFO_satellite_shape_area_list.append(DFO_satellite_shape_area)            
            DFO_satellite_shape = DFO_satellite_shape.unary_union
            DFO_match_nr = DFO.loc[DFO_temp_nr,'ID']      
            DFO_ID = DFO_match_nr
            DFO_match_time_dif = abs((EMDAT_date - DFO_temp_began).days)     
                
            # Affected people and pop density - GPW            
            stat = zonal_stats(DFO_satellite_shape, 
                f"{path_local}data/population/GPW_population_interpolated/gpw_population_{EMDAT_year}_30_sec.tif",
                all_touched = True, 
                stats = ['sum'])                           
            stat = pd.DataFrame(stat).sum()
            affected_GPW_sum_list.append(int(stat))
            DFO_satellite_shape_pop_density_GPW = int(stat)/(DFO_satellite_shape_area)     
            DFO_satellite_shape_pop_density_GPW_list.append(round(DFO_satellite_shape_pop_density_GPW,2))
            
            stat = zonal_stats(DFO_satellite_shape, 
                f"{path_local}data/population/GPW_population_interpolated/gpw_population_{EMDAT_year}_30_sec.tif",
                all_touched = True, 
                stats = ['mean'])                           
            stat = pd.DataFrame(stat).sum()
            affected_GPW_mean_list.append(int(stat))
            
            # Affected people and pop density - GHSL - 30 arc seconds            
            stat = zonal_stats(DFO_satellite_shape, 
                f"{path_local}data/population/GHSL_population_resampled_30_arcsec/ghsl_population_{EMDAT_year}_30_sec.tif",
                all_touched = True, 
                stats = ['sum'])                           
            stat = pd.DataFrame(stat).sum()
    
            try:
                affected_GHSL_sum_list.append(int(stat))
                DFO_satellite_shape_pop_density_GHSL = int(stat)/(DFO_satellite_shape_area)     
                DFO_satellite_shape_pop_density_GHSL_list.append(round(DFO_satellite_shape_pop_density_GHSL,2))
                                                                
            except:            
                affected_GHSL_sum_list.append(0)
                DFO_satellite_shape_pop_density_GHSL_list.append(0)
     
            stat = zonal_stats(DFO_satellite_shape, 
                f"{path_local}data/population/GHSL_population_resampled_30_arcsec/ghsl_population_{EMDAT_year}_30_sec.tif",
                all_touched = True, 
                stats = ['mean'])                           
            stat = pd.DataFrame(stat).sum()
            
            try:                               
                affected_GHSL_mean_list.append(int(stat))
                                                                
            except:            
                affected_GHSL_mean_list.append(0)
    
            # Iterate over all other attributes     
            
            affected_sum_dict = {
                "GDP_affected_sum":f"{path_local}data/gdp/kummu_etal/GDP/GDP_{EMDAT_year}.tif",
                "cable_affected_sum":f"{path_local}data/CISI/cable.tif",              
                "plant_affected_sum":f"{path_local}data/CISI/plant.tif",               
                "power_pole_affected_sum":f"{path_local}data/CISI/power_pole.tif",              
                "power_tower_affected_sum":f"{path_local}data/CISI/power_tower.tif",  
                "line_affected_sum":f"{path_local}data/CISI/line.tif",               
                "mast_affected_sum":f"{path_local}data/CISI/mast.tif",   
                "communication_tower_affected_sum":f"{path_local}data/CISI/communication_tower.tif",                
                "doctors_affected_sum":f"{path_local}data/CISI/doctors.tif",               
                "hospital_affected_sum":f"{path_local}data/CISI/hospital.tif",                            
                "pharmacy_affected_sum":f"{path_local}data/CISI/pharmacy.tif",                            
                "primary_road_affected_sum":f"{path_local}data/CISI/primary.tif",
                "tertiary_road_affected_sum":f"{path_local}data/CISI/tertiary.tif",
                "reservoir_affected_sum":f"{path_local}data/CISI/reservoir.tif",              
                "school_affected_sum":f"{path_local}data/CISI/school.tif",               
                "university_affected_sum":f"{path_local}data/CISI/university.tif"}
                        
            affected_mean_dict = {
                "GDP_affected_mean":f"{path_local}data/gdp/kummu_etal/GDP/GDP_{EMDAT_year}.tif",
                "education_affected_mean":f"{path_local}data/CISI/education.tif",              
                "energy_affected_mean":f"{path_local}data/CISI/energy.tif",              
                "health_affected_mean":f"{path_local}data/CISI/health.tif",              
                "telecommunication_affected_mean":f"{path_local}data/CISI/telecommunication.tif",              
                "transportation_affected_mean":f"{path_local}data/CISI/transportation.tif",              
                "water_affected_mean":f"{path_local}data/CISI/water.tif",  
                "CISI_global_affected_mean":f"{path_local}data/CISI/CISI_global.tif",
                "cable_affected_mean":f"{path_local}data/CISI/cable.tif",              
                "plant_affected_mean":f"{path_local}data/CISI/plant.tif",               
                "power_pole_affected_mean":f"{path_local}data/CISI/power_pole.tif",              
                "power_tower_affected_mean":f"{path_local}data/CISI/power_tower.tif",  
                "line_affected_mean":f"{path_local}data/CISI/line.tif",               
                "mast_affected_mean":f"{path_local}data/CISI/mast.tif",   
                "communication_tower_affected_mean":f"{path_local}data/CISI/communication_tower.tif",                
                "doctors_affected_mean":f"{path_local}data/CISI/doctors.tif",               
                "hospital_affected_mean":f"{path_local}data/CISI/hospital.tif",                            
                "pharmacy_affected_mean":f"{path_local}data/CISI/pharmacy.tif",                            
                "primary_road_affected_mean":f"{path_local}data/CISI/primary.tif",
                "tertiary_road_affected_mean":f"{path_local}data/CISI/tertiary.tif",
                "reservoir_affected_mean":f"{path_local}data/CISI/reservoir.tif",              
                "school_affected_mean":f"{path_local}data/CISI/school.tif",               
                "university_affected_mean":f"{path_local}data/CISI/university.tif",   
                "GDPpc_mean":f"{path_local}data/gdp/kummu_etal/GDPpc/GDPpc_{EMDAT_year}.tif",
                "HDI_mean":f"{path_local}data/gdp/kummu_etal/HDI/HDI_{EMDAT_year}.tif",
                "urbanization_mean":f"{path_local}data/landuse/urbanization/urbanization_{EMDAT_year}.tif",
                "landuse_total_mean":f"{path_local}data/landuse/landuse_total/landuse_total_{EMDAT_year}.tif",  
                "elevation_mean":f"{path_local}data/earthenv_topography/elevation_1KMmn_GMTEDmn.tif",                       
                "roughness_mean":f"{path_local}data/earthenv_topography/roughness_1KMmn_GMTEDmd.tif",                       
                "slope_mean":f"{path_local}data/earthenv_topography/slope_1KMmn_GMTEDmd.tif",  
                "female_mean":f"{path_local}data/demographic/female_perc.tif",               
                "pop_0_14_mean":f"{path_local}data/demographic/pop_0_14_perc.tif",               
                "pop_65_plus_mean":f"{path_local}data/demographic/pop_65_plus_perc.tif",               
                "FLOPROS_merged_mean":f"{path_local}data/FLOPROS/FLOPROS_merged.tif",                
                "FLOPROS_modeled_mean":f"{path_local}data/FLOPROS/FLOPROS_modeled.tif"}
            
            if affected_sum_list_len != len(affected_sum_dict) and affected_mean_list_len != len(affected_mean_dict):
                raise ValueError('Defined and actual length of the two dictionaries differ (one or both)')
                
            affected_sum_list = []
                            
            for variable_single in affected_sum_dict.items():            
                affected_sum_list.append(compute_affected(variable_single[1],'sum',DFO_satellite_shape))
            
            affected_mean_list = []
                
            for variable_single in affected_mean_dict.items():          
                affected_mean_list.append(compute_affected(variable_single[1],'mean',DFO_satellite_shape))

            # Forest Coverage            
            forest_area_list = []
            
            for file in os.listdir(f"{path_local}data/forests/resampled/"):                
                stat = zonal_stats(DFO_satellite_shape, 
                    f"{path_local}data/forests/resampled/"+file,
                    all_touched = True, 
                    stats = ['mean'])                           
            
                stat = pd.DataFrame(stat).mean()[0]
                                
                if stat >= 0:                
                    forest_area_list.append((stat/100))
            
            forest_area_average = round(np.mean(forest_area_list),5)
            forest_mean_DFO_satellite_shape_list.append(forest_area_average)                           

    DFO_match_list.append(DFO_match_counter)
    matching_type_list.append(matching_type)
    geometry_list.append(EMDAT_affected_shape.unary_union)
    
    if DFO_match_counter == 0:  
        DFO_match_nr_list = [np.nan]
        DFO_match_time_dif_list = [np.nan]
        DFO_duration_list = [np.nan]
        DFO_satellite_shape_area_list = [np.nan] 
        affected_GPW_sum_list = [np.nan]
        affected_GPW_mean_list = [np.nan]
        affected_GHSL_sum_list = [np.nan]
        affected_GHSL_mean_list = [np.nan]
        DFO_satellite_shape_pop_density_GHSL_list = [np.nan] 
        DFO_satellite_shape_pop_density_GPW_list = [np.nan]
        forest_mean_DFO_satellite_shape_list = [np.nan]    
    
    #%%
    
    print(DFO_match_nr_list)
    print(len(DFO_match_nr_list))
     
    # Construct FLODIS entry   
    EMDAT = pd.DataFrame(EMDAT)

    print(len(EMDAT))
    
    EMDAT['GFD_matches'] = DFO_match_list  
    EMDAT['GFD_matches_nr'] = DFO_match_nr_list  
    EMDAT['GFD_matches_time_dif'] = DFO_match_time_dif_list 
    EMDAT['GFD_duration'] = DFO_duration_list 
  #  EMDAT['DFO_satellite_shape_area'] = DFO_satellite_shape_area_list
    EMDAT['matching_type'] = matching_type_list
    EMDAT['pop_affected_sum_GHSL'] = affected_GHSL_sum_list 
    EMDAT['pop_affected_mean_GHSL'] = affected_GHSL_mean_list 
    EMDAT['pop_density_GHSL'] = DFO_satellite_shape_pop_density_GHSL_list 
    EMDAT['pop_affected_sum_GPW'] = affected_GPW_sum_list 
    EMDAT['pop_affected_mean_GPW'] = affected_GPW_mean_list 
    EMDAT['pop_density_GPW'] = DFO_satellite_shape_pop_density_GPW_list 
    
    for variable_single,variable_single_counter in zip(affected_sum_dict.items(),range(len(affected_sum_dict))):  
      #  print(affected_sum_list[variable_single_counter]) 
        if DFO_match_counter == 0:
            EMDAT[variable_single[0]] = [np.nan]
        else:
            EMDAT[variable_single[0]] = affected_sum_list[variable_single_counter]
    
    for variable_single,variable_single_counter in zip(affected_mean_dict.items(),range(len(affected_mean_dict))):  
       # print(affected_sum_list[variable_single_counter]) 
        if DFO_match_counter == 0:
            EMDAT[variable_single[0]] = [np.nan]
        else:
            EMDAT[variable_single[0]] = affected_mean_list[variable_single_counter]
            
    EMDAT['forest_cover_mean'] = forest_mean_DFO_satellite_shape_list 
    EMDAT['geometry'] = geometry_list
       
    #%%    
    
    # Save FLODIS entry to .csv    
    EMDAT.to_csv(f"{path_run}/results/EMDAT_single_results_{filename_temp_cut}.csv")
    
    #%%
    
    print('job succesfully completed!')
    
#%%

if __name__ == "__main__":
    main()
