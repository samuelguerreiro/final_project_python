import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator)
import numpy as np
import material
import argparse
import group1_output
#import group2_output #falta criar este ficheiro ainda (para a pergunta 4)


parse = argparse.ArgumentParser (description = "insert data")
parse.add_argument ("latitude", type = float, metavar = "lat", help = "latitude to analyse")
parse.add_argument ("longitude", type = float, metavar = "lon", help = "longitude to analyse")
parse.add_argument ("soiltype", type = int, metavar = "stype", help = "soil type to analyse")
parse.add_argument ("pFCritical", type = float, metavar = "pF", help = "pF critical to analyse" )
parse.add_argument ("next24rain_treshold", type = float, metavar = "24rain", help = "next24rain_treshold to analyse")
parse.add_argument ("VPD_treshold", type = float, metavar = "VPD", help = "VPD_treshold to analyse")

#The endpoint (Group 3) develops an API to collect data from user with argparse:
#Latitude - in decimal degrees
#Longitude - in decimal degrees
#Soiltype - an integer 1-5 corresponding to the 5 FAO soil textural classes 1-5 FAO class (1-coarse, 2-Medium, 3-Medium-Fine, 4-Fine, 5-Very Fine)
#pFCritical - the soil tension from which there is plant specific stress (pF at field capacity:2.3, pF at wilting point:4.2)
#Next24Rain_treshold - the ammount of rain forecasted in the next 24h, that could prevent the irrigation event
#VPD_treshold - Vapour Pressure Deficit, below which transpiration is unlikely to occur 

#test your application with
#Latitude - 37.64
#Longitude - -7.66
#Soiltype - 3
#pFCritical - 3.1
#Next24Rain_treshold - 2
#VPD_treshold - 0.5

try:
     arguments = parse.parse_args() 
except argparse.ArgumentError:
    print('Catching an argumentError')

inLat                     = arguments.latitude # replace this value with what you collect with your API
inLon                     = arguments.longitude # replace this value with what you collect with your API
inSoilType                = arguments.soiltype # replace this value with what you collect with your API
if inSoilType < 1 and inSoilType > 5: #acrescentamos este if para que só corra se SoilType entre 1 e 5 (condição do enunciado)
    raise TypeError ("The soil type is not valid")
    exit()

inpFCritical              = arguments.pFcritical # replace this value with what you collect with your API
invpd_treshold            = arguments.VPD_treshold # replace this value with what you collect with your API
innext24h_rain_treshold   = arguments.next24rain_treshold # replace this value with what you collect with your API


# 1 -Organize your user input data for easier reading (isto é o que vem do imput)
#inLat                     = 37.64 # replace this value with what you collect with your API
#inLon                     = -7.66 # replace this value with what you collect with your API
#inSoilType                = 1 # replace this value with what you collect with your API
#inpFCritical              = 3.1 # replace this value with what you collect with your API
#invpd_treshold            = 0.5 # replace this value with what you collect with your API
#innext24h_rain_treshold   = 2 # replace this value with what you collect with your API

# 2 - Create a dictionary of weather forecast with the group1 work. In the meantime you can use material.Output1Group1 as a mockup result
Forecast = group1_output.getHourlyWeatherForescast(inLat,inLon) #(output 1 vai devolver o dicionário; em material.py está o output que é suposto o grupo 1 mobter, podem,os usalo))
print (Forecast)

# 3 - Organize your data series
dates = Forecast['hourly']['time']
dates = list(map(lambda x: x[-8:-3], dates))# just to get the Day and Hour
#... continue to create the following lists and populate them with forecasted data
temp = Forecast['temperature'] # replace the empty list with result of group1 work
vpd = Forecast['vapor_pressure_deficit'] # replace the empty list with result of group1 work
rh = Forecast['relativehumidity_2m'][:] # replace the empty list with result of group1 work
ETo = Forecast['et0_fao_evapotranspiration'] # replace the empty list with result of group1 work
precipitation = Forecast['precipitation'][:] # replace the empty list with result of group1 work
SoilMoisture_3_9 = Forecast['soil_moisture_3_9cm'][:] # replace the empty list with result of group1 work
SoilMoisture_9_27 = Forecast['soil_moisture_9_27cm'][:] # replace the empty list with result of group1 work


# 4 Use group2 function to create the soil tension (pF) dataseries for the two soil layers. 

#O que está abaixo ainda falta o output, por isso comentámos. depois do output tirar o cardinal
#pF_3_9= group2_output.get_pF_forecast(SoilMoisture_3_9, inSoilType) # replace the empty list with result of group2 work
#pF_9_27= group2_output.get_pF_forecast(SoilMoisture_9_27, inSoilType) # replace the empty list the list with result of group2 work

#Decision to irrigate ( 3-9 cm)
plan_3_9 = [0] * len(dates) # replace the empty list with a list with same nr elements as 'dates', but filled with zeros
plan_9_27 = [0] * len(dates) # replace the empty list with a list with same nr elements as 'dates', but filled with zeros
plan_3_9_dates = [] # leave as is. This list will store the irrigation event for this soil layer
plan_9_27_dates = [] # leave as is. This list will store the irrigation event for this soil layer

