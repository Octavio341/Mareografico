from datetime import timedelta
import pandas as pd
import datetime 
import sys 

import os 
anio = 0
def es_bisiesto(anio):
    resto = anio % 4
    print("-------- dentro de la funcion  --------  ")
    print("resultado de la primera  ",resto)
    if resto == 0:
        resto = anio % 100
        print("resultado con 100",resto)
        if resto == 0:
            resto = anio % 400
            if resto == 0:
                return True
            else:
                return False
        else:
            print("es bisiesto")
            return True
    else:
        print("no es bisiesto")
        return False
    
    
es_bisiesto(anio)
print("¿es bisiesto?",es_bisiesto(anio))


print("-------------------------------------------")

###
# entra el primer archivo
###
if len(sys.argv) < 2 :
    print("R- python archivo.py _ falta el nombre del archivo a analizar")
    quit() #para salir del programa
else:
    print("-- Usted a ingresado lo siguiente --")
    print(sys.argv[0],sys.argv[1])

nombre_archivo = sys.argv[1]
print("R- el archivo a analizar se llama", nombre_archivo)

matriz_toga = pd.read_table(nombre_archivo,sep=r"\s+",names=
                            ["IDEstacion",
                             "Lugar",
                             "Fecha",
                             "D1",
                             "D2",
                             "D3",
                             "D4",
                             "D5",
                             "D6",
                             "D7",
                             "D8",
                             "D9",
                             "D10",
                             "D11",
                             "D12"],engine='python',skiprows=1)
print ("Esta es la matriz toga")
print(matriz_toga) # creamos la tabla 

fecha = str(matriz_toga["Fecha"].iloc[0])

print("R- se ha extraido la fecha ----",fecha[0:4],"-",fecha[4:6],fecha[6:8])


print("===============[ INICIO DE ANALISIS DE DATOS]===========================")

###################################################
############ ANÁLISIS DE DATOS ###################
###################################################

print("comprobando que el archivo contenga el numero adecuado de lineas de datos")

#Calcular cuantas lienas de datos se esperan 

if es_bisiesto(int(fecha[:4])): # esto me toma el año y lo verificamos si es bisiesto

    dias_esperados = 366 * 2 #  esto da como resultado  732

else:# si no es bisiesto
    dias_esperados =  365 * 2 #  esto da como resultado  730

if len(matriz_toga.index) == dias_esperados:
    print("R-los dias son iguales")

else:
    print("R- los dias no son iguales")
    print("se esperaban",dias_esperados,"por el total de lineas de datos contados "+str(len(matriz_toga.index)))
    sys.exit(1)




