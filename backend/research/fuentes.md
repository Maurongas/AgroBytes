# Fuentes de datos — texto extraído

Generado por `extraer_links.py` el 2026-11-14 11:43. ✅ 26 con contenido · ⚠️ 4 con poco texto · ❌ 2 con error.

> Texto copiado automáticamente de sitios externos: puede contener menús o restos de navegación.

## Índice

- ✅ [Soil Moisture Active Passive (SMAP)](#soil-moisture-active-passive-smap)
- ✅ [Global Precipitation Measurement (GPM) & IMERG](#global-precipitation-measurement-gpm-imerg)
- ✅ [Landsat](#landsat)
- ✅ [MODIS](#modis)
- ⚠️ [VIIRS](#viirs)
- ✅ [NASA POWER](#nasa-power)
- ✅ [Shuttle Radar Topography Mission (SRTM)](#shuttle-radar-topography-mission-srtm)
- ✅ [ECOSTRESS](#ecostress)
- ✅ [USDA Ag Data Commons](#usda-ag-data-commons)
- ✅ [Web Soil Survey (WSS)](#web-soil-survey-wss)
- ❌ [Cropland Data Layer (CDL): CropScape](#cropland-data-layer-cdl-cropscape)
- ❌ [PRISM Climate Data](#prism-climate-data)
- ✅ [USDA NRCS SSURGO/STATSGO2](#usda-nrcs-ssurgo-statsgo2)
- ⚠️ [National Agriculture Imagery Program (NAIP)](#national-agriculture-imagery-program-naip)
- ✅ [USGS National Land Cover Database (NLCD)](#usgs-national-land-cover-database-nlcd)
- ✅ [NLDAS/GLDAS: Land Data Assimilation Systems](#nldas-gldas-land-data-assimilation-systems)
- ⚠️ [FAO Global Agro-Ecological Zones (GAEZ)](#fao-global-agro-ecological-zones-gaez)
- ⚠️ [CoCoRaHS](#cocorahs)
- ✅ [USGS National Water Information Systems (NWIS)](#usgs-national-water-information-systems-nwis)
- ✅ [USDA AMS Market News](#usda-ams-market-news)
- ✅ [USDA NASS QuickStats](#usda-nass-quickstats)
- ✅ [OpenET](#openet)
- ✅ [USFS LANDFIRE](#usfs-landfire)
- ✅ [Global Ecosystem Dynamics Investigation (GEDI)](#global-ecosystem-dynamics-investigation-gedi)
- ✅ [Copernicus Sentinel-2: ESA](#copernicus-sentinel-2-esa)
- ✅ [ERA5: ECMWF Reanalysis](#era5-ecmwf-reanalysis)
- ✅ [NASA POWER · API Overview](#nasa-power-api-overview)
- ✅ [NASA POWER · Daily API](#nasa-power-daily-api)
- ✅ [NASA POWER · Climatology API](#nasa-power-climatology-api)
- ✅ [NASA POWER · Tutorial API](#nasa-power-tutorial-api)
- ✅ [NASA POWER · Methodology](#nasa-power-methodology)
- ✅ [NASA POWER · Application APIs](#nasa-power-application-apis)

---

## Soil Moisture Active Passive (SMAP)

- **URL:** https://www.earthdata.nasa.gov/data/platforms/space-based-platforms/smap
- **Título de la página:** Soil Moisture Active Passive (SMAP) | NASA Earthdata
- **Para qué sirve (según la lista):** Proporciona mediciones globales de humedad superficial del suelo y estados de congelación/descongelación cada 2–3 días para identificar estrés por sequía y disponibilidad de agua.

Skip to main content

Earthdata Forum is down due to unplanned maintenance. Please contact earthdata-support@nasa.gov with questions. See the alert

Suomi NPP is no longer delivering new data. Users must transition to alternative products. Suomi NPP data announcement

The Soil Moisture Active-Passive (SMAP) platform measures surface soil moisture and freeze-thaw state. These direct measurements improve our understanding of regional water cycles, ecosystem productivity, and processes that link the water, energy, and carbon cycles. Soil moisture information at high resolution enables improvements in weather, flood, and drought forecasts, and predictions of agricultural productivity and climate change.

SMAP measures surface soil conditions everywhere on Earth every two to three days, distinguishing between ground that is frozen or thawed. In ground that is not frozen or covered in water, SMAP measures how much water is in the top layer of soil. This data is used to produce global maps of soil moisture.

Learn more about SMAP

#### Data

209 Datasets

View Data and Tools

View data alert history

#### Type

Earth Observation Satellite

#### Objective

Measure global soil moisture, create global soil moisture maps, and determine the freeze or thaw state of the same area being mapped

#### Launch

January 31, 2015

#### Data Center

ASF DAAC

NSIDC DAAC

PO.DAAC

Remote video URL

This animation of sea surface salinity spans from April 1, 2015, to Aug. 27, 2024, based on the 8-day running mean version 6.0 Level 3 SMAP dataset from Remote Sensing Systems (RSS). Credit: PO.DAAC

| Short Name | Description | Gridding (km) | Latency* | ATBD** | Product Spec Doc | Source

| L1A_Radar | Raw radar data in time order (half orbit) | – | 12 hrs | n/a | View | ASF

| L1A_Radiometer | Radiometer raw data in time order | – | 12 hrs | n/a |   | NSIDC

| L1B_S0_LoRes | Low-resolution radar σ ο in time order (half orbit) | 5×30 | 12 hrs | View | View | ASF

|   | Backscatter analysis document

| L1B_TB | Radiometer TB in time order | 36×47 | 12 hrs | View |   | NSIDC

| L1C_S0_HiRes | High-resolution radar σ ο (half orbit gridded) | 1 | 12 hrs | View | View | ASF

|   | Backscatter analysis document | (1-3)***

| L1C_TB | Radiometer T B (half orbit, gridded) | 36 | 12 hrs | View |   | NSIDC

| L2_SM_A | Soil moisture (radar, half orbit) | 3 | 24 hrs | View |   | NSIDC

| L2_SM_P | Soil moisture (radiometer, half orbit) | 36 | 24 hrs | View |   | NSIDC

| L2_SM_A/P | Soil moisture (radar/radiometer, half orbit) | 9 | 24 hrs | View |   | NSIDC

| L3_F/T_A | Freeze-thaw state (radar, daily composite) | 3 | 50 hrs | View |   | NSIDC

| L3_SM_A | Soil moisture (radar, daily composite) | 3 | 50 hrs | View |   | NSIDC

| L3_SM_P | Soil moisture (radiometer, daily composite) | 36 | 50 hrs | View |   | NSIDC

| L3_SM_A/P | Soil moisture (radar/radiometer, daily composite) | 9 | 50 hrs | View |   | NSIDC

| L4_SM | Soil moisture (surface and root zone) | 9 | 7 days | View |   | NSIDC

| L4_C | Carbon net ecosystem exchange (NEE) | 9 | 14 days | View |   | NSIDC

SMAP is a remote-sensing observatory with two instruments — a synthetic aperture radar (SAR) and a radiometer — that map soil moisture and determine the freeze or thaw state of the area being mapped. Both instruments help map soil-moisture content, and unique properties of SAR enable the freeze-thaw mapping. Externally, the instruments share a common, 20-foot mesh antenna and a feed assembly. Inside the spacecraft, their electronics differ. When combined, the SMAP radar and radiometer deliver high-accuracy, high-resolution global maps of the Earth’s soil moisture and freeze-thaw state.

The radar actively sends pulses of radio waves down to a spot on Earth and measures the echo that returns microseconds later. The strength and “shape” of the echoes can be interpreted to indicate the moisture level of the soil, even through moderate levels of vegetation. The radiometer passively detects radio waves emitted by the ground from the same small area. The strength of the emission indicates temperatures.

The SMAP orbit is a 685-km altitude, near-polar, sun-synchronous, 6 a.m. / 6 p.m., eight-day, exact-repeat, frozen orbit.

- Near-polar orbit provides global land coverage up to high latitudes including all freeze-thaw regions of interest.
- Sun-synchrony provides observations of the surface close to the same local solar time each orbit throughout the mission, enhancing change-detection algorithms and scientific accuracy.
- Consistent 6 a.m. observation time is optimal because it minimizes the effect of Faraday rotation and impact on S/C design.
- Frozen orbit provides minimal altitude variation during an orbit, benefitting radar design and accuracy.
- 685-km altitude is an exact 8-day repeat orbit, advantageous for radar change-detection algorithms.
- Orbit provides optimum coverage of global land area at 3-day average intervals, and coverage of land region above 45N at 2-day average intervals.

Low-rate radiometer data and low-resolution radar data will be acquired continuously over fore and aft portions of the scan (full 360 degrees), as well as ascending and descending portions of the orbit.

High-resolution radar data will be acquired to include at a minimum:

- 360 degrees of the antenna scan (fore and aft looks) for the morning (6 a.m. equator crossing) half-orbit over the global land region (excluding the Antarctic)
- 180 degrees of the antenna scan (fore look) for the evening (6 p.m. equator crossing) half-orbit over the boreal land region (north of 45 degrees N latitude)
- 180 degrees of the antenna scan (fore look) for the morning half-orbit over the coastal ocean region (within 1,000 km of continental boundaries)
- The Science Operations Phase (SOP) begins after completion of the 90-day post-launch, in-orbit commissioning and lasts for three years. The first part of the SOP is the Calibration and Validation (Cal/Val) phase, which lasts for 12 months. Following the Cal/Val phase is the Routine Observations Phase (ROP), which lasts for 24 months.

##### Current Dataset Versions

- JPL SMAP-SSS CAP V5.0 ATBD, Validation and Users Guide (.pdf)
- RSS SMAP-SSS V5.0 ATBD, Validation Analysis and Data Users Guide (.pdf)

##### Prior Dataset Versions

- RSS SMAP-SSS V4.0 ATBD, Validation Analysis and Data Users Guide (.pdf)
- RSS SMAP-SSS V3.0 ATBD, Validation Analysis and Data Users Guide (.pdf)
- RSS SMAP-SSS V2.0 ATBD, Validation Analysis and Data Users Guide (.pdf)
- Release notes for RSS SMAP-SSS V2.0 70km datasets (.pdf)
- JPL SMAP-SSS CAP V4.3 ATBD, Validation and Users Guide (.pdf)
- JPL SMAP-SSS CAP V3.0 ATBD, Validation and Users Guide (.pdf)

##### Other Technical Documents

- NASA SMAP Handbook
- NASA Salinity Dielectric Constant Documentation and Data
- Remote Sensing Systems SMAP Version 5 (V5) Level 2C science-grade processing algorithm for SSS retrievals

##### Known Issues

- SMAP Radar Failure (July 7, 2015)
- Data Outages & Issues

#### Instruments Aboard SMAP

| Instrument Name  | Operational Date(s)  | Spectral Resolution  | Type of Instrument

|  Soil Moisture Active Passive L-Band Radar (SMAP L-Band Radar)   | January 31, 2015-July 7, 2015   |    | Imaging Radar

|  Soil Moisture Active Passive L-Band Radiometer (SMAP L-Band Radiometer)   | January 31, 2015 - present   |    | Spectrometer/Radiometer

#### Get Help

QUESTIONS & SUPPORT

Have a question?

Get help with NASA Earth science data, datasets, tools, services, and metadata on the Earthdata Forum. Experienced staff in the data user community review and answer questions.
Get help on Earthdata Forum

Earthdata
Forum

---

## Global Precipitation Measurement (GPM) & IMERG

- **URL:** https://gpm.nasa.gov/data
- **Título de la página:** Data | NASA Global Precipitation Measurement Mission
- **Para qué sirve (según la lista):** Ofrece estimaciones globales de tasas y acumulación de precipitación para evaluar la confiabilidad de las lluvias, tormentas extremas y riesgo de erosión.

Skip to main content

-  Home
-  Data

####  Data

Thursday, September 13, 2018

Precipitation data from the GPM and TRMM missions are made available free to the public in a variety of formats from several sources at NASA Goddard Space Flight Center. This section outlines the different types of data available, the levels of processing, the sources to download the data, and some helpful tips for utilizing precipitation data in your research.

##### Beginner Resources

###### Training

###### Tutorials

###### Data Visualization

###### Data FAQ

###### Learn about IMERG

Sections

#### GPM Data Resources

###### Data Directory (Downloads & Documentation)

###### Data Usage Policy

###### NASA Precipitation Processing System

###### Ground Validation Data

######

##### Frequently Asked Questions

How do I get precipitation data for my specific location?

There are several sources for downloading and viewing data which allow you to subset the data to only include specific parameters and/or geographic locations. These include the GES DISC, Giovanni and STORM. In Giovanni you can obtain data for a specific country, U.S. state, or watershed by using the "Show Shapes" option in the "Select Region" pane.

What happened to the TRMM Multi-satellite Precipitation Analysis (TMPA / 3B4x) data products?

The TRMM satellilte has been decommissioned and stopped collecting data in April 2015. The transition from the Tropical Rainfall Measuring Mission (TRMM) data products to the Global Precipitation Measurement (GPM) mission products has completed as of August 2019. The GPM IMERG dataset now includes TRMM-era data from June 2000 to the present, and other TRMM-era data has been reprocessed with GPM-era algorithms and is now available on the GPM FTP servers. TMPA data production ended as of December 31st, 2019 and the TRMMOpen FTP server has been shut down. Historical TMPA data is still available to download from the NASA GES DISC at: https://disc.gsfc.nasa.gov/datasets?keywords=TMPA&page=1

Click here for more details on the transition from TMPA to IMERG.

Am I allowed to use GPM data for my research?

Yes, in line with NASA's general data policy. Please refer to the GPM Data Policy for further details.

How do I give credit for using GPM data?

The data set source should be acknowledged when the data are used. One standard format for a formal reference is:

Dataset authors/producers, data release date: Dataset title, version. Data archive/distributor, access date in standard AMS format, data locator/identifier (doi or URL).

For example:

G.J. Huffman, D.T. Bolvin, R. Joyce, E.J. Nelkin, J. Tan, D. Braithwaite, K. Hsu, O.A. Kelley, P. Nguyen, S. Sorooshian, D.C. Watters, B.J. West, P. Xie, 2023: Integrated Multi-satellitE Retrievals for GPM (IMERG), version 07. NASA's Precipitation Processing Center, accessed 6 April 2026, https://arthurhouhttps.pps.eosdis.nasa.gov/gpmdata/

For more details on citation format, please refer to the American Meteorological Society Data Archiving and Citation guidelines: http://www2.ametsoc.org/ams/index.cfm/publications/authors/journal-and-…

Where can I find detailed documentation on the precipitation algorithms?

Browse our directory of GPM data products (https://gpm.nasa.gov/data/directory) to locate your desired algorithm, then click on the links in the algorithm description under "Documentation". All documentation is also available at the Precipitation Processing System website (https://pps.gsfc.nasa.gov/). Note that "GPM data products" includes data from both the GPM and TRMM eras, uniformly processed using the most current GPM-based algorithms.

What is the spatial and temporal resolution of GPM data?

The resolution of Level 0, 1, and 2 data is determined by the footprint size and observation interval of the sensors involved. Level 3 products are given a grid spacing that is driven by the typical footprint size of the input data sets.

For our popular multi-satellite GPM IMERG data products, the spatial resolution is 0.1° x 0.1° (or roughly 10km x 10km) with a 30 minute temporal resolution.

Visit the directory of GPM & TRMM data products for details on the resolution of each specific products.

Can I use images or videos from this site or other NASA websites?

For questions about permission for using NASA images and videos, please refer to NASA's official Media Usage Guidelines. For questions about specific images, please call 202-358-1900. For questions about specific video, please call 202-358-0309

Is it possible to subset GPM data?

What is the difference between "Near Real-time" (NRT) and "Production" / "Research" data?

GPM data products can be divided into two groups (near real-time and production) depending on how soon they are created after the satellite collects the observations. For applications such as weather, flood, and crop forecasting that need precipitation estimates as soon as possible, near real-time data products are most appropriate. For all other applications, production data products are generally the best data sets to use because additional or improved inputs are used to increase accuracy. These other inputs are only made available several days, or in some cases, several months, after the satellite observations are taken, and the production data sets are computed after all data have arrived, making possible a more careful analysis.

For the GPM IMERG dataset, IMERG Early and Late Runs are the near real-time products, while IMERG Final Run is the research / production product.

View the full list of frequently asked questions.

####

##### Data News

Wednesday, August 19, 2026

##### New WSF-M1 MWI NRT Files Available

Effective August 12, 2026 PPS made available NRT data from the DOD WSF-M1 MWI instrument. Both intercalibrated 1C granules and GPROF precipitation retrieval files are available to users. The WSF NRT granules are about 15 mins long. Some are shorter because of the way they are delivered to NRT. Please note that 1C granules are not the same as the DOD provided SDR product that provide the basis for the intercalibration. 1C products have fewer parameters in them than the original SDR. Only those needed for the precipitation retrieval are included. NOAA is the official distributor of the WSF SDR...

Thursday, August 6, 2026

##### Update to the IMERG V08 Transition Schedule, Aug. 2026

This is an update to the IMERG V08 transition schedule posted on April 28, 2026, at https://gpm.nasa.gov/data/news/imerg-v08-transition-schedule. At this moment, the IMERG development team is still waiting for V08 of one of the parent products to IMERG to be finalized. Until this parent product becomes available, the team cannot assess its full impact on IMERG V08 and move towards a complete reprocessing of the record starting 1998. Therefore, at this stage, it seems more likely that IMERG V08 Final Run will be released in the fall of 2026, though this projection assumes that the parent...

Tuesday, April 28, 2026

##### IMERG V08 Transition Schedule

For the Final Run, the V07 record ends in September 2025 because the parent products feeding into the IMERG algorithm (CORRA and GPROF) are being upgraded to V08. If processing were to go beyond September, the Final record would have to use V08 inputs instead of V07 inputs. Since the IMERG V07 code is configured with the expectation of V07 inputs, this would introduce potential discontinuities in the Final record. The IMERG V08 Final Run is planned for release in the summer of 2026, though this timeline assumes that V08 of the parent products behaves within expected bounds. When this release...

Thursday, January 8, 2026

##### Upcoming GPM Near Real-time Maintenance

On Tuesday, 20 January 2026, NASA's Precipitation Processing System (PPS) will temporarily shutdown the GPM Near Real-time (NRT) system at 18:00 EST (23:00 UTC). This is necessary to complete the move of data from the current high-speed storage system (not currently under maintenance) to the new storage system that is under maintenance. It will take approximately 14 hours to finalize the synchronization of the data from the old storage to the new one. During this 14 hours no new data will be produced or ingested. While user access to the file server (jsimpson.pps.eosdis.nasa.gov and...

Wednesday, July 30, 2025

##### SSMIS Data Collection to Continue into 2026

Department of Defense officials have reached an agreement to continue sharing DMSP SSMIS data until the sensor fails, or until the program formally ends (currently planned for September 2026). This decision puts off for now the impacts that the previously announced SSMIS shutdown would have had on the IMERG product.

Related Articles

#####  Global Precipitation During July to September of the 2026-27 El Niño

Monday, October 12, 2026

El Niño events occur every two to seven years, and they are driven by feedback between ocean currents and the circulation of the atmosphere over the tropical Pacific Ocean. Variation in ocean temperature and wind patterns drives variation in the rain and snow that falls over the tropical Pacific and elsewhere in the world. Many forecasts have been issued for the El Niño that started in the summer of 2026, and past El Niños have been extensively discussed during the months leading up to this one. One way that NASA contributes to the conversation is to provide, in near real time, estimates of
Read More

#####  Oscillations in Global Precipitation

Wednesday, August 5, 2026

Whether or not it rains a week from now where you live may seem mostly random, but a long enough data record will likely reveal rainfall patterns that repeat over hours, months, or years. Atmospheric scientists describe some of these repeating patterns as cycles and others as oscillations. There are annual and daily precipitation cycles tied to the variation of the sun's path across the sky [1]. An example of precipitation affected by time of day is that summer thunderstorms occur predominantly in afternoon or early evening along the East Coast of the United States. An example of seasonal

#####  Natural Cycles in Global Precipitation

Friday, March 27, 2026

In many places, the amount of that rain falls on a particular day or hour is influenced by multiple natural cycles that exist simultaneously on different time scales. One such cycle repeats every 24 hours, and another repeats every year. The global extent of these cycles can be studied using NASA's IMERG precipitation estimates that have been generated for 1998 to the present. Most of Earth's precipitation falls as rain, and the rest falls as snow, hail, or other forms of precipitation. The length of IMERG's data record makes it possible to average out some of the random error and unrelated

#####  27 Years of Global Rainfall at Your Fingertips

Thursday, July 24, 2025

NASA's Worldview website now allows you to explore global estimates of rainfall and snowfall from 1998 to the present at 30-minute intervals. Researchers and application developers have been using this dataset since 2014 (Portier 2024; Portier et al. 2023), but now it is also available as images in Worldview.

#####  Explore 20 Years of Rain and Snowfall Data from NASA’s Precipitation Missions

Wednesday, September 9, 2020

A new data product merges data from the Tropical Rainfall Measuring Mission (TRMM) and the Global Precipitation Measurement (GPM) mission, giving meteorologists and researchers access to a 20-year precipitation record. How much rain and snow fall on Earth in any given year? NASA scientists are answering this question more accurately than ever before and observing precipitation in the most remote places on Earth. And it’s all thanks to an international constellation of satellites. At any given time, instruments onboard about a dozen satellites contribute to a record of the world’s rain and snow

#####  Using the IMERG Long-term Precipitation Dataset for Applications

Thursday, October 17, 2019

A long precipitation data set like the new GPM IMERG V06 product is valuable for many applications and for decision-making. Accurate and reliable precipitation records are not only crucial to understanding trends and variability but also for water management resources and food security, ecological management, and weather, climate and hydrological forecasting. Here we present a few highlights showcasing how GPM IMERG is helping a variety of end users make decisions that will benefit society for years to come. GPM IMERG Data Used for Wind Energy Map of average precipitation in north-central...

#####  The Art of Creating Digital Hurricanes

Wednesday, May 25, 2016

Every day, scientists at NASA work on creating better hurricanes – on a computer screen. At NASA’s Goddard Space Flight Center in Greenbelt, Maryland, a team of scientists spends its days incorporating millions of atmospheric observations, sophisticated graphic tools and lines of computer code to create computer models simulating the weather and climate conditions responsible for hurricanes. Scientists use these models to study the complex environment and structure of tropical storms and hurricanes. Getting the simulations right has huge societal implications, which is why one Goddard...

#####  The Evolution of NASA Precipitation Data

Tuesday, September 29, 2015

NASA’s global precipitation data and data processing systems have come a long way from the launch of TRMM in 1997 to the ongoing GPM mission. Just before midnight Eastern Daylight Time on June 15, 2015, a fireball appeared over central Africa, streaked across Madagascar, and tracked across the uninhabited Southern Indian Ocean. This was the fiery end of the joint NASA/Japan Aerospace Exploration Agency (JAXA) Tropical Rainfall Measuring Mission (TRMM). TRMM’s homecoming after more than 17 years in orbit also marked the end of the first major satellite mission specifically designed to gather...

#####  GPM's First Global Rainfall and Snowfall Map

Thursday, March 12, 2015

The Global Precipitation Measurement mission has produced its first global map of rainfall and snowfall. Like a lead violin tuning an orchestra, the GPM Core Observatory – launched one year ago on Feb. 27, 2014, as a collaboration between NASA and the Japan Aerospace Exploration Agency – acts as the standard to unify precipitation measurements from a network of 12 satellites. The result is NASA's Integrated Multi-satellite Retrievals for GPM data product, called IMERG, which combines all of these data from 12 satellites into a single, seamless map. The map covers more of the globe than any...

#####  GPM's How-to Guide for Global Rain Maps

Thursday, September 4, 2014

In a data-processing room at NASA’s Goddard Space Flight Center in Greenbelt, Maryland, racks of high-powered computers are making a set of maps. They're not the familiar satellite map of farms, forests and cities. Instead, the maps will show what's in the atmosphere above the ground -- falling rain and snow. The data come from the Global Precipitation Measurement mission, an international partnership led by NASA and the Japan Aerospace Exploration Agency. The GPM Core Observatory launched on Feb. 27, 2014, and after an initial check-out period, began its prime mission on May 29. The data...

Hide Body

Hide Date

---

## Landsat

- **URL:** https://earthexplorer.usgs.gov/
- **Título de la página:** EarthExplorer
- **Para qué sirve (según la lista):** Proveen reflectancia corregida, índices de vegetación (como NDVI) e indicadores de estrés vegetal, suelo desnudo y cambios estacionales a distintas resoluciones espaciales.

Official websites use .gov

A .gov website belongs to an official government organization in the United States.

Secure .gov websites use HTTPS

A lock (  ) or https:// means you’ve safely connected to the .gov website. Share sensitive information only on official, secure websites.

Search Criteria

Data Sets

Additional Criteria

Results

##### 1. Enter Search Criteria

To narrow your search area: type in an address or place name, enter coordinates or click the map to define your search area (for advanced map tools, view the help documentation), and/or choose a date range.

Geocoder

GeoJSON/KML/Shapefile Upload

Select a Geocoding Method

Set WRS Type Point  Polygon

Type:  Path:  Row:

Search Limits: The search result limit is 100 records; select a Country, Feature Class, and/or Feature Type to reduce your chances of exceeding this limit.
Feature Type US Features  World Features
Feature Name   State  Feature Type    Country  Feature Class  Feature Type

Click on an Address/Place to show the location on the map and add coordinates to the Area of Interest Control.

| Num  | Address/Place  | Latitude  | Longitude

Click on a Feature to show the location on the map and add coordinates to the Area of Interest Control.

| Placename  | Type  | Region  | Latitude  | Longitude

You must be logged in to upload a file.

Type

Cal/Val Site

Polygon

Circle

Predefined Area

Coordinates Format Degree/Minute/Second  Decimal

-   No coordinates selected.

Circular polygons are created using a center point defined by decimal latitude and longitude values and a radius.

Center Latitude:

Radius:

Center Longitude:

No shape loaded.

Date Range

Cloud Cover

Result Options

Search from:   to:

Search months:

(all)

Cloud Cover Range:

Unknown Cloud Cover Values
This filter will only be applied to data sets that support cloud cover filtering ( in the data set list denotes cloud cover support).

Search Type Standard Search

Results per Page:

Mass Media Searches are not limited by number of results or size; however, Mass Media Orders in excess of 6 terabytes will require extra processing time and justification.

Latitude

Longitude

Latitude:

°  '  "

Longitude:

##### 2. Select Your Data Set(s)

Check the boxes for the data set(s) you want to search. When done selecting data set(s), click the Additional Criteria or Results buttons below. Click the plus sign next to the category name to show a list of data sets.

Use Data Set Prefilter (What's This?)
0 data sets out of 0 were hidden by the prefilter (Show).

Data Set Search:

Please wait while the Data Sets are loaded.

##### 3. Additional Criteria (Optional)

If you have more than one data sets selected, use the dropdown to select the additional criteria for each data set.

Data Sets:

Additional criteria filters are cached for performance. If you are not seeing an expected filter option, click here to refresh.
Please wait while the additional criteria form is loaded.

##### 4. Search Results

If you selected more than one data set to search, use the dropdown to see the search results for each specific data set.

Note: You must be logged in to download and order scenes

|   |

Search Criteria Summary (Show)

Clear Search Criteria

#### You are searching the following data sets:

- No data sets selected.

#### Your area of interest:

- No coordinates selected.

#### You are searching using the following criteria:

- Start Date: None
- End Date: None
- Months: (all)

(coordinates)

Options

Basemaps are for reference only and cannot be downloaded. Some non-USGS layers may not reflect current naming conventions. Use the left-side options to access available data.

---

## MODIS

- **URL:** https://lpdaac.usgs.gov/products/
- **Redirige a:** https://www.earthdata.nasa.gov/centers/lp-daac
- **Título de la página:** Land Processes Distributed Active Archive Center | NASA Earthdata
- **Para qué sirve (según la lista):** Proveen reflectancia corregida, índices de vegetación (como NDVI) e indicadores de estrés vegetal, suelo desnudo y cambios estacionales a distintas resoluciones espaciales.

Skip to main content

Earthdata Forum is down due to unplanned maintenance. Please contact earthdata-support@nasa.gov with questions. See the alert

Suomi NPP is no longer delivering new data. Users must transition to alternative products. Suomi NPP data announcement

### LP DAAC

Land Processes Distributed Active Archive Center

The Land Processes Distributed Active Archive Center (LP DAAC) operates as a partnership between the United States Geological Survey (USGS) and the National Aeronautics and Space Administration (NASA) dedicated to enabling natural resource managers, disaster responders, academia, and industry to investigate, characterize, and monitor land surface processes. By providing access to trusted, well-documented earth science datasets at no cost, LP DAAC supports a large community of users across science applications ranging from agriculture and geology to urban heat and wildfire mitigation.

LP DAAC processes, archives, and distributes more than 14 petabytes of land remote sensing data from major missions such as  Advanced Spaceborne Thermal Emission and Reflection Radiometer (ASTER), Moderate Resolution Imaging Spectroradiometer (MODIS), and Visible Infrared Imaging Radiometer Suite (VIIRS), ECOsystem Spaceborne Thermal Radiometer Experiment on Space Station (ECOSTRESS), Global Ecosystem Dynamics Investigation (GEDI), Earth surface Mineral dust source InvesTigation (EMIT), and Harmonized Landsat Sentinel-2, (HLS). Users may obtain all data products distributed by LP DAAC by using Earthdata Search or the many customized data tools.

In addition to archiving and distributing data, LP DAAC also provides resources like Python Jupyter notebooks through the LPDAAC Data Resources GitHub, and convenient data transformation tools like the Application for Extracting and Exploring Analysis Ready Samples (AppEEARS). AppEEARS allows users to conduct point and area sub-setting of popular geospatial datasets from the LP DAAC and other federal archives.

#### Data

1145 Datasets

View Data and Tools

View data alert history

#### Location

Sioux Falls, SD

#### Manager

Ryan Reker (Acting)
View All People

#### Founded

1990

#### Partners

USGS Earth Resources Observation and Science (EROS) Center

NASA's Earth Observing System (EOS) program comprises a series of polar-orbiting and low-inclination satellites designed to monitor and understand Earth systems through long-term global observations. LP DAAC archives data for a number of EOS missions.

##### MODIS

The Moderate Resolution Imaging Spectroradiometer (MODIS) instrument is operating aboard both the Terra and Aqua spacecraft. It views the entire surface of the Earth every one to two days. MODIS data contribute to a range of land and water application areas including wildfire monitoring, temperature and emissivity changes, land surface change, vegetation and ecosystem dynamics, natural disasters, and agriculture studies. View a list of MODIS products archived by LP DAAC.

##### ASTER

Advanced Spaceborne Thermal Emission and Reflection Radiometer (ASTER) data contribute to a wide array of global change-related application areas including vegetation and ecosystem dynamics, hazard monitoring, geology and soils, hydrology, and land cover change. The ASTER instrument is aboard the Terra satellite and is taskable and able to be scheduled for on-demand data acquisition requests. View a list of ASTER products archived by LP DAAC.

Users who rely on ASTER for applications that require ongoing observations are encouraged to begin transitioning their workflows to alternative data sources to ensure continuity into the future. Please see the ASTER Transition Resources page for additional information.

##### VIIRS

The Visible Infrared Imaging Radiometer Suite (VIIRS) is aboard the NASA/NOAA Suomi National Polar-orbiting Partnership (Suomi NPP), NOAA-20, and NOAA-21 satellites. VIIRS observes the entire Earth’s surface twice each day, once during the day and once at night. VIIRS data contribute to a range of land and water application areas including wildfire monitoring, temperature and emissivity changes, land surface change, vegetation and ecosystem dynamics, natural disasters, and agriculture studies. Generated in a similar format to the Moderate Resolution Imaging Spectroradiometer (MODIS), VIIRS data products aim to provide continuity with the MODIS mission. View a list of VIIRS products archived by LP DAAC.

Suomi NPP VIIRS data acquisitions ceased on November 2, 2026 (2026/305). Suomi NPP VIIRS data users should transition to the NOAA-21 (primary) and NOAA-20 (secondary) data products listed in the Suomi NPP VIIRS Land Data Transition Table.

##### ECOSTRESS

Principal Investigator: Simon Hook, NASA/Caltech Jet Propulsion Laboratory

The ECOsystem Spaceborne Thermal Radiometer Experiment on Space Station (ECOSTRESS) is aboard the International Space Station (ISS) and measures the temperature of plants to better understand how much water plants need and how they respond to stress. ECOSTRESS addresses three overarching science questions: How is the terrestrial biosphere responding to changes in water availability? How do changes in diurnal vegetation water stress impact the global carbon cycle? Can agricultural vulnerability be reduced through advanced monitoring of agricultural water consumptive use and improved drought estimation? ECOSTRESS uses a multispectral thermal infrared radiometer to measure the surface temperature. The radiometer obtains detailed images of the Earth’s surface that can provide information on the temperature of an individual farmer’s field. View a list of ECOSTRESS products archived by LP DAAC.

##### EMIT

Principal Investigator: Robert O. Green, NASA Jet Propulsion Laboratory

The Earth Surface Mineral Dust Source Investigation (EMIT) instrument aboard the International Space Station (ISS) measures visible to short-wave infrared (VSWIR) wavelengths of the surface mineralogy of arid dust source regions via imaging spectroscopy. The data collected by the EMIT instrument will be used to map relative abundance of source minerals to advance our understanding of the current and future role of mineral dust in the radiative forcing (warming or cooling) of the atmosphere. View a list of EMIT products archived by LP DAAC.

##### GEDI

Principal Investigator: Ralph Dubayah, University of Maryland

The Global Ecosystem Dynamics Investigation (GEDI) is a full-waveform lidar instrument aboard the International Space Station (ISS) that produces detailed observations of the 3-dimensional structure of the Earth’s surface. GEDI precisely measures forest canopy height, canopy vertical structure, and surface elevation which enhances our understanding of global carbon and water cycle processes, biodiversity, and habitat. GEDI is the first of its kind to provide high resolution laser ranging observations optimized for lidar measurements of the Earth’s forests and topography at the highest resolution and densest sampling of any other lidar instrument in orbit. Data from GEDI is archived and distributed by the LP DAAC. View a list of GEDI products archived by LP DAAC.

##### HLS

Principal Investigator: Christopher Neigh, NASA Goddard Space Flight Center, Co-Investigator: Junchang Ju, University of Maryland

The Harmonized Landsat Sentinel-2 (HLS) project is a NASA initiative to produce seamless, harmonized surface reflectance data from the Operational Land Imager (OLI) aboard the joint NASA/USGS Landsat 8 and Landsat 9 satellites and the Multi-Spectral Instrument (MSI) aboard Europe’s Copernicus Sentinel-2A, Sentinel-2B, and Sentinel-2C satellites. The aim is to produce seamless products with normalized parameters, which include atmospheric correction, cloud and cloud-shadow masking, geographic co-registration and common gridding, bidirectional reflectance distribution function, and spectral band adjustment. This will provide global observation of the Earth’s surface every 1.6 days with 30 meter spatial resolution. Applications that will benefit include agriculture assessment and monitoring, and phenology. View a list of HLS products archived by LP DAAC.

##### SNWG OPERA Disturbance

Investigator: Matt Hansen, University of Maryland

The Global Land Disturbance Mapping for JPL Observation Products for End-Users for Remote Sensing Analysis (OPERA) at the University of Maryland, is sponsored by NASA and developed at the Jet Propulsion Laboratory (JPL) in response to scientific gaps identified by the Satellite Needs Working Group (SNWG). The OPERA land Disturbance (DIST) product suite will provide near-global, per-pixel land surface change from Harmonized Landsat Sentinel-2 (HLS) scenes. The primary focus of the DIST product suite is to map vegetation cover loss along with general disturbance trends every 2–3 days with 30 meter spatial resolution. For more information on the OPERA DIST product suite, visit the DIST JPL product site.

##### Future Missions

Thank you for your interest in our upcoming missions. Details regarding future missions will be shared soon.

NASA’s Earth Science Program is dedicated to the advancement of Earth remote sensing and the scientific use of satellite measurements to expand our understanding of Earth systems. LP DAAC collaborates with the Making Earth System Data Records for Use in Research Environments (MEaSUREs) projects to facilitate the introduction of long-term, consistent, high-quality data records to the land remote sensing community.

##### GFCC

Principal Investigator: John Townshend, University of Maryland

The Global Forest Cover Change (GFCC) collection is derived from enhanced Landsat Global Land Survey (GLS) datasets and provides global coverage information on surface reflectance, water cover, and forest cover change.

| Short Name | Keyword | Spatial Resolution (m) | Temporal Resolution

| GFCC30FCC.001 | Land Cover | 30 | Multi-Year

| GFCC30SR.001 | Land Cover | 30 | Multi-Year

| GFCC30TC.003 | Land Cover | 30 | Multi-Year

| GFCC30WC.001 | Land Cover, Water | 30 | Other

##### GFSAD

Principal Investigator: Prasad Thenkabail, USGS

The Global Food Security-support Analysis Data (GFSAD) collection provides information on global croplands, including crop density and crop extent. The monitoring of global croplands is critical for policymaking and provides important baseline data that are used in many agricultural studies pertaining to water sustainability and food security.

| GFSAD1KCD.001 | Cropland | 1000 | Multi-Year

| GFSAD1KCM.001 | Cropland | 1000 | Multi-Year

| GFSAD30AFCE.001 | Cropland | 30 | Multi-Year

| GFSAD30AUNZCNMOCE.001 | Cropland | 30 | Multi-Year

| GFSAD30EUCEARUMECE.001 | Cropland | 30 | Multi-Year

| GFSAD30NACE.001 | Cropland | 30 | Multi-Year

| GFSAD30SAAFGIRCE.001 | Cropland | 30 | Multi-Year

| GFSAD30SACE.001 | Cropland | 30 | Multi-Year

| GFSAD30SEACE.001 | Cropland | 30 | Multi-Year

| GFSAD30VAL.001 | Cropland | 90 | Multi-Year

##### GLanCE

Principal Investigators: Mark Friedl, Curtis Woodcock, Pontus Olofsson, Thomas Loveland, and Zhe Zhu

The Global Land Cover Mapping and Estimation (GLanCE) data record is an annual product derived from Landsat 5, 7, and 8. This project provides high-quality maps of global land cover, land use, and land cover change at 30 meter spatial resolution annually from 2001 to 2019. These data provide the user community with land cover type, land cover change, metrics characterizing the magnitude and seasonality of greenness of each pixel, and the magnitude of change.

| Short Name | Collection | Keyword | Spatial Resolution (m) | Temporal Resolution

| GLanCE30.001 | MEaSUREs GLanCE | Land Cover, Vegetation Indices (VI) | 30.0 | Yearly

##### LSTE

Principal Investigator: Simon Hook, Jet Propulsion Laboratory
Co-investigator: Kerry Anne Cawse-Nicholson, Jet Propulsion Laboratory

The Land Surface Temperature and Emissivity (LSTE) collection provides global LSTE coverage for common use in surface energy balance studies, land surface modeling, climate change modeling, and urban heat island studies.

| CAM5K30CF.002 | MEaSUREs LSTE | Emissivity | 5600.0 | Monthly

| CAM5K30CF.003 | MEaSUREs LSTE | Emissivity | 5600.0 | Monthly

| CAM5K30CFCLIM.003 | MEaSUREs LSTE | Emissivity | 5600.0 | Monthly

| CAM5K30COVCLIM.003 | MEaSUREs LSTE | Emissivity | 25000.0 | Monthly

| CAM5K30EM.002 | MEaSUREs LSTE | Emissivity | 5600.0 | Monthly

| CAM5K30EM.003 | MEaSUREs LSTE | Emissivity | 5600.0 | Monthly

| CAM5K30EMCLIM.003 | MEaSUREs LSTE | Emissivity | 5600.0 | Monthly

| CAM5K30UC.003 | MEaSUREs LSTE | Emissivity | 5600.0 | Monthly

| CAM5K30UC.002 | MEaSUREs LSTE | Emissivity | 5600.0 | Monthly

| CAM5K30UCCLIM.003 | MEaSUREs LSTE | Emissivity | 5600.0 | Monthly

| GEOLST4KHR.002 | MEaSUREs LSTE | Land Surface Temperature (LST) | 4000.0 | < Daily

| LEOLSTCMG30.002 | MEaSUREs LSTE | Land Surface Temperature (LST) |   | Monthly

| LEOLSTCMG30.001 | MEaSUREs LSTE | Land Surface Temperature (LST) |   | Monthly

##### NASADEM

Principal Investigator: Sean Buckley, Jet Propulsion Laboratory

NASADEM extends the legacy of the Shuttle Radar Topography Mission (SRTM) by improving the digital elevation model (DEM) height accuracy and data coverage as well as providing several new data products. The improvements were achieved by reprocessing the original SRTM radar signal and telemetry data with updated algorithms and auxiliary data not available at the time of the original SRTM processing.

| NASADEM_HGT.001 | MEaSUREs NASADEM | Elevation | 30.0 | Multi-Day

| NASADEM_SC.001 | MEaSUREs NASADEM | Elevation | 30.0 | Multi-Day

| NASADEM_SHHP.001 | MEaSUREs NASADEM | Elevation | 30.0 | Multi-Day

| NASADEM_SIM.001 | MEaSUREs NASADEM | Elevation | 30.0 | Multi-Day

| NASADEM_SSP.001 | MEaSUREs NASADEM | Elevation | 30.0 | Multi-Day

##### SRTM

Principal Investigator: Michael Kobrick, Jet Propulsion Laboratory

The NASA Shuttle Radar Topography Mission (SRTM) is a collaborative effort by NASA, the National Geospatial-Intelligence Agency (NGA), and the participation of German and Italian space agencies. This collaboration aims to generate a near-global digital elevation model (DEM) of Earth using radar interferometry. SRTM was the primary (and virtually only) payload on the STS-99 mission of the space shuttle Endeavour, which launched February 11, 2000, and ﬂew for 11 days.

| SRTMGL1.003 | MEaSUREs SRTM | Elevation | 30.0 | Multi-Day

| SRTMGL1N.003 | MEaSUREs SRTM | Elevation | 30.0 | Multi-Day

| SRTMGL3.003 | MEaSUREs SRTM | Elevation | 90.0 | Multi-Day

| SRTMGL30.021 | MEaSUREs SRTM | Elevation | 1000.0 | Multi-Day

| SRTMGL3N.003 | MEaSUREs SRTM | Elevation | 90.0 | Multi-Day

| SRTMGL3S.003 | MEaSUREs SRTM | Elevation | 90.0 | Multi-Day

| SRTMIMGM.003 | MEaSUREs SRTM | Elevation | 30.0 | Multi-Day

| SRTMIMGR.003 | MEaSUREs SRTM | Elevation | 30.0 | Multi-Day

| SRTMSWBD.003 | MEaSUREs SRTM | Elevation, Land Cover | 30.0 | Multi-Day

##### VCF

Principal Investigator: Matthew Hansen, University of Maryland

The Vegetation Continuous Fields (VCF) collection provides global vegetation continuous fields from Advanced Very High Resolution Radiometer (AVHRR) long-term data records version 4 (LTDR v4) from 1982 through 2016. Version 1 of this data product includes a time series of VCF data at 5600 m resolution containing information on percent of tree cover, non-tree vegetation, and bare ground.

| VCF5KYR.001 | MEaSUREs VCF | Vegetation Continuous Fields (VCF) | 5600.0 | Yearly

##### VIP

Principal Investigator: Kamel Didan, University of Arizona

The Vegetation Index and Phenology (VIP) collection comprises 34 years of a consistent, global record of vegetation indices and landscape phenology. The VIP collections are based on MODIS, AVHRR, and Satellite Pour l'Observation de la Terre (SPOT) data inputs.

| VIP01.004 | MEaSUREs VIP | Phenology, Vegetation Indices (VI) | 5600.0 | Daily

| VIP07.004 | MEaSUREs VIP | Phenology, Vegetation Indices (VI) | 5600.0 | Weekly

| VIP15.004 | MEaSUREs VIP | Phenology, Vegetation Indices (VI) | 5600.0 | Multi-Day

| VIP30.004 | MEaSUREs VIP | Phenology, Vegetation Indices (VI) | 5600.0 | Monthly

| VIPPHEN_EVI2.004 | MEaSUREs VIP | Phenology, Vegetation Indices (VI) | 5600.0 | Yearly

| VIPPHEN_NDVI.004 | MEaSUREs VIP | Phenology, Vegetation Indices (VI) | 5600.0 | Yearly

##### WELD and GWELD

Principal Investigator: David Roy, Michigan State University; Zhang Hankui, South Dakota State University

The NASA-funded Web-enabled Landsat Data (WELD) project generated Landsat Enhanced Thematic Mapper Plus (ETM+) mosaics of the conterminous United States and Alaska from 2002 to 2012. The WELD products were developed specifically to provide consistent data that could be used to derive land cover, geophysical and biophysical products for regional assessment of surface dynamics, and to study Earth system functionality. The WELD data products were decommissioned on December 2, 2019.

Global WELD (GWELD) is an expansion of WELD data products on a global scale using Landsat 4 and 5 Thematic Mapper (TM) and Landsat 7 Enhanced Thematic Mapper Plus (ETM+) Collection 1 (Versions 3.0 and 3.1) and Collection 2 (Version 3.2) data. These global products provide monthly and annual data for terrestrial non-Antarctic locations for six 3-year epochs that occur every 5 years from 1985 to 2010. GWELD Version 3.0 data for the 2010 epoch is currently available. GWELD Version 3.1 data for the 2000, 1990, and 1985 epochs and Version 3.2 data for the 2005 epoch are also available.

| GWELDMO.003 | MEaSUREs WELD and GWELD | Surface Reflectance, Vegetation Indices (VI) | 30.0 | Monthly

| GWELDMO.031 | MEaSUREs WELD and GWELD | Surface Reflectance, Vegetation Indices (VI) | 30.0 | Monthly

| GWELDMO.032 | MEaSUREs WELD and GWELD | Surface Reflectance, Vegetation Indices (VI) | 30.0 | Monthly

| GWELDYR.003 | MEaSUREs WELD and GWELD | Surface Reflectance, Vegetation Indices (VI) | 30.0 | Yearly

| GWELDYR.031 | MEaSUREs WELD and GWELD | Surface Reflectance, Vegetation Indices (VI) | 30.0 | Yearly

| GWELDYR.032 | MEaSUREs WELD and GWELD | Surface Reflectance, Vegetation Indices (VI) | 30.0 | Yearly

##### Airborne Hyperspectral Reflectance Mosaic

Principal Investigators: John Gamon, Ran Wang, Hamed Gholizadeh, Jeannine Cavender-Bares, Christopher J. Helzer

Airborne Hyperspectral Reflectance datasets were acquired over various plots and sites: Cedar Creek Ecosystem Science Reserve (CCESR), Minnesota; Tallgrass Prairie Preserve, Oklahoma; Wood River, Nebraska; and Indian Cave State Park, Nebraska. These fine resolution mosaics can be used to better understand the optical diversity-biodiversity relationship and to investigate the spatial sensitivity of the optical diversity-biodiversity relationship at local scales.

| AEHYP1TPPOK.001 | Airborne Hyperspectral | Surface Reflectance | 1 | Other

| AEHYPCCMN300MM.001 | Airborne Hyperspectral | Surface Reflectance | 0.3 | Other

| AEHYPICNE1M.001 | Airborne Hyperspectral | Surface Reflectance | 1 | Other

| AEHYPWRNE1M.001 | Airborne Hyperspectral | Surface Reflectance | 1 | Other

##### ASTER GED

Principal Investigator: Glynn Hulley, Jet Propulsion Laboratory (JPL)

Using data from the Advanced Spaceborne Thermal Emission and Reflection Radiometer (ASTER) on NASA's Terra spacecraft, NASA/JPL derived the most detailed global emissivity map of the Earth, termed the ASTER Global Emissivity Database (GED).

| AG100.003 | ASTER GED | Elevation, Emissivity, Land Surface Temperature (LST), Vegetation Indices (VI) | 100 | Other

| AG1km.003 | ASTER GED | Elevation, Emissivity, Land Cover, Land Surface Temperature (LST), Vegetation Indices (VI) | 1000 | Other

| AG5KMMOH.041 | ASTER GED | Emissivity, Vegetation Indices (VI) | 5600 | Monthly

##### GHISA

Principal Investigator: Prasad Thenkabail, Itiya P. Aneece, Isabella Mariotto

The Global Hyperspectral Imaging Spectral-library of Agricultural crops (GHISA) is a comprehensive hyperspectral library of the world’s major agricultural crops (e.g., wheat, rice, barley, corn, soybeans, cotton, sugarcane, potatoes, chickpeas, lentils, and pigeon peas). Hyperspectral data for GHISA were acquired from spaceborne, airborne, and ground-based platforms.

| GHISACASIA.001 | GHISA | Cropland |   | Seasonal

| GHISACONUS.001 | GHISA | Cropland |   | Seasonal

##### G-LiHT

Principal Investigator: Bruce Cook

Goddard’s Light Detection and Ranging (LiDAR), Hyperspectral, and Thermal Imager (G-LiHT) was developed to simultaneously derive information about the composition, structure, and function of terrestrial ecosystems using a combination of airborne LiDAR, imaging spectroscopy, and thermal measurements.

| GLCHMK.001 | G-LiHT | Canopy Height, Lidar | 1 | Varies

| GLCHMT.001 | G-LiHT | Canopy Height, Lidar | 1 | Varies

| GLDSMT.001 | G-LiHT | Canopy Height, Elevation, Lidar | 1 | Varies

| GLDTMK.001 | G-LiHT | Elevation, Lidar | 1 | Varies

| GLDTMT.001 | G-LiHT | Elevation, Lidar | 1 | Varies

| GLHYANC.001 | G-LiHT | Lidar | 1 | Varies

| GLHYVI.001 | G-LiHT | Lidar, Vegetation Indices (VI) | 1 | Varies

| GLLIDARPC.001 | G-LiHT | Lidar | 1 | Varies

| GLMETRICS.001 | G-LiHT | Canopy Height, Lidar, Surface Reflectance, Vegetation Indices (VI) | 15 | Varies

| GLORTHO.001 | G-LiHT | Lidar | 0.3 | Varies

| GLRADS.001 | G-LiHT | Lidar, Surface Radiance | 1 | Varies

| GLREFL.001 | G-LiHT | Lidar, Surface Reflectance | 1 | Varies

| GLTRAJECTORY.001 | G-LiHT | Elevation | 1 | Varies

##### Headwall Hyperspectral Reflectance Mosaic

Principal Investigator: John Gamon, Ran Wang

An imaging spectrometer on an airborne tram system collected images at 1-millimeter spatial resolution for 33 selected plots at the biodiversity (BioDIV) experiment at the CCESR LTER, Minnesota. The hyperspectral range and fine resolution of the data will assist researchers in studying biodiversity in this area. These findings can be used to guide future airborne studies in developing more effective large-scale biodiversity sampling methods.

| HWHYPCCMN1MM.001 | Headwall | Surface Reflectance | 0.001 | Other

##### LGRIP30

Principal Investigator: Prasad Thenkabail

The Global Food Security-support Analysis Data (GFSAD) project provides the highest-known spatial-resolution Landsat-derived Global Rainfed and Irrigated area Product (LGRIP) at 30 meter spatial resolution for the nominal year 2015. The LGRIP product maps agricultural lands, calculates irrigated and rainfed areas, and performs accuracy assessment of the product.

| LGRIP30.001 | LGRIP | Cropland, Land Cover, Water | 30 | Multi-Year

| LGRIP30_L1_IRRI.002 | LGRIP | Cropland, Land Cover, Water | 30 | Multi-Year

| LGRIP30_L1_RAIN.002 | LGRIP | Cropland, Land Cover, Water | 30 | Multi-Year

| LGRIP30_L2_IRRI.002 | LGRIP | Cropland, Land Cover, Water | 30 | Multi-Year

| LGRIP30_L2_RAIN.002 | LGRIP | Cropland, Land Cover, Water | 30 | Multi-Year

| LGRIP30_L3.002 | LGRIP | Cropland, Land Cover, Water | 30 | Multi-Year

##### LPJ-EOSIM

Principal Investigator: Thomas Colligan

The Lund-Potsdam-Jena Earth Observation SIMulator (LPJ-EOSIM) model replicates biospheric processes to estimate how plants of different functional types obtain resources through photosynthesis and competition. The model estimates global wetland methane (CH4) emissions using simulated wetland extent and characteristics including soil moisture, temperature, and carbon content. The wetland CH4 flux data will be used to support the United States Greenhouse Gas Center (US GHG Center) and its mission to study natural GHG fluxes. A carbon dioxide (CO2) product is planned for the near future, along with the possibility of more data products containing biospheric variables such as gross primary production and net primary production.

| LPJ_EOSIM_L2_DCH4E.001 | LPJ-EOSIM | Greenhouse Gases (GHG), Methane (CH4) | 50000 | Daily

| LPJ_EOSIM_L2_DCH4E_LL.001 | LPJ-EOSIM | Greenhouse Gases (GHG), Methane (CH4) | 50000 | Daily

| LPJ_EOSIM_L2_MCH4E.001 | LPJ-EOSIM | Greenhouse Gases (GHG), Methane (CH4) | 50000 | Monthly

| LPJ_EOSIM_L2_MCH4E_LL.001 | LPJ-EOSIM | Greenhouse Gases (GHG), Methane (CH4) | 50000 | Monthly

##### LPJ-PROSAIL

Principal Investigator: Bryce Currey

The LPJ-PROSAIL global simulated imaging spectroscopy products are being developed to provide data analogs for the development of future spaceborne global imaging spectroscopy missions including NASA’s Surface Biology and Geology (SBG). The data products consist of simulated imaging spectroscopy data produced by the LPJ-PROSAIL model. The LPJ-PROSAIL model was developed by coupling LPJ, a dynamic global vegetation model, with PROSAIL, a canopy radiative transfer model. LPJ-PROSAIL will consist of multiple products containing dynamic surface reflectance, dynamic top-of-atmosphere radiance, and vegetation traits. The reflectance and radiance products will have a spectral range of 400 to 2500 nanometers (nm) with a spectral resolution of 10 nm at approximately 50 kilometer spatial resolution. Data will be available for each year from 2000 to present. Data availability within that timeframe will vary by product. Each granule will contain a full year of simulated monthly data. For more information visit the LPJ-PROSAIL website.

| LPJ_L2_SSREF.001 | LPJ-PROSAIL | Spectroscopy, Surface Reflectance | 50000 | Monthly

| LPJ_L2_SSREF.002 | LPJ-PROSAIL | Spectroscopy, Surface Reflectance | 50000 | Monthly

##### MuSLI

Principal Investigator: Mark Friedl

NASA’s Multi-Source Land Imaging (MuSLI) Land Surface Phenology (LSP) (MSLSP) provides a 30 m spatial resolution data product containing phenology timing metrics for North America. These data are useful for a wide range of applications including: ecosystem and agro-ecosystem modeling, monitoring of terrestrial ecosystems and their response to climate change and extreme events, as well as mapping land cover, land use, and land cover change.

| MSLSP30NA.011 | MuSLI | Phenology, Surface Reflectance, Vegetation Indices (VI) | 30 | Yearly

##### FUTURE Community

###### INCA

Principal Investigator: Josh Gray

NASA’s Indicator of National Climate Assessment (INCA) will provide a 500 meter spatial resolution, yearly data product that spans from January 2001 to December 2016; it will contain global phenology metrics based on Terra and Aqua Moderate Resolution Imaging Spectroradiometer (MODIS) data. This data product will provide a remote sensing-based land surface phenology climate indicator (LSP-CI) that supports the National Climate Assessment’s need for national scale, long-term monitoring of climate change impacts on ecosystems.

NASA's LP DAAC processes, archives, and distributes land data products to hundreds of thousands of users in the earth science community. Our land data products are made available and support the ongoing monitoring of Earth’s land dynamics and environmental systems to facilitate interdisciplinary research, education, and decision-making.

##### Process

Raw data collected from specific satellite sensors, such as ASTER aboard NASA’s Terra satellite, are received and processed into a readable and interpretable format here at the LP DAAC, while other data undergo processing in other facilities around the country before arriving to the LP DAAC to be archived and distributed to the public.

##### Archive

The LP DAAC continually archives a wide variety of land remote sensing data products collected by sensors onboard satellites, aircraft, and the International Space Station (ISS). The archive currently totals more than 14 petabytes of data.

##### Distribute

All data products in the archive are distributed free of charge through NASA Earthdata Search. The LP DAAC supports tools and services, like the Application for Extracting and Exploring Analysis Ready Samples (AppEEARS), which allows users to transform and visualize data before download while offering enhanced subsetting and reprojecting capabilities.

##### Apply

Visit our News and Learn pages to learn about LP DAAC data products in various stories and articles and get access to webinars, tutorials, and data recipes. Interact with the land data science community through the Earthdata Forum. Discover tools available to support a variety of research needs on our Data and Tools page.

##### History

LP DAAC is located just outside of Sioux Falls, South Dakota, at the USGS Earth Resources Observation and Science (EROS) Center. On August 28, 1990, NASA and USGS established EROS as a Distributed Active Archive Center (DAAC).

Our community of users includes scientists, researchers, federal, state, and local government, educational and commercial professionals, application users, and the general public.

#### CoreTrustSeal Certified Repository

We are proud to be a CoreTrustSeal Certified Repository. CoreTrustSeal is an international, community based, non-governmental, and non-profit organization promoting sustainable and trustworthy data infrastructures.

---

## VIIRS

- **URL:** https://search.earthdata.nasa.gov/search?q=VIIRS
- **Título de la página:** Earthdata Search
- **Para qué sirve (según la lista):** Proveen reflectancia corregida, índices de vegetación (como NDVI) e indicadores de estrés vegetal, suelo desnudo y cambios estacionales a distintas resoluciones espaciales.

> ⚠️ Muy poco texto: probablemente la página se arma con JavaScript. Ábrela en el navegador.

##### Earthdata Search uses JavaScript

Please use a JavaScript-aware browser and make sure JavaScript is enabled.

##### Your browser is out of date

In order to use Earthdata Search, you must upgrade your web browser.
Alternatively, you can Earthdata Access.

To upgrade your browser, click on the icons below to go to the download page.

-    Chrome
-    Firefox
-    Safari
-    Opera
-    Internet Explorer

v26.2.3-3 NASA Official: Doug Newman FOIA NASA Privacy Policy USA.gov     Earthdata Access: A Section 508 accessible alternative

---

## NASA POWER

- **URL:** https://power.larc.nasa.gov/
- **Título de la página:** NASA POWER | Homepage
- **Para qué sirve (según la lista):** Contiene conjuntos de datos solares, meteorológicos y climatológicos (temperatura, humedad, radiación) para estimar el uso de agua de los cultivos y el riesgo de heladas.

Skip to main content

### POWERing the Future of Energy, Infrastructure, and Agroclimatology

Enabling NASA Earth observations, modeling, and analysis for decision-makers worldwide to address the most pressing challenges posed by our environment and make decisions that enhance societal well-being.

Search site content

Parameters

Explore our catalog of 300+ solar and meteorological data parameters.

Documentation

Review data methodology, tutorials, and publications citing POWER data.

Impact Stories

Dive into stories demonstrating POWER's impact worldwide.

---

## Shuttle Radar Topography Mission (SRTM)

- **URL:** https://www.earthdata.nasa.gov/data/instruments/srtm
- **Título de la página:** Shuttle Radar Topography Mission (SRTM) | NASA Earthdata
- **Para qué sirve (según la lista):** Suministra modelos globales de elevación y terreno para analizar pendientes, escorrentía, flujo de agua y riesgo de erosión.

Skip to main content

Earthdata Forum is down due to unplanned maintenance. Please contact earthdata-support@nasa.gov with questions. See the alert

Suomi NPP is no longer delivering new data. Users must transition to alternative products. Suomi NPP data announcement

The Shuttle Radar Topography Mission (SRTM) payload flew aboard the Space Shuttle Endeavour during the STS-99 mission. SRTM collected topographic data over nearly 80% of Earth's land surfaces, creating the first-ever near-global dataset of land elevations.

The SRTM payload consisted of two radar antennas, one located in the shuttle's payload bay and the other installed on the end of a 200-foot mast that extended from the payload bay. Each SRTM radar assembly contained two types of antenna panels: C-band and X-band. C-band radar data were used to create near-global topographic maps of Earth called Digital Elevation Models (DEMs).

Data from the X-band radar were used to create slightly higher resolution DEMs but without the global coverage of the C-band radar. The two radar datasets were combined to create interferogramatic maps of scanned areas. SRTM measurements took place February 11-22, 2000.

Image

Image Caption

Color shaded-relief image of Africa created from SRTM data. Map color-coding is directly related to topographic height, with brown and yellow indicating lower elevations and green and white indicating higher elevations. Blue areas represent water. Credit: NASA/JPL-Caltech/National Geospatial Intelligence Agency.

SRTM Mission

#### Data

28 Datasets

View Data and Tools

View data alert history

#### Instrument Type

Imaging Radars

#### Specifications

#### Resolution

Temporal

February 11, 2000 - February 22, 2000

#### Get Help

QUESTIONS & SUPPORT

Have a question?

Get help with NASA Earth science data, datasets, tools, services, and metadata on the Earthdata Forum. Experienced staff in the data user community review and answer questions.
Get help on Earthdata Forum

Earthdata
Forum

---

## ECOSTRESS

- **URL:** https://ecostress.jpl.nasa.gov/data
- **Título de la página:** Data — ECOSTRESS
- **Para qué sirve (según la lista):** Mide la temperatura de la superficie terrestre y la evapotranspiración a alta resolución espacial para detectar puntos críticos de calor y demanda hídrica de los cultivos.

#### Reprocessing Timeline

In October 2022, ECOSTRESS released Collection 2, which includes an updated radiometric vicarious calibration, improved geolocation flagging, improved cloud mask, and improvements and additions to evapotranspiration (ET) models. The team has also made available the inputs that were used in the ET models, for full transparency. These include normalized difference vegetation index (NDVI), and albedo derived from a data fusion between VIIRS and harmonized Landsat-Sentinel (HLS), as well as reanalysis data resampled to ECOSTRESS spatial resolution.

Radiance, geolocation, land surface temperature & emissivity, and cloud products (level 1 and 2 products) have been available in Collection 2 since October 05, 2022. Higher level products (level 3 and 4) have been available in Collection 2 since January 18, 2024. The team produced Collection 1 for Level 1 and 2 data products until the Collection 2 reprocessing of Level 1 and Level 2 data products was complete so that users could continue to evaluate a consistent time series. Collection 1 was discontinued in Calendar Year 2025. Collection 1 ended for level 3 and 4 products on December 31, 2022, due to the changing MODIS orbit and changes in Landsat data accessibility. The Collection 1 data availability dates and Collection 2 reprocessing dates are listed in the table below:

#### Data Example

NASA’s ECOSTRESS Maps LA’s Street Temperatures. Click on image to see larger version. - NASA/JPL-Caltech

In this overlay image, retrieved land surface temperature (LST) from NASA’s Ecosystem Spaceborne Thermal Radiometer Experiment on Space Station (ECOSTRESS) was downscaled to a spatial resolution of 10m and overlaid on a street map of Los Angeles. The image was derived by taking an average of all clear-sky afternoon (1-4pm) imagery acquired by ECOSTRESS from 2018-2023. The LST represents the ‘skin’ temperature of the surface (that you would feel to the touch) and is usually much hotter than the surface air temperature that meteorologists report in a weather forecast.

ECOSTRESS was launched to the international space station in 2018. Its primary mission is to identify plants’ thresholds for water use and water stress, giving insight into their ability to adapt to a warming climate. However, it has many other science uses including urban heat mitigation, wildfire mapping, water quality, and surface mineralogy. NASA’s Jet Propulsion Laboratory in Southern California built and manages the ECOSTRESS mission for the Earth Science Division in the Science Mission Directorate at NASA Headquarters in Washington. ECOSTRESS is an Earth Venture Instrument mission; the program is managed by NASA’s Earth System Science Pathfinder program at NASA's Langley Research Center in Hampton, Virginia

- Streets LA KMZ file (download)
- Streets LA Geotiff file (download)

How to access data - Demo

#### Get ECOSTRESS Data

| NASA Earthdata - "ECOSTRESS" Search  |

| LP DAAC subsetting tool - AppEEARS

Click on:

"point samples"

or

"area samples"  |

Data Description and FAQ

Preview of currently acquired data

LP DAAC ECOSTRESS Swath 2 Grid Data Prep Script

##### Documents

Algorithm Theoretical Basis Documents (ATBDs)

Product Specification Documents (PSDs)

User Guide Products

Combined Summary Table of ATDBs, PSDs, User Guides

##### Radiometer Spectral Response Functions (SRF)

SRF Graph

SRF Data+Graph

##### Science Data Products

Science Data Products Summary Table

---

## USDA Ag Data Commons

- **URL:** https://www.nal.usda.gov/services/agdatacommons
- **Título de la página:** Ag Data Commons User Guide | National Agricultural Library
- **Para qué sirve (según la lista):** Repositorio de acceso abierto con datos agrícolas terrestres sobre suelos, cultivos, clima, fenología y prácticas de manejo en EE. UU.

Skip to main content

Official websites use .gov
A .gov website belongs to an official government organization in the United States.

Secure .gov websites use HTTPS
A lock (  ) or https:// means you’ve safely connected to the .gov website. Share sensitive information only on official, secure websites.

### Ag Data Commons User Guide

#### What is Ag Data Commons

The Ag Data Commons is a research data catalog and repository for public access to data produced during research funded or co-funded by the United States Department of Agriculture.

In accordance with the USDA Public Access DR, all USDA-funded researchers must ensure that a catalog record indicating the point of public access to their data is created in the Ag Data Commons. Supplementary repository service is optional and is open to data without a community- or subject-specific home.

Through the Ag Data Commons, the USDA National Agricultural Library (NAL) provides services to make USDA-funded research data systems and data products Findable, Accessible, Interoperable, and Reusable (FAIR). Each submitted dataset goes through a review by Ag Data Commons data curators -- NAL metadata librarians who ensure completeness and accuracy of the submission before approving it for publication.

#### Eligibility for submissions to the Ag Data Commons

If you are thinking about sharing your research output through the Ag Data Commons, please make sure that your submission meets the following conditions:

1. USDA-funding. A submission must satisfy at least one of the two USDA-funding criteria:

a. One of the co-authors of the data product is affiliated with USDA, or

b. It was produced as a result of a research project funded or co-funded by USDA, for example through NIFA grant or through an agency-approved research project.

2. Content type. The item(s) considered for submission must fall into one of the following types:

a. Data (e.g. tabular data, genomic sequences, multimedia materials)

b. Data product (e.g., database)*

c. Non-executable software created to help users process or model data*.

3. Level of access - public. Your submission must contain only data and/or data products intended for public access. The Ag Data Commons does not accept datasets with Personally Identifiable Information (PII).

*See Ag Data Commons Collection Policy for details about these content types.

#### Account creation

After verifying that your submission is eligible to deposit in the Ag Data Commons, you can create an account. Note that a user account is only required to submit data resources to the Ag Data Commons. Those wishing to view or download data do not require accounts.

To create an account, select “Log In” at the upper right corner of the Ag Data Commons home page. You will be prompted to select the user type for your account. Options include:

- Customer: Use this option for non-federal users (e.g., university partners, grant recipients, etc.). You can use Login.gov or eAuth to log into your account.
- USDA Employee/Contractor: Use this option if you work directly for the USDA. You can use your PIV card, USDA MobileLinc, or USDA Work Account through Microsoft to log into your account.
- Other Federal Employee/Contractor: Use this option if you work for a federal department outside the USDA. You can use your PIC/CAC PIN or Login.gov to log into your account.

Your account will be automatically created the first time you log in.

New users will start with zero storage capacity and need to request storage space from the curation team to upload dataset files. The Data Submission Manual provides instructions on this process. A curator will review your request and may follow up with you for additional information before granting the request.

#### More on Ag Data Commons

-   Data Submission Manual
-   Ag Data Commons Collection Policies
-   Ag Data Commons Portal [agdatacommons.nal.usda.gov]
-   Ag Data Commons Usage Statistics [agdatacommons.nal.usda.gov]
-   View Articles Citing Ag Data Commons [zotero.org]
-   Ag Data Commons Dashboard: Trend in Citations to ADC

#### Page Content Curated By

Knowledge Services Division (KSD)

---

## Web Soil Survey (WSS)

- **URL:** https://websoilsurvey.nrcs.usda.gov/app/
- **Título de la página:** Web Soil Survey - Home
- **Para qué sirve (según la lista):** Proporciona mapas detallados y propiedades oficiales de los suelos de EE. UU., incluyendo drenaje, textura, materia orgánica y riesgo de compactación.

﻿

Skip to Page Content

|   |   |   |   |   |   |   |   |   |

|    |   You are here: Web Soil Survey Home     |

|   |

|   |   |       |   |

|   |   |     |   |

|   |   |

|   Soils Home

|   National Cooperative Soil Survey (NCSS)

|   Archived Soil Surveys

|   Status Maps

|   Official Soil Series Descriptions (OSD)

|   Series Extent Explorer

|   Geospatial Data Gateway

|   eFOTG

|   National Soil Characterization Data

|   Soil Health

|   Soil Geography

|  Web Soil Survey (WSS) provides soil data and information produced by the National Cooperative Soil Survey. It is operated by the USDA Natural Resources Conservation Service (NRCS) and provides access to the largest natural resource information system in the world. NRCS has soil maps and data available online for more than 95 percent of the nation’s counties and anticipates having 100 percent in the near future. The site is updated and maintained online as the single authoritative source of soil survey information.

|  Soil surveys can be used for general farm, local, and wider area planning. Onsite investigation is needed in some cases, such as  soil quality assessments  and certain conservation and engineering applications. For more detailed information, contact your local USDA Service Center at the following link: USDA Service Center or your NRCS State Soil Scientist at the following link: NRCS State Soil Scientist.

|   |        |   |  Use the Area of Interest tab to define your area of interest.

Click or Press the Enter or Spacebar key to view the larger image. Press the Escape key to close.

|   |        |   | Click the Soil Map tab to view or print a soil map, and detailed descriptions of the soils in your Area of Interest.

|   |        |   | Click the Soil Data Explorer tab to access soil data for your area and determine the suitability of the soils for a particular use. The items you want saved in a report can be added to your shopping cart.

|   |        |   | Use the Shopping Cart tab to get your custom printable report immediately, or download it later.

|    |   |   | Start Web Soil Survey (WSS)  |   |

|    |   |   |   Know Web Soil Survey Requirements  |   |

|    |   |   |   Know Web Soil Survey operation hours  |   |

|    |   |   | Find what areas of the U.S. have soil data  |   |

|    |   |   |    Find information by topic  |   |

|    |   |   |  Know how to hyperlink from other documents to Web Soil Survey  |   |

|    |   |   |  Know the SSURGO data structure  |   |

|    |   |   |    Use Web Soil Survey on a mobile device  |   |

|    |   |   |  Web Soil Survey 3.4.0 has been released! View Web Soil Survey release history  |   |

|    |   |   | Sign up for e-mail updates via GovDelivery  |   |

|    |   |   |   Getting Started With Web Soil Survey   |   |

|    |   |   |   How to use Web Soil Survey Online Help  |   |

|    |   |   |   Known Problems and Workarounds  |   |

|    |   |   |   Frequently Asked Questions  |   |

|    |   |   |   Citing Web Soil Survey as a source of soils data  |   |

|    |    |

|   |     |

|    |

NRCS Home  |  USDA  |  NRCS Soils  |  FOIA  |

Accessibility Statement  |  Privacy Policy  |  Non-Discrimination Statement  |

Information Quality  |  USA.gov  |  White House

---

## Cropland Data Layer (CDL): CropScape

- **URL:** https://nassgeodata.gmu.edu/CropScape/
- **Para qué sirve (según la lista):** Ofrece clasificaciones anuales de cultivos a 30 metros de resolución en EE. UU. para examinar rotaciones existentes y patrones agrícolas reales.

> ❌ No se pudo descargar: El sitio tiene un certificado SSL mal configurado (el navegador lo tolera, Python no). Ábrelo en el navegador.

---

## PRISM Climate Data

- **URL:** https://prism.oregonstate.edu/
- **Para qué sirve (según la lista):** Contiene datos climáticos diarios, mensuales y normales de 30 años para EE. UU. (precipitación, temperatura, punto de rocío, fechas de heladas) ajustados por topografía.

> ❌ No se pudo descargar: El sitio tiene un certificado SSL mal configurado (el navegador lo tolera, Python no). Ábrelo en el navegador.

---

## USDA NRCS SSURGO/STATSGO2

- **URL:** https://www.nrcs.usda.gov/resources/data-and-reports/soils
- **Título de la página:** Soils | Natural Resources Conservation Service
- **Para qué sirve (según la lista):** Provee atributos detallados del suelo a escala de campo y regional (capacidad de retención de agua, grupo hidrológico, factores de erosión).

Skip to main content

Official websites use .gov
A .gov website belongs to an official government organization in the United States.

Secure .gov websites use HTTPS
A lock (    ) or https:// means you’ve safely connected to the .gov website. Share sensitive information only on official, secure websites.

###  Soils

The Iowa NRCS Soils Program provides quality soil, geographic, and resources information, products, and services to internal and external customers.

##### Web Soil Survey

Web Soil Survey - Web Soil Survey provides soil data and information produced by the National Cooperative Soil Survey. It is operated by the USDA Natural Resources Conservation Service and provides access to the largest natural resource information system in the world.

- Published Soil Surveys for Iowa
- Available Soil Surveys and Formats

##### Iowa Soil Resources

- Soil Series Descriptions
- Soil Quality for Environmental Health
Soil and Land Use - This Iowa State University Agronomy Extension site is intended to provide data related to the agricultural uses of Iowa land.

- Soil Survey & Digital Soil Data: Soil Suitabilities & Interpretation
- Soils Education
- Dig It! The Secrets of Soil

##### Videos

- How to Differentiate and Identify Soil Horizons (YouTube)
- Soils 101

####  Additional Soils Documents

SoilWeb 2.0 App Fact Sheet (1.25 MB)

Iowa MLRA Soil Survey Offices (305.04 KB)

Major Land Resource Areas (MLRA) Regions Map of Iowa (814.88 KB)

Major Land Resource Area (MLRA) Regions Map of Iowa (1.62 MB)

Iowa Woodland Suitability Recommendations (by Soil Type) (321.81 KB)

Iowa Soil Survey Correlation Dates Map (69.38 KB)

####  Contact

Patrick Chase

State Soil Scientist

515-284-4135

patrick.chase@usda.gov

---

## National Agriculture Imagery Program (NAIP)

- **URL:** https://naip-usdaonline.hub.arcgis.com/
- **Título de la página:** National Agriculture Imagery Program - NAIP Hub Site
- **Para qué sirve (según la lista):** Imágenes aéreas de alta resolución (1 metro) tomadas durante la temporada de crecimiento en EE. UU. para delimitar campos y observar el desarrollo de cultivos.

> ⚠️ Muy poco texto: probablemente la página se arma con JavaScript. Ábrela en el navegador.



---

## USGS National Land Cover Database (NLCD)

- **URL:** https://www.usgs.gov/centers/eros/science/national-land-cover-database
- **Título de la página:** National Land Cover Database | U.S. Geological Survey
- **Para qué sirve (según la lista):** Clasificaciones de cobertura y uso del suelo a 30 metros a lo largo de varias décadas para contextualizar paisajes agrícolas y zonas circundantes.

Skip to main content

Official websites use .gov
A .gov website belongs to an official government organization in the United States.

Secure .gov websites use HTTPS
A lock () or https:// means you’ve safely connected to the .gov website. Share sensitive information only on official, secure websites.

###  National Land Cover Database

Completed

By Earth Resources Observation and Science (EROS) Center   September 11, 2018

#### Annual NLCD Now Available!

Visit the Website

-   Overview
-   Science
-   Data
-   Multimedia
-   Publications
-   News

EROS is central to the creation of the National Land Cover Database (NLCD) which stands as the definitive land cover database for the United States.

###### NOTE: This webpage refers to the Legacy National Land Cover Database (NLCD). Please visit Annual NLCD for the latest release.

Media

Sources/Usage: Public Domain. View Media Details

Map of the Conterminous U.S. showing the Land Cover layer from the NLCD 2021.

Legacy NLCD includes map products characterizing land cover and land cover change across nine epochs from 2001 to 2021 (2001, 2004, 2006, 2008, 2011, 2013, 2016, 2019, and 2021) for the conterminous U.S. The 2021 suite of NLCD products follow the same protocols and procedures of the previously released NLCD epochs (2001-2019), are directly comparable to the 2019 release across the full time series, and are suitable for multi-temporal analysis. Science products and the change index, however, will need to be reacquired for the additional 2021 change information.

The U.S. Geological Survey (USGS) works closely with the Multi-Resolution Land Characteristics (MRLC) Consortium—a collaborative group of federal agencies—to produce the National Land Cover Database (NLCD) for the conterminous U.S. The MRLC, a consortium of federal agencies who coordinate and generate consistent and relevant land cover information at the national scale for a wide variety of environmental, land management, and modeling applications, have been providing the scientific community with detailed land cover products for more than 30 years. Over that time, NLCD has been one of the most widely used geospatial datasets in the U.S., serving as a basis for understanding the Nation’s landscapes in thousands of studies and applications, trusted by scientists, land managers, students, city planners, and many more as a definitive source of U.S. land cover.

Specific map products include:

- Land cover – Conterminous U.S. land cover at a 30-meter spatial resolution with a 16-class legend based on a modified Anderson Level II classification system
- Land cover change index – Provides a simple and comprehensive way to visualize change that occurred across all the NLCD epochs of land cover
- Urban imperviousness – Indicates urban impervious surfaces as a percentage of developed surface over every 30-meter pixel in the Conterminous U.S.
- Urban impervious descriptor – Classifies specific types of roads, wind tower sites, building locations, and energy production sites to allow a deeper analysis of developed features
- NLCD Science Products

- Land Cover Change Disturbance Date – Identifies the first land cover classification change event between any two adjacent target years across all NLCD epochs at the 30-meter pixel level
- Forest Disturbance Date – Identifies the most recent year of forest disturbance between the years 1984–2021
- Land Cover Change Count – Calculates an integer count total of any change recorded between two consecutive epochs
- Land Cover with additional Forest Transition Classes – Delineates spectrally stable grass and shrub areas from those that are transitional forest classes, which tend to be represented by forest harvest, burns, regrowth, and other disturbances
- U.S. Forest Service Science Tree Canopy Cover – The original, unmasked Tree Cover Canopy data produced by the U.S. Forest Service, an MRLC partner

For more information about Legacy NLCD visit the National Land Cover Database (NLCD) Products - ScienceBase-Catalog

Below are other science projects associated with this project.

######    Eyes on Earth Episode 54 – National Land Cover Database 2019  Eyes on Earth Episode 54 – National Land Cover Database 2019

Eyes on Earth is a podcast on remote sensing, Earth observation, land change and science, brought to you by the USGS Earth Resources Observation and Science (EROS) Center. In this episode, we learn about the latest land cover release from EROS.

Eyes on Earth Episode 54 – National Land Cover Database 2019

######  Eyes on Earth Episode 54 – National Land Cover Database 2019

Learn More

######    Eyes on Earth Episode 42 – Rangelands of the U.S.  Eyes on Earth Episode 42 – Rangelands of the U.S.

Eyes on Earth is a podcast on remote sensing, Earth observation, land change and science, brought to you by the USGS Earth Resources Observation and Science (EROS) Center. In this episode, we hear how Landsat helps monitor vulnerable rangelands in the Western U.S.

Eyes on Earth Episode 42 – Rangelands of the U.S.

######  Eyes on Earth Episode 42 – Rangelands of the U.S.

May 26, 2020

######   LCMAP and NLCD: Complementary Data for Understanding the Geography of the United States

Land Change Monitoring, Assessment, and Projection (LCMAP) Collection 1 science products provide unprecedented monitoring of past changes occurring in land cover and condition across the conterminous U.S. over more than 30 years at an annual timestep.

By

Core Science Systems Mission Area, National Land Imaging Program, Land Change Monitoring, Assessment, and Projection

LCMAP and NLCD: Complementary Data for Understanding the Geography of the United States

######  LCMAP and NLCD: Complementary Data for Understanding the Geography of the United States

######    Eyes on Earth Episode 3 - National Land Cover Database  Eyes on Earth Episode 3 - National Land Cover Database

Eyes on Earth is a podcast on remote sensing, Earth observation, land change and science, brought to you by the USGS Earth Resources Observation and Science (EROS) Center. In this episode, we talk about the National Land Cover Database.

Eyes on Earth Episode 3 - National Land Cover Database

######  Eyes on Earth Episode 3 - National Land Cover Database

September 11, 2018

######   Western U.S. Cheatgrass and Shrubland Monitoring

The USGS Earth Resources Observation and Science (EROS) Center National Land Cover Database team in collaboration with the Bureau of Land Management (BLM) has produced the most comprehensive remote-sensing based quantification of western United States shrublands to date.

By

Earth Resources Observation and Science (EROS) Center

Western U.S. Cheatgrass and Shrubland Monitoring

######  Western U.S. Cheatgrass and Shrubland Monitoring

September 12, 2013

######   National Land Cover Database Visualization and Information Tool

The National Land Cover Database (NLCD) serves as the definitive Landsat-based, 30-meter resolution, land cover database for the Nation. NLCD supports a wide variety of Federal, State, local, and nongovernmental applications that seek to assess ecosystem status and health, understand the spatial patterns of biodiversity, predict effects of climate change, and develop land management...

By

Community for Data Integration (CDI)

National Land Cover Database Visualization and Information Tool

######  National Land Cover Database Visualization and Information Tool

The National Land Cover Database (NLCD) serves as the definitive Landsat-based, 30-meter resolution, land cover database for the Nation. NLCD supports a wide variety of Federal, State, local, and nongovernmental applications that seek to assess ecosystem status and health, understand the spatial patterns of biodiversity, predict effects of climate change, and develop land management policy

Below are data or web applications associated with this project.

August 5, 2020

######    National Land Cover Database (NLCD) 2016 Shrubland Fractional Components for the Western U.S. (ver. 3.0, July 2020)  National Land Cover Database (NLCD) 2016 Shrubland Fractional Components for the Western U.S. (ver. 3.0, July 2020)

Quantifying Western U.S. shrublands as a series of fractional components with remote sensing provides a new way to understand these changing ecosystems. The USGS NLCD team in collaboration with the BLM has produced the most comprehensive remote sensing-based quantification of Western U.S. shrublands to date. Nine shrubland ecosystem components, including percent shrub, sagebrush...

By

June 18, 2020

######    Remote Sensing Shrub/Grass National Land Cover Database (NLCD) Back-in-Time (BIT) Products for the Western U.S., 1985 - 2018  Remote Sensing Shrub/Grass National Land Cover Database (NLCD) Back-in-Time (BIT) Products for the Western U.S., 1985 - 2018

The need to monitor change in sagebrush steppe is urgent due to the increasing impacts of climate change, shifting fire regimes, and management practices on ecosystem health. Remote sensing provides a cost-effective and reliable method for monitoring change through time and attributing changes to drivers. We report an automated method of mapping rangeland fractional component cover over...

By

January 7, 2020

######    Non-native and synanthropic bird data derived from 2010-2012 Breeding Bird Survey and associated landscape metrics from 2011 NLCD  Non-native and synanthropic bird data derived from 2010-2012 Breeding Bird Survey and associated landscape metrics from 2011 NLCD

Locations of and proportional abundance of non-native and synanthropic passerines were extracted from Breeding Bird Survey (BBS) data from 2010-2012. Information characterizing the spatial variation and the associated amount, aggregation, and diversity of developed and agricultural land cover types was extracted from the National Land Cover Datasets of 2011. Data supported analyses in...

By

Fort Collins Science Center

######    National Land Cover Database (NLCD)  National Land Cover Database (NLCD)

The National Land Cover Database (NLCD) provides nation-wide data on land cover and land cover change at the Landsat Thematic Mapper (TM) 30-meter resolution. NLCD provides spatial reference and descriptive data for characteristics of the land surface such as thematic class (e.g., urban, agriculture, and forest), percent impervious surface, and percent tree canopy cover.

By

Drought

Below are multimedia items associated with this project.

Dallas-Ft. Worth - NLCD 2016 Impervious Descriptor layer

Mapping Roadways at Landsat Scale

October 15, 2021

###### Mapping Roadways at Landsat Scale

A satellite flying over this area northwest of Dallas, TX will capture a wide variety of urban and rural activity. The 80-odd square miles seen in the Landsat image on the left includes airports, dense urban centers, suburban and exurban neighborhoods, manufacturing and distribution centers, oil and gas production sites, lakes, forests, wetlands and more.

By

By

Eyes on Earth - National Land Cover Database 2019 thumbnail

Eyes on Earth Episode 54 - National Land Cover Database 2019

July 12, 2021

###### Eyes on Earth Episode 54 - National Land Cover Database 2019

The National Land Cover Database, or NLCD, was the first and remains the most well-known set of satellite-based land cover mapping products released by EROS. It sorts the each 30-by-30-meter plot of land in the United States into a land cover class, such as cropland, pasture, high-intensity developed, deciduous forest, and the like.

By

Core Science Systems Mission Area, Earth Resources Observation and Science (EROS) Center

By

Eyes on Earth Episode 42 - Rangelands of the U.S.

January 25, 2021

###### Eyes on Earth Episode 42 – Rangelands of the U.S.

The extensive rangelands across the Western United States are threatened by invasive grasses, climate change, and altered fire regimes that can disturb the landscape. The largely semi-arid lands are also important for the survival of species that need undisturbed sagebrush ecosystems to thrive.

By

Core Science Systems Mission Area, Earth Resources Observation and Science (EROS) Center , Landsat Missions

By

Eyes on Earth - Collin Homer

Eyes on Earth - Episode 3 - The National Land Cover Database

September 16, 2019

###### Eyes on Earth - Episode 3 - The National Land Cover Database

Sorting Landsat data into an accurate and reliable record of land cover in the United States is one of the most important jobs at EROS. This episode of Eyes on Earth explores the what, how, and why of the National Land Cover Database (NLCD).

By

By

Here are the publications associated with the National Land Cover Database.

Filter Total Items: 14

April 20, 2026

######    Thematic accuracy assessment of the National Land Cover Database (NLCD2021) for the conterminous United States  Thematic accuracy assessment of the National Land Cover Database (NLCD2021) for the conterminous United States

The MultiResolution Land Characteristics (MRLC) consortium’s National Land Cover Database (NLCD) was established as an operational, stakeholder-oriented land cover monitoring program with the release of the NLCD2001 database. Both land cover and land cover change data became available with the release of NLCD2006. Here, we report the land cover and land cover change accuracies for...

Authors

James Wickham, Stephen V. Stehman, Daniel G. Sorenson, Leila Gass, Jon Dewitz, Johnathan Vasa Kilaru

By

March 1, 2023

######    Thematic accuracy assessment of the NLCD 2019 land cover for the conterminous United States  Thematic accuracy assessment of the NLCD 2019 land cover for the conterminous United States

The National Land Cover Database (NLCD), a product suite produced through the MultiResolution Land Characteristics (MRLC) consortium, is an operational land cover monitoring program. Starting from a base year of 2001, NLCD releases a land cover database every 2–3-years. The recent release of NLCD2019 extends the database to 18 years. We implemented a stratified random sample to collect...

James Wickham, Stephen V. Stehman, Daniel G. Sorenson, Leila Gass, Jon Dewitz

By

Earth Resources Observation and Science (EROS) Center, Western Geographic Science Center

January 30, 2023

######    National Land Cover Database 2019: A comprehensive strategy for creating the 1986-2019 forest disturbance product  National Land Cover Database 2019: A comprehensive strategy for creating the 1986-2019 forest disturbance product

The National Land Cover Database (NLCD) 2016 products show that, between 2001 and 2016, nearly half of the land cover change in the conterminous United States (CONUS) involved forested areas. To ensure the quality of NLCD land cover and land cover change products, it is important to accurately detect the location and time of forest disturbance. We designed a comprehensive strategy to...

Suming Jin, Jon Dewitz, Congcong Li, Daniel G. Sorenson, Zhe Zhu, Rakibul Shogib, Patrick Danielson, Brian Granneman, Catherine Costello, Adam Case, Leila Gass

By

January 11, 2023

######    National Land Cover Database 2019: A new strategy for creating clean leaf-on and leaf-off Landsat composite images  National Land Cover Database 2019: A new strategy for creating clean leaf-on and leaf-off Landsat composite images

National Land Cover Database (NLCD) 2019 is a new epoch of national land cover products for the conterminous United States. Image quality is fundamental to the quality of any land cover product. Image preprocessing has often taken a considerable proportion of overall time and effort for this kind of national project. An approach to prepare image inputs for NLCD 2019 production was...

Suming Jin, Jon Dewitz, Patrick Danielson, Brian Granneman, Catherine Costello, Zhe Zhu

By

Science Synthesis, Analysis, and Research Program, Earth Resources Observation and Science (EROS) Center, Advanced Research Computing (ARC)

February 23, 2021

######    Rangeland fractional components across the western United States from 1985 to 2018  Rangeland fractional components across the western United States from 1985 to 2018

Monitoring temporal dynamics of rangelands to detect and understand change in vegetation cover and composition provides a wealth of information to improve management and sustainability. Remote sensing allows the evaluation of both abrupt and gradual rangeland change at unprecedented spatial and temporal extents. Here, we describe the production of the National Land Cover Database (NLCD)...

Matthew B. Rigge, Collin Homer, Hua Shi, Debbie Meyer, Brett Bunde, Brian J. Granneman, Kory Postma, Patrick Danielson, Adam Case, George Z. Xian

By

March 3, 2020

######    Conterminous United States land cover change patterns 2001–2016 from the 2016 National Land Cover Database  Conterminous United States land cover change patterns 2001–2016 from the 2016 National Land Cover Database

The 2016 National Land Cover Database (NLCD) product suite (available on www.mrlc.gov), includes Landsat-based, 30 m resolution products over the conterminous (CONUS) United States (U.S.) for land cover, urban imperviousness, and tree, shrub, herbaceous and bare ground fractional percentages. The release of NLCD 2016 provides important new information on land change patterns across CONUS...

Collin G. Homer, Jon Dewitz, Suming Jin, George Z. Xian, Catherine Costello, Patrick Danielson, Leila Gass, Michelle Funk, James Wickham, Steven Stehman, Roger F. Auch, Kurt H. Riitters

By

August 21, 2018

######    Accuracy assessment of NLCD 2011 impervious cover data for the Chesapeake Bay region, USA  Accuracy assessment of NLCD 2011 impervious cover data for the Chesapeake Bay region, USA

The National Land Cover Database (NLCD) contains three eras (2001, 2006, 2011) of percentage urban impervious cover (%IC) at the native pixel size (30 m-x-30 m) of the Landsat Thematic Mapper satellite. These data are potentially valuable to environmental managers and stakeholders because of the utility of %IC as an indicator of watershed and aquatic condition, but lack an accuracy...

James Wickham, Nate Herold, Stephen V. Stehman, Collin Homer, George Z. Xian, Peter Claggett

By

March 29, 2017

######    Thematic accuracy assessment of the 2011 National Land Cover Database (NLCD)  Thematic accuracy assessment of the 2011 National Land Cover Database (NLCD)

Accuracy assessment is a standard protocol of National Land Cover Database (NLCD) mapping. Here we report agreement statistics between map and reference labels for NLCD 2011, which includes land cover for ca. 2001, ca. 2006, and ca. 2011. The two main objectives were assessment of agreement between map and reference labels for the three, single-date NLCD land cover products at Level II...

James Wickham, Stephen V. Stehman, Leila Gass, Jon Dewitz, Daniel G. Sorenson, Brian J. Granneman, Richard V. Poss, Lori Anne Baer

By

Earth Resources Observation and Science (EROS) Center, Geosciences and Environmental Change Science Center, Western Geographic Science Center

January 9, 2013

######    Accuracy assessment of NLCD 2006 land cover and impervious surface  Accuracy assessment of NLCD 2006 land cover and impervious surface

Release of NLCD 2006 provides the first wall-to-wall land-cover change database for the conterminous United States from Landsat Thematic Mapper (TM) data. Accuracy assessment of NLCD 2006 focused on four primary products: 2001 land cover, 2006 land cover, land-cover change between 2001 and 2006, and impervious surface change between 2001 and 2006. The accuracy assessment was conducted by...

James D. Wickham, Stephen V. Stehman, Leila Gass, Jon Dewitz, Joyce A. Fry, Timothy G. Wade

By

January 1, 2010

######    Thematic accuracy of the NLCD 2001 land cover for the conterminous United States  Thematic accuracy of the NLCD 2001 land cover for the conterminous United States

The land-cover thematic accuracy of NLCD 2001 was assessed from a probability-sample of 15,000 pixels. Nationwide, NLCD 2001 overall Anderson Level II and Level I accuracies were 78.7% and 85.3%, respectively. By comparison, overall accuracies at Level II and Level I for the NLCD 1992 were 58% and 80%. Forest and cropland were two classes showing substantial improvements in accuracy in...

J.D. Wickham, S.V. Stehman, J.A. Fry, J.H. Smith, Collin G. Homer

By

######    National Land Cover Database 2001 (NLCD01) Tree Canopy Layer Tile 4, Southeast United States: CNPY01_4  National Land Cover Database 2001 (NLCD01) Tree Canopy Layer Tile 4, Southeast United States: CNPY01_4

This 30-meter resolution data set represents the tree canopy layer for the conterminous United States for the 2001 time period. The data have been arranged into four tiles to facilitate timely display and manipulation within a Geographic Information System, browse graphic: nlcd01-partition.jpg The National Land Cover Data Set for 2001 was produced through a cooperative project conducted...

Andrew E. LaMotte, Michael Wieczorek

April 11, 2009

######    Comparison of NLCD with NWI Classifications of Baldwin and Mobile Counties, Alabama  Comparison of NLCD with NWI Classifications of Baldwin and Mobile Counties, Alabama

An assessment of the accuracy of National Land Cover Data 2001 as compared to National Wetlands Inventory mapping of Mobile and Baldwin Counties conducted by the U.S. Geological Survey's (USGS) National Wetlands Research Center (NWRC). Both classifications were checked against stratified randomly selected ground-based sites and with each other to compare the accuracy of the NLCD with NWI

Larry Handley, Chris Wells

Below are news stories associated with the National Land Cover Database.

October 8, 2024

######    NLCD’s Path from Early Landscape Snapshot to Decades of Change  NLCD’s Path from Early Landscape Snapshot to Decades of Change

The widely used National Land Cover Database (NLCD) has long been the foundational land cover source for scientists, resource managers, and decision-makers across the United States, trusted for its accurate and unbiased data. Here, we’re exploring the evolution of NLCD through its reinvention this year as Annual NLCD.

By

Core Science Systems Mission Area, National Land Imaging Program, Earth Resources Observation and Science (EROS) Center, Landsat Missions

Maximizing Accuracy of Rangeland Data

April 3, 2024

######  Maximizing Accuracy of Rangeland Data

Project Manager Matthew Rigge and the Rangeland Condition Monitoring Assessment and Projection (RCMAP) team take an almost businesslike approach to...

Read Article

NLCD 2021 Now Available

July 31, 2023

######  NLCD 2021 Now Available

The U.S. Geological Survey (USGS), in association with the Multi-Resolution Land Characteristics (MRLC) Consortium, is pleased to announce the...

New Land Cover Maps Capture Nearly Two Decades of Change Across the U.S.

July 20, 2021

######  New Land Cover Maps Capture Nearly Two Decades of Change Across the U.S.

The U.S. Geological Survey recently released updated land cover maps for the conterminous United States that depict 18 years of change to the Nation’s...

New USGS EROS Tool Shows County-By-County Change Across United States

April 6, 2021

######  New USGS EROS Tool Shows County-By-County Change Across United States

The USGS Earth Resources Observation and Science (EROS) Center has released a new online tool to help the public better visualize county-by-county...

Detecting Shrub Recovery in Sagebrush Steppe: Comparing Landsat-Derived Maps with Field Data on Historical Wildfires

February 26, 2021

######  Detecting Shrub Recovery in Sagebrush Steppe: Comparing Landsat-Derived Maps with Field Data on Historical Wildfires

Sagebrush can be scarce after fires in a semiarid ecosystem and their paucity over vast burn areas creates challenges for detection by remote sensing...

EROS Rangeland Tools Aid Western U.S. Land Managers

January 27, 2021

######  EROS Rangeland Tools Aid Western U.S. Land Managers

The extensive rangelands across the Western United States are threatened by invasive grasses, climate change, and altered fire regimes that can...

Land Cover Partnership Releases Change Datasets for U.S., Mexico, Canada

November 18, 2020

######  Land Cover Partnership Releases Change Datasets for U.S., Mexico, Canada

The release of a change dataset for North America’s three largest countries will enable GIS researchers to more easily study continent-scale land use...

Rangeland Mapping Tools Take Users Back in Time Across Western U.S.

August 3, 2020

######  Rangeland Mapping Tools Take Users Back in Time Across Western U.S.

The USGS Earth Resources Observation and Science (EROS) Center and Department of Interior’s Bureau of Land Management have just released an...

NLCD Readies Improvements for Upcoming Release of 2019 Product Suite

July 27, 2020

######  NLCD Readies Improvements for Upcoming Release of 2019 Product Suite

The next edition of the National Land Cover Database (NLCD) will appear more quickly than previous editions, offer accuracy comparable to NLCD 2016...

New Land Cover Maps Depict 15 Years of Alaska Change

April 17, 2020

######  New Land Cover Maps Depict 15 Years of Alaska Change

The latest edition of the National Land Cover Database (NLCD 2016) for Alaska is now publicly available.

EROS contributes to New Land Cover Maps for U.S., Canada, Mexico

February 27, 2020

######  EROS contributes to New Land Cover Maps for U.S., Canada, Mexico

The three largest countries in North America share trade, climate and culture in a host of broad and specific ways. A new set of land cover maps for...

New NLCD products to be folded into Esri software, Earth Engine

May 24, 2019

######  New NLCD products to be folded into Esri software, Earth Engine

The National Land Cover Database (NLCD) 2016 product suite was recently released for bulk download on the Multi-Resolution Land Characteristics...

By

By

By

By

By

By

By

By

By

By

By

By

By

By

By

By

By

By

By

By

By

By

By

By

By

By

Was this page helpful?

---

## NLDAS/GLDAS: Land Data Assimilation Systems

- **URL:** https://www.earthdata.nasa.gov/
- **Título de la página:** Your Gateway to NASA Earth Observation Data | NASA Earthdata
- **Para qué sirve (según la lista):** Combina observaciones satelitales y terrestres para generar series temporales subdiarias de temperatura, precipitación, humedad del suelo y evapotranspiración.

Skip to main content

Earthdata Forum is down due to unplanned maintenance. Please contact earthdata-support@nasa.gov with questions. See the alert

Suomi NPP is no longer delivering new data. Users must transition to alternative products. Suomi NPP data announcement

#### Browse Data by Topic

Our data pathfinders guide you by topic to the data, tutorials, and tools you need for your research.

Atmosphere

Biosphere

Climate Indicators

Cryosphere

Human Dimensions

Land Surface

Ocean

Solid Earth

Sun-Earth Interactions

Terrestrial Hydrosphere

#### New on Earthdata

Read More in the News

Worldview Image of the Week

2 MIN READ

Atmospheric River Season for the Pacific Northwest

Rainy season brings some relief after the summer's severe drought

Tutorial

5 MIN READ

How to Search & Order Data With the LAADS Find Data Interface

This tutorial guides the user through the LAADS Find Data Interface.

Event

1 MIN READ

earthaccess Hackathon at AGU 2026

The NASA Openscapes group is hosting an earthaccess hackathon on Wednesday, December 9, 2026 from 3:30 to 6:30pm during the American Geophysical Union Fall Meeting.

News

8 MIN READ

What a Difference an Hour Makes

TEMPO's hourly scans of North America are revolutionizing air quality monitoring across the continent.

Tracking the Journey of Iceberg A81

3 MIN READ

Transitioning From Suomi NPP to NOAA-20 and NOAA-21: What LANCE Users Need to Know

Blog

Autumnal Colors in the Ridge and Valley Province

Detecting Station Errors Quickly in Earth Laser Ranging Data

#### Featured Data Tools

From discovery to visualization, our data tools simplify and streamline your research.

Earthdata Search

Earthdata Search enables data discovery, search, comparison, visualization, and access across NASA’s Earth science data holdings.

Earthdata GIS

Earthdata GIS is a resource for distributing cloud-native, GIS-ready NASA Earth science data and services, including over 200 raster and feature geospatial services as well as resources such as thematic applications and ArcGIS StoryMaps.

GUARDIAN

The GNSS-based Upper Atmospheric Realtime Disaster Information and Alert Network (GUARDIAN) is a near real-time (NRT) ionospheric monitoring tool for natural hazards warning.

#### Open Science

We empower a collaborative scientific process through the open sharing of data and knowledge. Our open data, services, and software policies ensure that data are fully available to any user for any purpose.

##### Earth Science Data Systems 2025 Fiscal Year Highlights

View All Program Metrics

Image

+7.4 billion

files distributed to end users

10+ million

distinct data and service users

178+ petabytes

of Earth science data available

---

## FAO Global Agro-Ecological Zones (GAEZ)

- **URL:** https://gaez.fao.org/
- **Título de la página:** GAEZ v4 Data Portal
- **Para qué sirve (según la lista):** Proporciona capas globales de idoneidad agroclimática, restricciones del suelo y potencial de rendimiento para decenas de cultivos.

> ⚠️ Muy poco texto: probablemente la página se arma con JavaScript. Ábrela en el navegador.



---

## CoCoRaHS

- **URL:** https://www.cocorahs.org/Maps
- **Redirige a:** https://www.cocorahs.org/Maps/
- **Título de la página:** CoCoRaHS - Community Collaborative Rain, Hail & Snow Network
- **Para qué sirve (según la lista):** Red comunitaria con mediciones diarias de lluvia y nieve en Norteamérica útil para validar estimaciones satelitales como IMERG.

> ⚠️ Muy poco texto: probablemente la página se arma con JavaScript. Ábrela en el navegador.



---

## USGS National Water Information Systems (NWIS)

- **URL:** https://waterdata.usgs.gov/nwis
- **Redirige a:** https://waterdata.usgs.gov/
- **Título de la página:** Water Data for the Nation
- **Para qué sirve (según la lista):** Registros históricos de niveles de agua subterránea, caudal de arroyos y calidad del agua para evaluar la disponibilidad para riego.

Skip to main content

Official websites use .gov
A .gov website belongs to an official government organization in the United States.

Secure .gov websites use HTTPS
A lock (  ) or https:// means you’ve safely connected to the .gov website. Share sensitive information only on official, secure websites.

### Water Data for the Nation

High-quality and discoverable water data for everyone

Over 135 years of water data from more than one million monitoring locations

The United States Geological Survey (USGS) collects water data at monitoring locations across the United States using automated sensors  and manual data collection. Each monitoring location has location information that details the location name and identifier, the agency responsible for data collection, and geographic information about the location. Most monitoring locations have data available in one or more of the following categories of water data: continuous data, daily data, field measurements, and discrete sample data.
Learn more about the categories of water data available in Water Data for the Nation.

Find monitoring locations by monitoring location name, number, or political boundary. Refined searches by state, county, site type and more are also possible.

#### Find the water information you need

##### Discover real-time data in your state

State pages provide a summary of the latest continuous data being collected in your state. Quickly filter the map and list to show a data type of interest to you, or customize the filters to further refine the map and list to your needs.

Select a State or Territory Page

Select a state

##### Create a list of your favorite monitoring locations

Make and share a list of USGS monitoring locations that you are interested in. Access the latest continuous water data at those locations all in one place. Create combined location graphs or a custom list of data graphs from your favorites list.

Go to My Favorites

##### View latest conditions and weather events

USGS has over 13,500 real-time stream, lake, reservoir, precipitation, water quality, and groundwater monitoring locations. View the latest continuous data in your area together with weather-related data to understand rapidly changing water conditions.

Go to the National Water Dashboard

##### Create a water alert

USGS monitors water conditions nationwide. Get notified with WaterAlert, a near-real time hydrologic alerting system that notifies you of stream, lake, and coastal conditions across the nation. Subscribe to text or email alerts when water conditions change.

Go to WaterAlert

##### Explore historical water data

USGS has collected water data throughout US states and territories for more than 135 years. Find historical and currently operational monitoring locations collecting continuous and discrete sample data that interests you. Filter using locations of interest, type of water data, and recency of data that meet your needs.

Go to Explore USGS Water Data

##### Access water data

USGS has several options to support access to all water data available in Water Data for the Nation. Water Data APIs provide USGS water data in machine-readable formats via REST APIs, a common framework applications use to search and download data. The dataRetrieval package simplifies the process of loading USGS water data into R or Python environments.

Go to Water Data APIsGo to dataRetrieval

---

## USDA AMS Market News

- **URL:** https://www.ams.usda.gov/market-news
- **Título de la página:** USDA Market News | Agricultural Marketing Service
- **Para qué sirve (según la lista):** Publica precios de materias primas, tendencias de demanda y condiciones del mercado agrícola para evaluar la viabilidad económica de los cultivos de rotación.

Skip to main content

### USDA Market News

For 100 years, AMS has provided free, unbiased price and sales information to assist in the marketing and distribution of farm commodities. Each year, Market News issues thousands of reports, providing the industry with key wholesale, retail and shipping data.

The reports give farmers, producers and other agricultural businesses the information they need to evaluate market conditions, identify trends, make purchasing decisions, monitor price patterns, evaluate transportation equipment needs and accurately assess movement.

Market News captures data for:

- Cotton and Tobacco
- Dairy & milk products
- Fruits, vegetables & specialty crops
- Livestock, meats, poultry, eggs, grain & hay
- Organic
- Local & regional foods

---

## USDA NASS QuickStats

- **URL:** https://quickstats.nass.usda.gov/
- **Título de la página:** USDA/NASS QuickStats Ad-hoc Query Tool
- **Para qué sirve (según la lista):** Estadísticas agrícolas a nivel de condado y estado en EE. UU., incluyendo rendimientos, superficie sembrada e historial de producción.

/* The following is used for dendancies in build "dojox.grid.DataGrid", "dijit.layout.ContentPane", "dijit.form.MultiSelect", "dijit.form.ComboBox", "dijit.form.Form", "dojo.data.ItemFileReadStore", "dijit.ProgressBar", "dijit.layout.BorderContainer", "dijit._Widget", "dijit.Tree", "dijit.form.TextBox", "dijit.form.ValidationTextBox", "dojox.validate.web", "dojo.fx", "dijit.Editor", "dijit._editor.plugins.AlwaysShowToolbar", "dijit._editor.plugins.EnterKeyHandling", "dijit._editor.plugins.FontChoice", // 'fontName','fontSize','formatBlock' "dijit._editor.plugins.TextColor", "dijit._editor.plugins.LinkDialog", "dojo.dnd.Container", "dojo.dnd.Manager", "dojo.dnd.Source", "dijit.Menu", "dojox.widget.PlaceholderMenuItem", "dojo.parser" */

Quick Stats

Status:

Keyword Search
Hints

##### Keyword Search Hints:
Close(X)

The keyword search feature allows you to search using any word. For any keyword that you enter, all matching items will be returned (i.e. a search for "Corn" will yield results for Corn, Sweet Corn, and Popcorn). Once you have initiated a search by keyword, you can then proceed to limit by any other available Selections.

If you enter two or more keywords, the results will include entries for all entered keywords. Example: a search for "apple orange" will yield results for any items containing the word orange OR the word apple.

The keyword search is not case sensitive.

Search is currently only enabled for commodities.

---

## OpenET

- **URL:** https://openetdata.org/
- **Redirige a:** https://etdata.org/
- **Título de la página:** Open-Source Transparent Water Management Data | OpenET
- **Para qué sirve (según la lista):** Ofrece estimaciones de evapotranspiración a escala de campo basadas en satélites para los estados del oeste de EE. UU., ayudando a gestionar el riego.

Skip to content

### Filling the Biggest Data Gap

in Water Management

OpenET empowers water management from local to global scales by delivering transparent, scientifically rigorous satellite-based evapotranspiration (ET) data through accessible tools.

Data Explorer

OpenET API

FARMS Tool

What's the difference? Compare tools

#### Open, Trusted Data Transforms Decision-Making

See how OpenET data is driving innovation—from optimizing on-farm water use to advancing sustainable water management to informing policy at the basin scale.

###### Advancing Groundwater Sustainability with California DWR & OpenET

California

Read More

###### Sustainable Water Management for the Ogallala Aquifer

Twin Platte Natural Resources District, West Central Nebraska

###### Using Satellite Data to Measure Consumptive Water Use for Irrigation & Water Conservation Programs

Upper Colorado River Basin

###### OpenET & Water Planning, Data Collection, & Data Dissemination

Texas

###### Support for Precision Irrigation Tools & Optimized Farm Management

California Central Coast

###### Testing Innovative Management Practices for Water Conservation on Pasturelands

Kremmling, Colorado

###### Restoring Groundwater Balance & Supply Through Community Planning

Harney County, Oregon

###### Overcoming Measurement Challenges & Streamlining Water Compliance

Sacramento-San Joaquin Delta, California

#### Built for Impact,

Powered by Transparency

Our methods are transparent, verifiable, and rigorously validated. At its core, OpenET is about solutions—giving farmers, water managers, and communities the tools they need to make decisions.

Our data are openly available and made actionable through easy-to-use tools.

Our partnerships build trust and solutions that scale through genuine collaboration.

Open Science & Transparency

“OpenET provides real-time insights into crop water use that farmers have never had before. When combined with soil-moisture probes, it helps producers grow more with less water — a game-changer for the next generation of agriculture.”

Dwane Roth

Fourth-generation Kansas Farmer (semiretired)

“OpenET’s ability to provide large-scale, spatially rich ET data helps us better understand crop water use patterns across diverse cropping systems. By combining OpenET with local soil, crop, and weather data, we’re working to build tools that support near real-time, practical decision-making in the field.

OpenET has the potential to play a key role in improving on-farm water management across the West.”

Maria Zamora Re

Extension Irrigation Specialist @ Oregon State University

#### Actionable Data

By making high-resolution evapotranspiration (ET) data widely accessible and easy to use, OpenET empowers growers, water managers, policymakers, and researchers to make smarter, more sustainable decisions. The “open” in OpenET means that the data are publicly available for anyone to use, while still being developed and maintained through a rigorous, science-based process to ensure accuracy and reliability.

#####   Proven, science-backed methods for ET data

OpenET uses proven, science-backed methods to produce daily, monthly, and annual satellite-based ET data at the field scale (30m x 30m).

#####   Precipitation and vegetation condition

OpenET also provides access to gridded precipitation information and satellite data on vegetation conditions—offering a comprehensive view of key factors that influence water use.

Explore Data Production Methods

#### A Collaborative Solution to a Critical Need

OpenET puts the best available science into the hands of those who need it most.

Developed by leading experts in partnership with farmers, water managers, and policymakers, OpenET delivers transparent, field-scale ET data to support real-world water challenges.

Learn more about how it can be used here

#####   Develop smarter
irrigation strategies

#####   Support flexible water conservation
and trading programs

#####   Create balanced
water budgets

#####   Increase groundwater
sustainability efforts

#### OpenET Consortium Partners

Learn more about the partners

#### How OpenET Works

OpenET calculates evapotranspiration (ET) using publicly available data and trusted scientific models. Here’s how it all comes together:

-  1We use satellite observations of Land Surface Temperature (LST) and vegetation conditions. We use gridded weather data products, not data from individual weather stations (with the exception of the creation of bias-correction surfaces for reference ET).
-  2This data is fed into calculate ET models to compute field-scale water use.
-  3Daily, monthly, & annual ET data are provided via easy-to-use & reliable tools.

Explore Research & Literature

#### Stay Informed

Sign up for our quarterly newsletter to stay up to date on new data releases, advances, and OpenET community engagement.

#### Filling the Biggest Data Gap

As we expand globally, our mission remains the same: deliver open, reliable, and actionable water data—developed with users, for users.

#### Compare OpenET Tools

#####   Data Explorer

A user-friendly, visual tool for quickly exploring ET data. You can select areas of interest, view historical patterns, and download results.

More About Data Explorer

#####   API

Provides automated access to ET data for large-scale or repeated use. Ideal for integrating ET into irrigation scheduling tools, hydrologic models, water accounting systems, or other applications.

More About the API

#####   FARMS Tool

Designed for growers, this tool compares ET with water use at the field level. Reports from FARMS can help users to optimize irrigation efficiency, and support farm-level decision-making.

More About FARMS

---

## USFS LANDFIRE

- **URL:** https://www.landfire.gov/
- **Título de la página:** Homepage | LANDFIRE
- **Para qué sirve (según la lista):** Capas de tipos y condiciones de vegetación, modelos de combustible y características del paisaje en EE. UU. para analizar microclimas y biodiversidad.

Skip to main content

-  Reference
-  Disturbance
-  Vegetation
-  Fuel
-  Historic Fire Regime
-  Topographic

Discover the LF mission, who we are, what we do and how LF is important to you. Also learn about the LF History and how it all began...

Learn More

Explore our data approach, applications, methods, uncover detailed product information, and download the data in various formats ...

Browse Data

Navigate through our support materials, including our technical documentation, dictionary, definitions and standards, and LF publications ...

View Resources

###### Data Alerts

See More Alerts

Data Release: 2026-10-27

2025 Full Extent CONUS products release and LFRDB update.

Data Release: 2026-09-30

2025 Fall Seasonal Fuels and AK & CONUS Annual Disturbance updates are available.

Data Release: 2026-06-23

2025 Summer Seasonal Fuels and NW GeoArea Vegetation, Fuel, and Preliminary Annual Disturbance product updates are available.

Data Release: 2026-05-18

2025 Spring Seasonal Fuels and AK Vegetation, Fuel, and Preliminary Annual Disturbance product updates are available.

Data Release: 2026-04-30

2025 SW Vegetation, Fuel, and Preliminary Annual Disturbance update is available.

Data Release: 2026-04-15

Early Spring Seasonal Fuels FBFM40 product for the LF 2025 Update is available.

Data Update: 2026-01-28

Historical Disturbance products retired.

---

## Global Ecosystem Dynamics Investigation (GEDI)

- **URL:** https://gedi.umd.edu/data
- **Redirige a:** https://gedi.umd.edu/data-collection-started/
- **Título de la página:** Data collection started - GEDI
- **Para qué sirve (según la lista):** Mediciones láser de alta resolución sobre la estructura forestal, altura del dosel y biomasa aérea alrededor de paisajes agrícolas.

GEDI

Ecosystem Lidar

- Mission

- Mission Status
- Mission Overview
- Technology
- Timeline
- Mission Team

- Instrument

- Instrument Overview
- Specifications
- Launch

- Science

- Science Overview
- Publications

- GEDI-Related Publications
- Conference Proceedings

- Competed Science Team

- Applications

- Applications Overview
- Topography and Surface Deformation
- Water Resources
- Weather Prediction
- Forest Management

- Data Products

- Products Overview
- Access
- ATBD Documents
- L4B visualization
- Calibration/Validation
- Resources & Tutorials

- Media

- Gallery
- Latest News

- Contact

Data collection started

- 0

- April 16, 2019

GEDI finished its on-orbit checkout phase (the commissioning period) and started official operations to acquire science data on March 25th, 2019. GEDI is currently following Reference Ground Tracks (RGTs) to evenly sample the forest structure across the earth. Every week the science team prioritizes the potential RGTs by programming the instrument to point nadir, or slightly off-nadir, to provide the best spatial coverage and to target specific areas of interest. The science data collection phase is scheduled to last for 2 years and the first data products will be delivered in six months around the end of September, 2019. Before then we plan to make example data sets available to help the community prepare for the first data release.

###### Image: GEDI data collection over South Carolina woodland, darker green shows where the leaves and branches are denser, lighter green shows less dense canopy. Image credits: Joshua Stevens (NASA Earth Observatory), Bryan Blair (NASA Goddard Space Flight Center), Michelle Hofton and Ralph Dubayah (University of Maryland).

Read more about the newly collected data in these press releases on the NASA , EarthObservatory, phys  and CofC websites.

##### FOLLOW US

© 2026 GEDI Ecosystem Lidar | WordPress Web Design and Development by HyperArts

---

## Copernicus Sentinel-2: ESA

- **URL:** https://dataspace.copernicus.eu/
- **Título de la página:** Copernicus Data Space Ecosystem | Europe's eyes on Earth
- **Para qué sirve (según la lista):** Imágenes multiespectrales de 10–20 metros de la Agencia Espacial Europea con alta frecuencia de visita para monitorear índices de vegetación y estrés de cultivos.

### Welcome to
Copernicus Data
Space Ecosystem

Welcome to the Copernicus Data Space Ecosystem, an open ecosystem that provides free instant access to a wide range of data and services from the Copernicus Sentinel missions and more on our planet’s land, oceans and atmosphere.

The Copernicus Data Space Ecosystem not only ensures the continuity of the open and free access to Copernicus data but also extends the portfolio for data processing and data access possibilities. Delve into the data immediately via the Copernicus Browser or register to create an account and have an even better comprehensive exploration experience.

- Get started

OUR NEXT EVENT

##### WSI webinar: Applications and hands-on training

18.11.2026

Online
More about this event

#### Stay informed

November 12, 2026

##### Copernicus Sentinel-5 Precursor (S5P) products improvement - operational switch

Data disruption General New feature Operational ESA news Sentinel-5P

Read article

November 9, 2026

##### Upgrade of Copernicus Browser and Sentinel Hub services from 10/11/2026 till 13/11/2026

General Service disruption System updates Batch processing API, Asynchronous Processing API, Batch Statistical API, new EO products, OGC

##### New product release: Copernicus Land Monitoring Service Protected Areas 2021

New data Copernicus Land Monitoring Service

- Discover more news

Cases highlighted

HIGHLIGHTED CASE

##### Mapping Europe's Hottest Neighbourhoods: How TreeCity Uses the Copernicus Data Space Ecosystem to Power Urban Heat Risk Planning
View this case in detail

##### Harnessing Copernicus Data to Optimize Solar Energy Production at the Benban Solar Park

##### From satellite pass to soil sensor: FairGrow brings Sentinel-2 to small growers in 57 languages

##### Real-time land cover monitoring with openEO

##### Advancing dynamic environmental mapping within openEO

####  Analysis tools at your fingertips

##### Explore the data

Copernicus Browser is a user-friendly web interface for viewing, analysing, and downloading satellite imagery directly from any web browser.

get started

##### openEO services

openEO is an open-source API that simplifies cloud-based processing of Earth observation data. It provides a common language for accessing, sharing, and transforming satellite data into actionable insights.

discover more

##### Traceability

The Traceability service ensures data integrity by allowing you to verify a product's authenticity, detect tampering, and check if it has been marked obsolete.

##### Data Workspace

Data Workspace is a web application to generate on-demand Earth Observation products. It allows you to easily select processing algorithms and configure relevant parameters.

read more

##### JupyterLab

The JupyterLab service is a web-based public virtual machine environment that enables you to work directly with CDSE data and APIs without the need to download the data.

##### Automate your analytics

The CDSE provides a range of Application Programming Interfaces (APIs), including catalog access, product download, visualization, and processing services such as STAC, openEO, and Sentinel Hub APIs.

explore the APIs

#### An ecosystem for
Earth observation
innovation

A service to benefit institutional users, research, commercial sector as well as to every citizen of our planet.

Explore the services

##### T Cloud Public

T-Systems International GmbH

##### Dunia

GeoVille

##### Terrascope

VITO Remote Sensing

##### S5P-PAL

S[&]T

NEW

Roadmap

#### CDSE Roadmap overview

#### About Copernicus

Copernicus is the European Union's flagship Earth observation initiative, designed to provide valuable information services to citizens and organizations across the EU. It utilizes a combination of satellite Earth observation and in-situ (non-space) data to monitor and understand our planet and its environment.

The data produced by Copernicus is of such high quality and relevance that it was transformative for the Earth Observation industry, and its free and open data policy is the cornerstone of the program.

The goal of the Copernicus program is to make Earth observation-based solutions accessible to all, and to leverage the power of this data to drive positive change and preserve our planet.

- November 30, 2025
- Climate

##### November 2026 desktop background

Air pollution and men's health Every November, the Movember campaign raises awareness of men's health, including mental health. While our health is influenced by genetics and…

- Read more

#### The service team

The Copernicus Data Space Ecosystem is powered by leading European cloud and earth observation service providers.The combination of the partners' experience and the guidance of ESA ensures a comprehensive, high-quality and user-friendly ecosystem.

---

## ERA5: ECMWF Reanalysis

- **URL:** https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels?tab=overview
- **Título de la página:** ERA5 hourly data on single levels from 1940 to present
- **Para qué sirve (según la lista):** Conjunto de datos de reanálisis climático global con variables horarias (temperatura, viento, radiación, temperatura del suelo) para rellenar vacíos de estaciones locales.

### ERA5 hourly data on single levels from 1940 to present

ERA5 is the fifth generation ECMWF reanalysis for the global climate and weather for the past 8 decades. Data is available from 1940 onwards. ERA5 replaces the ERA-Interim reanalysis.

Reanalysis combines model data with observations from across the world into a globally complete and consistent dataset using the laws of physics. This principle, called data assimilation, is based on the method used by numerical weather prediction centres, where every so many hours (12 hours at ECMWF) a previous forecast is combined with newly available observations in an optimal way to produce a new best estimate of the state of the atmosphere, called analysis, from which an updated, improved forecast is issued. Reanalysis works in the same way, but at reduced resolution to allow for the provision of a dataset spanning back several decades. Reanalysis does not have the constraint of issuing timely forecasts, so there is more time to collect observations, and when going further back in time, to allow for the ingestion of improved versions of the original observations, which all benefit the quality of the reanalysis product.

ERA5 provides hourly estimates for a large number of atmospheric, ocean-wave and land-surface quantities. An uncertainty estimate is sampled by an underlying 10-member ensemble at three-hourly intervals. Ensemble mean and spread have been pre-computed for convenience. Such uncertainty estimates are closely related to the information content of the available observing system which has evolved considerably over time. They also indicate flow-dependent sensitive areas. To facilitate many climate applications, monthly-mean averages have been pre-calculated too, though monthly means are not available for the ensemble mean and spread.

ERA5 is updated daily with a latency of about 5 days. In case that serious flaws are detected in this early release (called ERA5T), this data could be different from the final release 2 to 3 months later. In case that this occurs users are notified.

The data set presented here is a regridded subset of the full ERA5 data set on native resolution. It is online on spinning disk, which should ensure fast and easy access. It should satisfy the requirements for most common applications.

An overview of all ERA5 datasets can be found in this article. Information on access to ERA5 data on native resolution is provided in these guidelines.

Data has been regridded to a regular lat-lon grid of 0.25 degrees for the reanalysis and 0.5 degrees for the uncertainty estimate (0.5 and 1 degree respectively for ocean waves). There are four main sub sets: hourly and monthly products, both on pressure levels (upper air fields) and single levels (atmospheric, ocean-wave and land surface quantities).

The present entry is "ERA5 hourly data on single levels from 1940 to present".

###### Data description

###### Data type

Gridded

###### Projection

Regular latitude-longitude grid

###### Horizontal coverage

Global

###### Horizontal resolution

Reanalysis: 0.25° x 0.25° (atmosphere), 0.5° x 0.5° (ocean waves)

Mean, spread and members: 0.5° x 0.5° (atmosphere), 1° x 1° (ocean waves)

###### Temporal coverage

1940 to present

###### Temporal resolution

Hourly

###### File format

GRIB

###### Update frequency

Daily

#####

About C3SHelpPrivacyTerms of UseCookiesBackground

---

## NASA POWER · API Overview

- **URL:** https://power.larc.nasa.gov/docs/services/api/
- **Título de la página:** NASA POWER | Docs | Data Services | API Overview - NASA POWER | Docs
- **Para qué sirve (según la lista):** Panorama general de la API: endpoints, comunidades (AG = agroclimatología) y formatos.

Skip to content

### APIs¶

The RESTful Application Programming Interfaces (API) support analysis ready data distribution through a framework of microservices that retrieve, subset, and convert the data into user community specific Analysis Ready Data (ARD) formats.

#### Types¶

| Category  | Description

| Temporal  | The APIs that return user community specific Analysis Ready Data (ARD) products.

| Application  | The APIs that return user specified reports and validation products that use the Temporal APIs.

| Validate  | The APIs that enable user validation of POWER data against surface sites.

| System  | The APIs that supply consistent configuration information across the APIs.

API Response Times Vary

The response times vary between the different services and load a given time.

- As a general rule the higher the temporal level (Hourly vs Climatology) and the greater number of parameters requested will slightly slow down the API's response.
- The Application API's are the slowest to respond, typically handling multiple temporal data requests simultaneously. Additionally, they involve more intensive back-end processing, but requests typically complete in under a minute.

#### Errors¶

POWER microservice API uses conventional HTTP response codes to indicate the success or failure of an API request.

| Code  | Explanation  | Description

| 200  | Success  | The request was successful.

| 422  | Validation Error  | lists all syntax and parameter violations in the response.

| 429  | Too Many Requests  | Too Many Requests.

---

## NASA POWER · Daily API

- **URL:** https://power.larc.nasa.gov/docs/services/api/temporal/daily/
- **Título de la página:** NASA POWER | Docs | Data Services | Daily API - NASA POWER | Docs
- **Para qué sirve (según la lista):** Endpoint de datos diarios por punto: parámetros de la URL y ejemplos.

Skip to content

### Daily API¶

The Daily microservice API returns time series analysis-ready data responses for solar and meteorological data to be used directly by applications.

Additional Data Specifications: - Provides parameters by day with average, maximum, and/or minimum values. - All parameters are available in their original source spatial resolution.

Warning

If you are going to be using the Daily API to download the entire catalog, please remember that with the 0.5° x 0.5° global grid you only need to submit one request per cell. If your application persists in requesting the same relative location, it will potentially be blocked.

#### Formats¶

| Formats  | Availability  | Notes

| NetCDF  | Single Point and Regional  |

| ASCII  | Single Point and Regional  |

| ICASA  | Single Point  | Only available for the AG Community.

| JSON  | Single Point and Regional  |

| CSV  | Single Point and Regional  |

Tip

If you are requesting the ICASA format via the Data Access Viewer (DAV), you do not have to select any parameters as the DAV will autofill the required parameters. When using the Application Programming Interface (API) to request an ICASA format, you need to include at least one parameter, and the API will autofill the required parameters in the file response. For the monthly amplitude to be included in the file, please select a time period that covers at least two months. The ICASA file responds in Local Solar Time (LST). ICASA is only available for single point requests, not regional requests.

#### Time Standards¶

POWER provides two different time standards:

- Universal Time Coordinated (UTC): The most commonly accepted time standard worldwide.
- Local Solar Time (LST): A 15-degree swath that represents solar noon at the middle longitude of the swath.

- Daily UTC and LST time standards data are available from 1981/01/01 to Near Real Time (NRT)
- Daily API defaults to providing LST; use time-standard=UTC or time-standard=LST in the API request URL to specify the time standard.

#### Limitations¶

Parameters

- A maximum of 20 parameters can currently be requested in one submission for a single point. Regional requests are limited to one parameter.
- These limits do not apply if more parameters are needed by the application to construct on the fly parameters.

Wind Elevation and Custom Surface

- This parameter is only available under the "Point" spatial option.
- Wind Elevation values in Meters are required to be between 10m and 300m.
- If you provide a correct wind surface alias wind-surface, please include a surface elevation wind-elevation with the request.

For a list of wind surface aliases, please use this System API Request. For more information, please reference the Manager Documentation.

Site Elevation

If you wish to pass your own site elevation (in meters), you will receive a corrected atmospheric pressure value upon adjustment to the elevation you provided.

- Site Elevation site-elevation values are in Meters.

#### Request Structure¶

- The request arguments can be in any order after the question mark.
- A single parameter or a list of parameters can be selected with one of the following list separators: ',' or '%2C'.

##### Examples¶

To help construct and test your API requests, please use the API Pages for the POWER Daily API and POWER Manager API.

###### Point¶

SimpleComplexSite ElevationWind ElevationWind SurfaceAll OperationsICASA

1

/api/temporal/daily/point?parameters=T2M&community=SB&longitude=0&latitude=0&start=20170101&end=20170201&format=JSON

1

/api/temporal/daily/point?parameters=T2M,PS,WS10M&community=AG&longitude=0&latitude=0&start=20170101&end=20170201&format=CSV

1

/api/temporal/daily/point?parameters=T2M&community=SB&longitude=0&latitude=0&start=20170101&end=20170201&format=JSON&site-elevation=50

1

/api/temporal/daily/point?parameters=T2M&community=AG&longitude=0&latitude=0&start=20170101&end=20170201&format=ASCII&wind-elevation=50

1

/api/temporal/daily/point?parameters=T2M&community=AG&longitude=0&latitude=0&start=20170101&end=20170201&format=ASCII&wind-surface=SeaIce&wind-elevation=50

1

/api/temporal/daily/point?parameters=T2M,PS,WS10M&community=AG&longitude=0&latitude=0&start=20170101&end=20170201&format=ASCII&wind-surface=SeaIce&wind-elevation=50&site-elevation=50

The International Consortium for Agricultural Systems Applications (ICASA) format is specifically tailored for agricultural crop modeling and simulation with tools such as DSSAT. It is only available for a single point, not a region.

When requesting ICASA format, the API automatically selects the required weather parameters, regardless of the parameters selected, and sets the community to Agroclimatology (AG). For the monthly amplitude to be included in the response, please select a time period that covers at least two months.

1

/api/temporal/daily/point?parameters=T2M&community=AG&longitude=0&latitude=0&start=20170101&end=20170401&format=ICASA

###### Regional¶

Below are examples to return daily data for a region on a 0.5 x 0.5 degree grid.

1 2 3

``` bash /api/temporal/daily/regional?latitude-min=50&latitude-max=55&longitude-min=50&longitude-max=55&parameters=T2M&community=SB&start=20170101&end=20170201&format=CSV ```

---

## NASA POWER · Climatology API

- **URL:** https://power.larc.nasa.gov/docs/services/api/temporal/climatology/
- **Título de la página:** NASA POWER | Docs | Data Services | Climatology API - NASA POWER | Docs
- **Para qué sirve (según la lista):** Promedios climatológicos mensuales de largo plazo por punto.

Skip to content

### Climatology API¶

The Climatology microservice API returns time series analysis-ready data responses for solar and meteorological data to be used directly by applications.

#### Formats¶

| Formats  | Available  | Notes

| NetCDF  | Yes  |

| ASCII  | Yes  |

| ICASA  | No  |

| JSON  | Yes  |

| CSV  | Yes  |

#### Limits¶

Parameters

- A maximum of 20 parameters can currently be requested in one submission for a single point. Regional requests are limited to one parameter.
- These limits do not apply if more parameters are needed by the application to construct on the fly parameters or if a combination of parameters are selected that return multiple parameters with the same name.

Wind Elevation and Custom Surface

- This parameter is only available under the "Point" spatial option.
- Wind Elevation values in Meters are required to be between 10m and 300m.
- If you provide a correct wind surface alias, please include a surface elevation with the request.

For a list of wind surface aliases, please use this System API Request. For more information please reference the Manager Documentation.

Site Elevation

If you wish to pass your own site elevation (in meters), you will receive a corrected atmospheric pressure value upon adjustment to the elevation you provided.

- Site Elevation site-elevation values are in Meters.

#### Request Structure¶

- The request arguments can be in any order after the question mark.
- A single parameter or a list of parameters can be selected with one of the following list separators: ',' or '%2C'.

##### Examples¶

To help construct and test your API requests, please use the API Pages for the POWER Climatology API and POWER Manager API.

###### Custom Climatology¶

To request a custom climatology, just include start and end URI components like start=2016&end=2017.

SimpleASCIICSV

1

/api/temporal/monthly/climatology/point?parameters=T2M,T2M_MAX&community=SB&longitude=0&latitude=0&format=JSON&start=2016&end=2017

1

/api/temporal/monthly/climatology/point?parameters=T2M,T2M_MAX&community=SB&longitude=0&latitude=0&format=ASCII&start=2016&end=2017

1

/api/temporal/monthly/climatology/point?parameters=T2M,T2M_MAX&community=SB&longitude=0&latitude=0&format=CSV&start=2016&end=2017

###### Point¶

SimpleComplexSite ElevationWind ElevationWind SurfaceArbitrary TiltAll Operations

1

/api/temporal/climatology/point?parameters=T2M&community=SB&longitude=0&latitude=0&format=JSON

1

/api/temporal/climatology/point?parameters=T2M,PS,WS10M&community=AG&longitude=0&latitude=0&format=CSV

1

/api/temporal/climatology/point?parameters=T2M&community=SB&longitude=0&latitude=0&format=JSON&site-elevation=50

1

/api/temporal/climatology/point?parameters=T2M&community=AG&longitude=0&latitude=0&format=ASCII&wind-elevation=50

1

/api/temporal/climatology/point?parameters=T2M&community=AG&longitude=0&latitude=0&format=ASCII&wind-surface=SeaIce&wind-elevation=50

1

/api/temporal/climatology/point?parameters=SI_EF_TILTED_SURFACE&community=AG&longitude=0&latitude=0&format=ASCII

1

/api/temporal/climatology/point?parameters=T2M,PS,WS10M,SI_EF_TILTED_SURFACE&community=AG&longitude=0&latitude=0&format=ASCII&wind-surface=SeaIce&wind-elevation=50&site-elevation=50

###### Regional¶

Below are examples for returning a climatology for a region on a 0.5 x 0.5 degree grid.

1 2 3

```bash /api/temporal/climatology/regional?latitude-min=50&latitude-max=55&longitude-min=50&longitude-max=55&parameters=T2M&community=SB&format=CSV ```

---

## NASA POWER · Tutorial API

- **URL:** https://power.larc.nasa.gov/docs/tutorials/service-data-request/api/
- **Título de la página:** NASA POWER | Docs | Tutorials | API - NASA POWER | Docs
- **Para qué sirve (según la lista):** Tutorial paso a paso con ejemplos de peticiones.

Skip to content

### API Data Requests¶

This section provides code examples on how to access data from the RESTful Application Programming Interfaces (APIs). For more information on the API services, please see the API Services Section.
Guidance on Multiprocessing Download (Synchronous Requests)
When requesting data from the POWER API:

- Please ensure you do not submit too many synchronous requests. If the server determines that you are negatively impacting performance, it may block your access.
- Please ensure that you properly request data from the POWER data services at no higher than its current resolution. The POWER data products are currently available at a 0.5 x 0.625 degree resolution for meteorology and 1 x 1 for solar parameters. If you are requesting data at too high a resolution (i.e., less than 0.5 degree or about 50 km), you may be repeatedly requesting the same information.
- Within two to three (2–3) months after real-time, improved climate quality data products replace the meteorological data products. You need to take this into account when downloading the POWER Data Archive.

#### Single-Point¶

The NASA Prediction of Worldwide Energy Resources (POWER) project provides free, globally available climate data for applications in energy, agriculture, and infrastructure. This tutorial will guide you through how to:

- Understand and use the POWER application programming interface (API).
- Retrieve real-world climate data.
- Visualize data using Python.

Additional Resources

POWER API Documentation: https://power.larc.nasa.gov/docs/services/api/ Parameter Dictionary: https://power.larc.nasa.gov/parameters/

##### Guide to Download Data¶

1) Choose Your Parameters: For this tutorial, we’ll focus on solar radiation (ALLSKY_SFC_SW_DWN), which is essential for solar energy applications.

2) Define Your Location and Time Range: Phoenix, Arizona (Latitude: 33.4484, Longitude: -112.0740) and Time Range: January 1, 2020 – December 31, 2020

3) Construct the API URL:

1

/api/temporal/daily/point?parameters=ALLSKY_SFC_SW_DWN&community=RE&longitude=-112.0740&latitude=33.4484&start=20200101&end=20201231&format=JSON

Pandas (Single Point)Xarray (Single Point)

1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18

''' *Version: 1.0 Published: 2025/12/31* Source: [NASA POWER](https://power.larc.nasa.gov/) POWER API Single-Point Pandas Access This is an overview of the process to request and pandas dataframe for a point location from the POWER API. ''' import pandas as pd url = "https://power.larc.nasa.gov/api/temporal/hourly/point?parameters=T2M,ALLSKY_SFC_SW_DWN&community=RE&longitude=-112.0740&latitude=33.4484&start=20241201&end=20241231&format=csv&header=false" df = pd.read_csv(url) time_mapping = {"YEAR": "year", "MO": "month", "DY": "day", "HR": "hour"} df = df.rename(columns=time_mapping) df["time"] = pd.to_datetime(df[time_mapping.values()]) df = df.drop(columns=time_mapping.values()) df = df.set_index("time") print (df)

1  2  3  4  5  6  7  8  9 10 11 12 13 14

''' *Version: 1.0 Published: 2025/12/30* Source: [NASA POWER](https://power.larc.nasa.gov/) POWER API Single-Point Xarray Access This is an overview of the process to request and xarray dataframe for a point location from the POWER API. ''' url = "https://power.larc.nasa.gov/api/temporal/hourly/point?parameters=T2M,ALLSKY_SFC_SW_DWN&community=RE&longitude=-112.0740&latitude=33.4484&start=20241201&end=20241231&format=xarray" response = requests.get(url, verify=True, allow_redirects=True, timeout=30) response.raise_for_status() ds = xr.Dataset.from_dict(response.json()) print(ds)

#### Multi-Point¶

This is an overview of the process to request data from multiple single point locations from the POWER API.

- The code under the Loop (Points) tab below allows you to download directly from the API in any available format.
- The code under the Multiprocessing (Points) and Multiprocessing (Region) tabs supports multiprocessing and reads data from the JSON response, loading it into a Pandas DataFrame before exporting it as a CSV file. This can be modified to generate other formats using Python and/or the Pandas module.

Loop (Points)Multiprocessing (Points)Multiprocessing (Region)

1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24

''' *Version: 2.0 Published: 2021/03/09* Source: [NASA POWER](https://power.larc.nasa.gov/) POWER API Multi-Point Download This is an overview of the process to request data from multiple data points from the POWER API. ''' import os, json, requests locations = [(32.929, -95.770), (5, 10)] output = r"" base_url = r"https://power.larc.nasa.gov/api/temporal/daily/point?parameters=T2M,T2MDEW,T2MWET,TS,T2M_RANGE,T2M_MAX,T2M_MIN&community=RE&longitude={longitude}&latitude={latitude}&start=20150101&end=20150305&format=JSON" for latitude, longitude in locations: api_request_url = base_url.format(longitude=longitude, latitude=latitude) response = requests.get(url=api_request_url, verify=True, timeout=30.00) content = json.loads(response.content.decode('utf-8')) filename = response.headers['content-disposition'].split('filename=')[1] filepath = os.path.join(output, filename) with open(filepath, 'w') as file_object: json.dump(content, file_object)

1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58

''' *Version: 2.0 Published: 2021/03/09* Source: [NASA POWER](https://power.larc.nasa.gov/) POWER API Multi-Point Download This is an overview of the process to request data from multiple data points from the POWER API. ''' import os, sys, time, json, urllib3, requests, multiprocessing urllib3.disable_warnings() def download_function(collection):  ''' ''' request, filepath = collection response = requests.get(url=request, verify=False, timeout=30.00).json() with open(filepath, 'w') as file_object: json.dump(response, file_object) class Process(): def __init__(self): self.processes = 5 # Please do not go more than five concurrent requests. self.request_template = r"https://power.larc.nasa.gov/api/temporal/daily/point?parameters=T2M,T2MDEW,T2MWET,TS,T2M_RANGE,T2M_MAX,T2M_MIN&community=RE&longitude={longitude}&latitude={latitude}&start=20150101&end=20150305&format=JSON" self.filename_template = "File_Lat_{latitude}_Lon_{longitude}.csv" self.messages = [] self.times = {} def execute(self): Start_Time = time.time() locations = [(39.9373, -83.0485), (10.9373, -50.0485)] requests = [] for latitude, longitude in locations: request = self.request_template.format(latitude=latitude, longitude=longitude) filename = self.filename_template.format(latitude=latitude, longitude=longitude) requests.append((request, filename)) requests_total = len(requests) pool = multiprocessing.Pool(self.processes) x = pool.imap_unordered(download_function, requests) for i, df in enumerate(x, 1): sys.stderr.write('\rExporting {0:%}'.format(i/requests_total)) self.times["Total Script"] = round((time.time() - Start_Time), 2) print ("\n") print ("Total Script Time:", self.times["Total Script"]) if __name__ == '__main__': Process().execute()

1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62

''' *Version: 1.0 Published: 2020/02/11* Source: [NASA POWER](https://power.larc.nasa.gov/) POWER API Multipoint Download (CSV) This is an overview of the process to request data from multiple data points from the POWER API. ''' import os, sys, time, json, urllib3, requests, multiprocessing urllib3.disable_warnings() import numpy as np def download_function(collection):  ''' ''' request, filepath = collection response = requests.get(url=request, verify=False, timeout=30.00).json() with open(filepath, 'w') as file_object: json.dump(response, file_object) class Process(): def __init__(self): self.processes = 5 # Please do not go more than five concurrent requests. self.request_template = r"https://power.larc.nasa.gov/api/temporal/daily/point?parameters=T2M,T2MDEW,T2MWET,TS,T2M_RANGE,T2M_MAX,T2M_MIN&community=RE&longitude={longitude}&latitude={latitude}&start=20150101&end=20150305&format=JSON" self.filename_template = "File_Lat_{latitude}_Lon_{longitude}.csv" self.messages = [] self.times = {} def execute(self): Start_Time = time.time() latitudes = np.arange(-1.75, 1.0, 0.5) # Update your download extent. longitudes = np.arange(-1.75, 1.0, 0.5) # Update your download extent. requests = [] for longitude in longitudes: for latitude in latitudes: request = self.request_template.format(latitude=latitude, longitude=longitude) filename = self.filename_template.format(latitude=latitude, longitude=longitude) requests.append((request, filename)) requests_total = len(requests) pool = multiprocessing.Pool(self.processes) x = pool.imap_unordered(download_function, requests) for i, df in enumerate(x, 1): sys.stderr.write('\rExporting {0:%}'.format(i/requests_total)) self.times["Total Script"] = round((time.time() - Start_Time), 2) print ("\n") print ("Total Script Time:", self.times["Total Script"]) if __name__ == '__main__': Process().execute()

---

## NASA POWER · Methodology

- **URL:** https://power.larc.nasa.gov/docs/methodology/
- **Título de la página:** NASA POWER | Docs | Methodology - NASA POWER | Docs
- **Para qué sirve (según la lista):** De dónde salen los datos (MERRA-2, CERES/GEWEX), resolución y limitaciones.

Skip to content

### POWER Data Methodology¶

#### POWER Project Release History¶

The National Aeronautics and Space Administration (NASA), through its Earth Science research program, has long supported satellite systems and research providing data important to the study of climate and climate processes. These data include long-term climatologically averaged estimates of meteorological quantities and surface solar, and thermal infrared energy, or radiative, fluxes. Additionally, mean values of the base meteorological and solar data are provided in a time series format. These satellite and model-based products have proven to be sufficiently accurate to provide reliable solar and meteorological resource data over regions where surface measurements are sparse or nonexistent. The products offer two unique features: the data is global and generally contiguous in space and time. These two important characteristics tend to generate exceptionally large data archives which can be intimidating for users, particularly those with little experience or resources to explore these large data sets. Moreover, the data products contained in the various NASA archives are often in formats that present challenges to new users. To foster the usage of global solar and meteorological data, NASA’s Earth Science to Action program within the Earth Science Division supports the development and release of user-friendly data sets formulated specifically for designated user communities with access to these data via a user-friendly web-based mapping portal.

The Surface meteorology and Solar Energy (SSE) project was one of the earlier activities funded under a previous NASA Applied Science Program to foster use of NASA’s data holdings. The SSE data-delivery website was focused on providing easy access to parameters valued in the renewable energy industry and was initially released in 1997. The solar and meteorological data contained in this first release was based on the 1993 NASA/World Climate Research Program Version 1.1 Surface Radiation Budget (SRB) science data and TIROS Operational Vertical Sounder (TOVS) data from the International Satellite Cloud Climatology Project (ISCCP). Release 2 of SSE was made public in 1999 with parameters specifically tailored to the needs of the renewable energy community. Subsequent releases of SSE (SSE-Release 3.0 in 2000, SSE-Release 4.0 in 2003, SSE-Release 5.0 in 2005, and SSE-Release 6.0 in 2008) have continued to build upon an interactive dialog with potential customers resulting in updated parameters using the most recent NASA data as well as inclusion of new parameters that have been requested by the user community.

The POWER Project was initiated in 2002 as an outgrowth of the SSE project. The initial POWER Project encompassed the SSE component and added two new data sets with applicability to the architectural (e.g. Sustainable Buildings) and agricultural (e.g. Agroclimatology) industries, with the continuing objective of improvements to and expansion of the focused parameters included in each section of POWER.

Upgrades to the SSE component of POWER included adding Geographic Information System (GIS) functionality to the data ordering/access process. SSE-GIS constituted the Release 7.0 version, but also provided updated data sets.

POWER Release 8 aggregated the three focused data components of POWER: SSE, Sustainable Building, and Agroclimatology into a new responsive data portal designed to fit on desktop, tablet, and smart phone platforms. Additional upgrades included geospatially enabled online tools to facilitate data ordering, viewing, and analysis of the solar and meteorological data. The meteorological data/parameters in POWER Release 8 were based upon Goddard’s Global Modeling and Assimilation Office (GMAO) Modern Era Retrospective-Analysis for Research and Applications (MERRA-2) assimilation model products and GMAO Forward Processing – Instrument Teams (FP-IT) GEOS 5.12.4 near-real time products. MERRA-2 data spans the time period from 1981 to within several months of real time; GEOS 5.12.4 data covers the time period from the end of the MERRA-2 data stream to within several days of real time. MERRA-2 and GEOS 5.12.4 algorithm versions are essentially the same which results in minimal discontinuities between the different assimilation models. The solar based data/parameters in POWER Release 8 were based upon satellite observations with subsequent inversion to surface solar insolation by NASA’s Global Energy and Water Exchange Project (GEWEX) /Surface Radiation Budget (SRB) Release 3 and NASA’s CERES Fast Longwave And Shortwave Radiative project (FLASHFlux).

POWER Release 9 built upon the data portal established with Release 8, but added data releases from NASA's SRB Release 4, CERES SYN1deg, and FLASHFlux Version 4A. The data/parameters in POWER Release 9 are provided on a global grid with spatial resolutions equal to the input data. That resolution is 1.0° latitude by 1.0° longitude for the radiation data sets and ½° latitude by ⅝° longitude for the meteorological data sets. The grid reference system is WGS84. An additional improvement over previous version is the inclusion of hourly data for certain parameters.

##### POWER Release 10¶

POWER Release 10 enhances the data pipeline by fully migrating to a cloud-based data processing pipeline. Each source has an independent data processing pipeline implementing improvements, decreasing processing latencies, improving temporal coverage, and much more.

Meteorological parameters continue to be based upon MERRA-2 and GEOS FP-IT assimilation models.

Sections under "Data Sources and Validation", listed in the left menu in this methodology, provide summaries of the sources and estimated uncertainty associated with the data underlying the solar and meteorological parameters available through POWER. The uncertainty estimates are based upon comparisons with surface measurements. Additionally, procedures for computing value-added parameters are detailed under the "Derived and Adjusted Data" heading in the left menu.

##### High-Resolution Sources¶

POWER integrates several higher-resolution NASA sources alongside the primary archive. These are exposed through the High-Resolution toggle in the DAV and through dedicated parameter aliases in the API.

| Source  | Domain  | Resolution  | Temporal Start  | Temporal End

| IMERG  | Precipitation  | 0.1° (~10 km), daily UTC  | June 1, 1998  | Near Real Time

| SMAP L4  | Soil Moisture  | ~0.09° (~9 km), daily UTC  | 31 March 2015  | Near Real Time

| NEX-GDDP-CMIP6  | Future Climate  | ~0.25° (~25 km), daily  | 2015  | 2100

#### Components¶

While many of the sources of POWER data contain parameters that cross these boundaries of component type, the following links give overviews of the sources and parameters:

| Component  | Description

| Energy Fluxes  | Solar and thermal-IR radiative fluxes (CERES SYN1deg, FLASHFlux, GEWEX SRB R4-IP).

| Meteorology  | Surface meteorological parameters (MERRA-2, GEOS-IT).

| Clouds and Aerosols  | Auxiliary parameters like cloud amount and atmospheric aerosols. (CERES SYN1deg, TEMPO)

| Hydrology  | Surface water-cycle data (GWM, SMAP, HydroSCS, MERRA-2, GEOS-IT,!--IMERG→).

| Future Projections  | Downscaled CMIP6 future projections curated by NASA's RASI workgroup (NEX-GDDP).

---

## NASA POWER · Application APIs

- **URL:** https://power.larc.nasa.gov/docs/services/api/application/
- **Título de la página:** NASA POWER | Docs | Data Services | Application APIs - NASA POWER | Docs
- **Para qué sirve (según la lista):** APIs auxiliares (p. ej. consulta de parámetros disponibles).

Skip to content

### Application APIs¶

The Application APIs that return user community specific Analysis Ready Data (ARD) products.

| Services  | Description

| Indicators  | Create an ASHRAE Climate Indicators report from a custom location and time range.

| Windrose  | Create a Windrose data table for a custom location and time range.

| Zones  | Pull Thermal and Thermal Moisture Zone operations from a custom location and time range.

| Insights  | Insights that apply to a whole specified region.

#### Formats¶

Below you will find an overview of the output Formats available for the Application APIs. For more information, please reference the specified Application APIs pages.

| Services  | HTML  | PDF  | JSON  | CSV  | ASCII  | XLSX  | NetCDF  | Other

| Indicators  | Yes  | No  | Yes  | No  | No  | Yes  | No  | No

| Windrose  | No  | No  | Yes  | Yes  | Yes  | No  | No  | No

| Zones  | No  | No  | Yes  | No  | No  | No  | Yes  | No

| Insights  | Yes  | No  | Yes  | No  | No  | No  | No  | Yes
