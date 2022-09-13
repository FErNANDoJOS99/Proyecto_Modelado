from importlib import import_module
from re import S
import requests
import time 
import pandas as pd   ## pd es el objeto sque se creo con pandas
pd._version  
import numpy as np
from functools import lru_cache
#lru_cache es un decorador??
#functools es un modulo ???

diccionario_ABC={}
diccionario_Weathers={}



datos=pd.read_csv('dataset1.csv',header=0)  ## header es igual al encabezado de la primer fila 
origin=datos['origin'] 
destine=datos['destination']


# Con esto hago un conjunto con puras siglas IATA  

conjunto =set()
conjunto={""}
for i in range(0,len(origin)):
    conjunto.add(origin[i])
for i in range(1,len(destine)-1):
    conjunto.add(destine[i])


origin_latitude=datos['origin_latitude']
origin_longitude=datos['origin_longitude']
destin_latitude=datos['destination_latitude']
destin_longitude=datos['destination_longitude']



'''
Busca las coordeanadas segun la IATA
ABC Las claves IATA que estan en el conjunto 
coleccion1 = La columna de todos los lugares de IATA
coleccion2 =la columna de latitudes
coleccion3 =la columna de longitudes

'''

def search_coord(ABC,coleccion1,coleccion2,coleccion3):
    indice=0
    for i in coleccion1:
        
        if i==ABC:
           return   [coleccion2.iloc[indice],coleccion3[indice]]                         

        indice =indice+1 
    return []







## Hace un diccionario con claves IATA y por contenido un 
## string con latitud y longitud 

def maker_dict(ABC,latitude,altitude,dict):
    dict[ABC]=[latitude,altitude]
    

for i in conjunto :
        coordenada=search_coord(i,origin,origin_latitude,origin_longitude)
        if coordenada==[]:
            coordenada=search_coord(i,destine,destin_latitude,destin_longitude)
        if len(coordenada)==2:
            maker_dict(i,coordenada[0],coordenada[1],diccionario_ABC)




##@lru_cache()    ## alparecer si pongo esto se guarda en el cache el return  del metodo llamado
def request_Api_OpenW(lati1,longi1):
    diccionario_temp={}
 
    url="https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid=d1611b9fdfa424b8749ea02becc6d1c8".format(lati1,longi1)
    res =requests.get (url)   #le habla a la API  para que la analizen 

    data =res.json()  #con este comando se hace que la informacion que mando la API este mejor estructurada y asi manipulas mejor 

    temp=data ["main"]["temp"]  # se pone asi porque temp esta dentro del diccionario main 
    wind_speed =data["wind"]["speed"]
    
    latitude =data ["coord"]["lat"]
    longitude =data ["coord"] ["lon"]
    description =data ["weather"][0]["description"]  # Description es una lista por eso se ponde desde cero 
    name=data ["name"]
    
    print("Espere ,cargando informacion")
    '''
     print("nombre de la ciudad ",name)
    print("temperature",temp)
    print("Velocidad del viento:",wind_speed,"m/s")
    print("latitude:",latitude)
    print ("longitud:",longitude)
    print("description:",description)

    
    '''

    diccionario_temp={"nombre":name,"temperatura":temp,"viento":wind_speed,"latitude":latitude,"longitud":longitude,"description":description}
    return diccionario_temp







'''

 Hace las llamadas con las direcciones se salen del IATA que estan en el diccionario_ABC
 y los valores de la solucitud los guarda en un diccionario llamado 
 diccionario_Weathers

'''

def seacher_Weather():
    contador=0

    for i in diccionario_ABC:
        print("\n",contador,"\n")
        diccionario_Weathers[i]=request_Api_OpenW(diccionario_ABC[i][0],diccionario_ABC[i][1])
        contador=contador+1



 
 

## Es para imprimir el diccionario de una forma bonita 
def drawing_Coordenada(dict1=diccionario_Weathers,clave="0"):
    if clave!="0":
        info=dict1[clave]
    else:info=dict1
    nombre=info["nombre"]
    temperatura=info["temperatura" ]
    viento=info["viento"]
    latitude=info["latitude"] 
    longitude=info["longitud"]
    description=info[ "description"]   

    print("El nombre de la ciudad es ",nombre)
    print("temperature",temperatura)
    print("Velocidad del viento:",viento,"m/s")
    print("latitude:",latitude)
    print ("longitud:",longitude)
    print("description:",description)
    print("\n")
    
    







def put_out_everything():
   
 
    for i in range(0,len(destine)):
        j=origin[i]
        k=destine[i]
        print("Clima  de origen  ",j,"  " )
        drawing_Coordenada(diccionario_Weathers,j)
        print("\nClima  de destino ",k," ")
        drawing_Coordenada(diccionario_Weathers,k)
        print("\n\n\n Registro ",i," #####################\n")

        

        


    
print("Tienes 2 opciones ")
print("Buscar una IATA en especifico")
print("Ver todo los horarios de vuelo con su destino ")
i=input ("Escoge  1 o 2 \n")
if "2"<i<"1":
    print("No escogiste opcion correcta ")
else:
    if i=="1":
        iata =input ("Escribe la IATA\n") 
        coordenadas1=diccionario_ABC[iata]   
        print(coordenadas1)
       # print(request_Api_OpenW(coordenadas1[0],coordenadas1[1]))
        drawing_Coordenada(request_Api_OpenW(coordenadas1[0],coordenadas1[1]))
    
    if i=="2":
        seacher_Weather()
        put_out_everything()















