import argparse
import material
import numpy as np
import group2
#Definition of the arguments of the script  
parser = argparse.ArgumentParser(description= ' develops an API to collect data from user',exit_on_error=False)
parser.add_argument('--latitude', type = float , help='provide the latitude')
parser.add_argument('--longitude', type = float, help='provide the longitude')
parser.add_argument('--soiltype', type = int, help='provide the Soiltype')
parser.add_argument('--pFCritical', type = float, help='provide the soil tension from which there is plant specific stress')
parser.add_argument('--Next24Rain_treshold', type = float, help='provide the the ammount of rain forecasted in the next 24h')
parser.add_argument('--VPD_treshold', type = int, help='provide the Vapour Pressure Deficit')
try:
     args = parser.parse_args() 
except argparse.ArgumentError:
    print('Catching an argumentError')
#Consider the group1 results
inLat = material.Output1Group1['inlat']
inLon = material.Output1Group1['inlon']
inSoilType = group2.get_pF_forecast['inSoilType']
inpFCritical  = group2.get_pF_forecast['inpFCritical']
invpd_treshold = material.Output1Group1['invpd_treshold']
innext24h_rain_treshold = material.Output1Group1['innext24h_rain_treshold']
# 1 -Organize your user input data for easier reading
inLat                     = 37.64 # replace this value with what you collect with your API
inLon                     = -7.66 # replace this value with what you collect with your API
inSoilType                = 1 # replace this value with what you collect with your API
inpFCritical              = 3.1 # replace this value with what you collect with your API
invpd_treshold            = 0.5 # replace this value with what you collect with your API
innext24h_rain_treshold   = 2 # replace this value with what you collect with your API
# 2 - Create a dictionary of weather forecast with the group1 work. In the meantime you can use material.Output1Group1 as a mockup result
Forecast = material.Output1Group1
# 3 - Organize your data series
dates = Forecast['hourly']['time']
dates = list(map(lambda x: x[-8:-3], dates))# just to get the Day and Hour
#... continue to create the following lists and populate them with forecasted data
temp = material.Output1Group1['temperature'] # replace the empty list with result of group1 work
vpd = [] # replace the empty list with result of group1 work
rh = material.Output1Group1['relativehumidity_2m'][:] # replace the empty list with result of group1 work
ETo = [] # replace the empty list with result of group1 work
precipitation = material.Output1Group1['precipitation'][:] # replace the empty list with result of group1 work
SoilMoisture_3_9 = material.Output1Group1['soil_moisture_3_9cm'][:] # replace the empty list with result of group1 work
SoilMoisture_9_27 = material.Output1Group1['soil_moisture_3_9cm'][:] # replace the empty list with result of group1 work
# 4 Use group2 function to create the soil tension (pF) dataseries for the two soil layers. 
pF_3_9=group2.soil_pF['inpFCritical '][] # replace the empty list with result of group2 work
pF_9_27=[] # replace the empty list the list with result of group2 work
#Decision to irrigate ( 3-9 cm)
plan_3_9 = [0] * len(dates) # replace the empty list with a list with same nr elements as 'dates', but filled with zeros
plan_9_27 = [0] * len(dates) # replace the empty list with a list with same nr elements as 'dates', but filled with zeros
plan_3_9_dates = [] # leave as is. This list will store the irrigation event for this soil layer
plan_9_27_dates = [] # leave as is. This list will store the irrigation event for this soil layer
# Decision algorithm to trigger irrigation event - Improve if you feel it nees improvement
# Rules: 1) soil tension is higher than pFCritical, 2) VPD is higher than vpd_treshold, 3) the sum of rain in the next 24 hours is less than 1 liter per m2
for idx,i in enumerate(vpd):
    next24_rain = sum(precipitation[idx:idx+24])
    if pF_3_9[idx]>=inpFCritical and vpd[idx] > invpd_treshold and next24_rain < innext24h_rain_treshold:
        if sum(filter(None, plan_3_9))<1:
            plan_3_9[idx] = 1
            plan_3_9_dates.append(dates[idx])
    if pF_9_27[idx]>=inpFCritical and vpd[idx] > invpd_treshold and next24_rain < innext24h_rain_treshold:
         if sum(filter(None, plan_9_27))<1:
            plan_9_27[idx] = 1
            plan_9_27_dates.append(dates[idx])