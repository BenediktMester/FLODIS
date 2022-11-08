# FLODIS
FLODIS links estimates of flood-induced human displacements, fatalities, and economic damages to flooded areas observed through remote sensing.

The "FLODIS_datasets_output" folder contains the final FLODIS datasets for displacement, fatalities and damages. Additionally, geocoded IDMC data on displacement between 2008 and 2021 is provided, which can be linked with other hazard inventories.

The "scripts" folder consists of the following scripts:

- 01_IDMC_geolocation.ipynb
- 02_GDIS_EMDAT_information_merge.ipynb
- 03_GFD_preprocessing.py
- 04_socio_economic_indicators_preprocessing.ipynb
- 05_population_GPW_preprocessing.py
- 06_population_GHSL_preprocessing.py
- 07_demographic_preprocessing.py
- 08_FLODIS_IDMC_matching.py
- 09_FLODIS_EMDAT_matching.py
- 10_FLODIS_postprocessing.ipynb
- 11_plot_maps_stats.ipynb
- 12_technical_validation.ipynb

Short description of the scripts:

- 01 is used to identify subnational information in the IDMC displacement databank, and link it with the GADM dataset
- 02 links GDIS (geolocated EM-DAT) with the disaster information of EM-DAT
- 03, 04, 05, 06, and 07 preprocess all other datasets used as input
- 08 and 09 contain the matching process between the disaster databanks (IDMC/EM-DAT) and flood extent from GFD
- 10 cleans the data, and merges disaster entries, if matched with the same GFD flood
- 11 and 12 create all maps, and statistics used in the main manuscript

Additional information

- Linked EM-DAT variables:

['Start Year', 'Start Month', 'Start Day', 'End Year', 'End Month',
       'End Day', 'Total Deaths', 'No Injured', 'No Affected', 'No Homeless',
       'Total Affected',"Total Damages ('000 US$)"]
