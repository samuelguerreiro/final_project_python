import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator) #para localizar e formatar o desenho de uma função
import numpy as np
import material #output dop grupo 1 antes o receber
import argparse #tb existe o matplotlib._api mas não é para user, é para gerir a API (argparse é p dados do utilizador, para criar apenas, não gere)
#argparse é argument parse e usamos p tratar o imput dado pelo utilizador
import group1_output
#import group2_output #falta criar este ficheiro ainda (para a pergunta 4)Samuel
import math

parse = argparse.ArgumentParser (description = "insert data") #criar o parser ("separador/analisador"); serve para o utilizador saber os dados que deve dar e depois tratá-los; p o utilzarod r«perceber o que é necessário
parse.add_argument ("latitude", type = float, metavar = "lat", help = "latitude to analyse") # a msg do help aparece quando o utilizador na powershell o colicita, com "-h"; escrever "python group3_SAMUEL_try.py -h" para visualizar
parse.add_argument ("longitude", type = float, metavar = "lon", help = "longitude to analyse")
parse.add_argument ("soiltype", type = int, metavar = "stype", help = "soil type to analyse: 1-coarse, 2-medium, 3-medium-fine, 4-fine, 5-very fine") 
parse.add_argument ("pFCritical", type = float, metavar = "pF", help = "pF critical to analyse")
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

try:# para tentar correr o codigo dentro do try e gerar uma exceção se o programa falhar/não conseguir abrir os argumentos
     arguments = parse.parse_args() 
except argparse.ArgumentError:
    print('Catching an argumentError')

#substituimos valores com o que guarsamos do parser ( o que o utilizador nos fornceceu); o in é input:
inLat                     = arguments.latitude # replace this value with what you collect with your API
inLon                     = arguments.longitude # replace this value with what you collect with your API
inSoilType                = arguments.soiltype # replace this value with what you collect with your API
if inSoilType < 1 and inSoilType > 5: #acrescentamos este if para que só corra se SoilType entre 1 e 5 (condição do enunciado)
    raise TypeError ("The soil type is not valid")
    exit()

inpFCritical              = arguments.pFCritical # replace this value with what you collect with your API
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
#inlat e inlon são dados pelo utilizador. estamos ausar a função criada pelo grupo 1 para fazer um dicionário personalizado para os imputs que recebermos do tuilizador

# 3 - Organize your data series
dates = Forecast['hourly']['time'] #entra no dicionário com duas chaves, hora e tempo; as fduas são necessarias p+ chegar ao valor certo, pq 1h tem varios minutos
dates = list(map(lambda x: x[-8:-3], dates))# just to get the Day and Hour; ficaria no formato 18T14, sendo 18 o dia e 14 os minutos, como vemos no output (ver figura no end.point fornecido pelo prof e convem po -la na apresentação); percorre os valores e corta-os entre as posições -3 e -8 da propria variável (i.e. vai a cada uma das posições e guarda-as recortadas)
#... continue to create the following lists and populate them with forecasted data
temp = Forecast['temperature'] # replace the empty list with result of group1 work
vpd = Forecast['vapor_pressure_deficit'] # replace the empty list with result of group1 work
rh = Forecast['relativehumidity_2m'] # replace the empty list with result of group1 work
ETo = Forecast['et0_fao_evapotranspiration'] # replace the empty list with result of group1 work
precipitation = Forecast['precipitation'] # replace the empty list with result of group1 work
SoilMoisture_3_9 = Forecast['soil_moisture_3_9cm'] # replace the empty list with result of group1 work
SoilMoisture_9_27 = Forecast['soil_moisture_9_27cm'] # replace the empty list with result of group1 work
Soils = Forecast["soils"] [inSoilType] #criamos um dicionario para as carateristicas do tipo de solo que recebemos como argumento do utilizador


# 4 Use group2 function to create the soil tension (pF) dataseries for the two soil layers. 

#####O que está abaixo ainda falta o output, por isso comentámos. depois do output tirar o cardinal
#pF_3_9= group2_output.get_pF_forecast(SoilMoisture_3_9, inSoilType) # replace the empty list with result of group2 work
#pF_9_27= group2_output.get_pF_forecast(SoilMoisture_9_27, inSoilType) # replace the empty list the list with result of group2 work

#Decision to irrigate ( 3-9 cm)
plan_3_9 = [0] * len(dates) # replace the empty list with a list with same nr elements as 'dates', but filled with zeros
plan_9_27 = [0] * len(dates) # replace the empty list with a list with same nr elements as 'dates', but filled with zeros
plan_3_9_dates = [] # leave as is. This list will store the irrigation event for this soil layer
plan_9_27_dates = [] # leave as is. This list will store the irrigation event for this soil layer

# Decision algorithm to trigger irrigation event - Improve if you feel it nees improvement
# Rules: 1) soil tension is higher than pFCritical, 2) VPD is higher than vpd_treshold, 3) the sum of rain in the next 24 hours is less than 1 liter per m2

#foi retirado do materiual.py e serve p calcular o pF de cada tipo de solo:
def get_mSoil(nSoil):
    return 1-1/nSoil
def get_pF(Theta, alpha, Thetar, Thetas,nSoil ):
    mSoil=get_mSoil(nSoil)
    psi_part1 = 1/alpha
    if ((Theta  - Thetar)/(Thetas-Thetar)) <0:
        return (4.2)    
    psi=(1/alpha)*((((Theta-Thetar)/(Thetas-Thetar))**(-1/mSoil))-1)**(1/nSoil)
    if ( psi <= 0):
        pF = 0
    else:
        pF=math.log(psi,10)
    
    return pF

# criamos as listas com os niveis de pF para cada uma das prof. recorrendo a função para este caçlculo dispo. p prof.; o indice que usamos é a posição de cada uma das datas na sua lista:
# resultado supostamente obtido pelo grupo 2 (não tinhamos de o fazer):
pF_3_9 = []
for i in range(0, len(dates)):
    pF_3_9 [i] = get_pF(SoilMoisture_3_9[i], Forecast["soils"] [inSoilType] ["alpha"],  Forecast["soils"] [inSoilType] ["thetar"],  Forecast["soils"] [inSoilType] ["thetas"],  Forecast["soils"] [inSoilType] ["nsoil"])

pF_9_27 = []
for i in range(0, len(dates)):
    pF_9_27 [i] = get_pF(SoilMoisture_9_27[i], Forecast["soils"] [inSoilType] ["alpha"],  Forecast["soils"] [inSoilType] ["thetar"],  Forecast["soils"] [inSoilType] ["thetas"],  Forecast["soils"] [inSoilType] ["nsoil"])


for idx,i in enumerate(vpd):
    next24_rain = sum(precipitation[idx:idx+24])
    if pF_3_9[idx]>=inpFCritical and vpd[idx] > invpd_treshold and next24_rain < innext24h_rain_treshold:
        if sum(filter(None, plan_3_9))<1:
            plan_3_9[idx] = 1
            plan_3_9_dates.append(dates[idx]) #fazemos o planeamento das proximas regas; no grafico a linha a vermelha é a posição 0 desta listya (i.e. a próxima)
    if pF_9_27[idx]>=inpFCritical and vpd[idx] > invpd_treshold and next24_rain < innext24h_rain_treshold:
         if sum(filter(None, plan_9_27))<1:
            plan_9_27[idx] = 1
            plan_9_27_dates.append(dates[idx])

# o codigo abaixo dá as imagens que esta no end.point_ressult (usar isso). mostrar o schema e dizer no fim o que aprendemos com isto: com determoinadas funções e impuits de dados reauis com«nseguimos planear e visualizar graficamente resoluções para problemas quotidiano.
# na intro dizer o objetivo (tratar dados e visualizar, mostrando o schema)


            # you don't want to worry about this section - only that it needs the variables
###################################################### VISUALIZATION ################################################
       
fig, axs = plt.subplots(2,2,sharex=True)
fig.suptitle('Green DS Master - Decision Support tool for irrigation needs. Current weather & soil retrieved from open-meteo.com\n'+
             'Irrigation criteria: pF > ' + str(inpFCritical) + ", VPD > " + str(invpd_treshold)+ ", no rain next day that allows pF < " + str(inpFCritical) + "\n"+
             "Next irrigation event for early rooting (3-9cm):" + str(plan_3_9_dates[0]) + "\n"+
             "Next irrigation event for established roots (9-27cm):" + str(plan_9_27_dates[0]) )
fig.set_size_inches(12,5)
axs[0,0].set_title('Temperature / VPD')
axs[0,0].plot(dates, temp, color='orange', label='Temp')
axs[0,0].set_ylabel('Celsius', color='orange')
secax_0_0 = axs[0,0].twinx()  # instantiate a second axes that shares the same x-axis
secax_0_0.plot(dates, vpd, color='blue')
secax_0_0.set_ylabel('VPD (kPa)', color='blue')
secax_0_0.fill_between(dates, vpd, invpd_treshold,  where=(np.array(vpd) >= np.array([invpd_treshold] * len(vpd))),
                 alpha=0.30, color='blue', label='VPD > '+str(invpd_treshold))
axs[0,0].legend(loc='upper left', frameon=False)

axs[0,1].set_title('EvapoTranspiration/Rain/Rel Hum')
axs[0,1].plot(dates, ETo, color='red',label='ETo')
axs[0,1].bar(dates, precipitation, color='blue',label='Rain')
axs[0,1].set_ylabel('ETo,Rain (mm)', color='black')
axs[0,1].legend(loc='upper right', frameon=False)
secax_0_1 = axs[0,1].twinx()  # instantiate a second axes that shares the same x-axis
secax_0_1.plot(dates, rh, color='magenta',label='RH')
secax_0_1.set_ylabel('Rel Hum (%)', color='magenta')
secax_0_1.legend(loc='upper right', frameon=False)

axs[1,0].set_title('Soil Moisture 3 to  9cm')
axs[1,0].plot(dates, SoilMoisture_3_9 , color='black', label='Soil moisture (3-9)')
secax_1_0 = axs[1,0].twinx()  # instantiate a second axes that shares the same x-axis
secax_1_0.plot(dates, pF_3_9, color='orange',label='pF')
secax_1_0.bar(dates, [x * inpFCritical for x in plan_3_9], color='red',label='Next irrigation', linewidth=3)
secax_1_0.set_ylabel('pF log(-h)', color='orange')
secax_1_0.tick_params(axis='y', colors='orange')
secax_1_0.plot(dates, [inpFCritical] * len(dates), color='orange',label='Critical pF', linestyle='dashed')
secax_1_0.set_ylim([min(pF_3_9)*0.97, max(pF_3_9)*1.03]) # just for scale purposes
axs[1,0].set_ylabel('% vol', color='black')
axs[1,0].legend(loc='upper right', frameon=False)



axs[1,1].set_title('Soil Moisture, 9 to 27 cm')
axs[1,1].plot(dates, SoilMoisture_9_27, color='black', label='Soil moisture (9-27)')
axs[1,1].set_ylabel('% / % ', color='black')
axs[1,1].legend(loc='upper right', frameon=False)
secax_1_1 = axs[1,1].twinx()  # instantiate a second axes that shares the same x-axis
secax_1_1 .plot(dates, pF_9_27, color='orange',label='pF')
secax_1_1.set_ylabel('pF log(-h)', color='orange')
secax_1_1 .plot(dates, [inpFCritical] * len(dates), color='orange',label='Critical pF', linestyle='dashed')
secax_1_1.bar(dates, [x * inpFCritical for x in plan_9_27] , color='red',label='Next irrigation', linewidth=3)
secax_1_1.set_ylim([min(pF_9_27)*0.97, max(pF_9_27)*1.03]) # just for scale purposes

secax_1_1.legend(loc='upper left', frameon=False)

axs[1,0].tick_params(axis='x', labelrotation=60)
axs[1,0].xaxis.set_major_locator(MultipleLocator(12))
axs[1,0].set_xlabel('DayHour')
axs[1,1].tick_params(axis='x', labelrotation=60)
axs[1,1].xaxis.set_major_locator(MultipleLocator(12))
axs[1,1].set_xlabel('DayHour')

# adding Label to the y-axis
#plt.autoscale(enable=True, axis='both', tight=True)
plt.tight_layout()
# adding legend to the curves
plt.legend()
plt.show()