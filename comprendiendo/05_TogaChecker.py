from PyQt5 import QtWidgets, QtGui
import matplotlib.pyplot as plt
import sys, ntpath, os
import pandas as pd
import datetime
import numpy as np

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
print("ejecutando: 05_TogaChecker.py ")


# Funci'on que lee el archivo TOGA, grafica los datos y muestra la grafica en la ventana
#def plotToga():
   # filename = QtWidgets.QFileDialog.getOpenFileName(win, "Seleccione el archivo TOGA...", filter="Archivos DAT (*.dat)")

    #nombre_archivo=str(filename[0])
    #return nombre_archivo


    # Leer el archivo de datos
nombre_archivo=sys.argv[1]
matriz_toga = pd.read_table(nombre_archivo, sep=r'\s+', names = ["StationID", "StationName", "Date", "D1", "D2", "D3","D4", "D5", "D6", "D7", "D8", "D9", "D10", "D11", "D12"], engine = 'python', skiprows = 1, na_values = "9999")

print("nombre del dato",nombre_archivo)
print("")
matriz= matriz_toga.iloc[:,3:].dropna()
tamano= matriz.size
print('La cantidad de datos del archivo es de: ',tamano)

fecha = str(matriz_toga["Date"][1])
print("Fecha de los datos",fecha[:4])
resto = int(fecha[:4])%4
   
if resto == 0:
    resto2 = int(fecha[:4])%100

    if resto2 == 0:
        resto3 = int(fecha[:4])%400

        if resto3 == 0:
            print('Es bisiesto') 

            if tamano == 8784:
                print('La cantidad de datos esta completa')
            else:
                print('La cantidad de datos esta incompleta','...', 'Faltan', 8784-tamano)


        else:
            print('No es bisiesto')
            
            if tamano == 8760:
                print('La cantidad de datos esta completa')
            else:
                print('La cantidad de datos esta incompleta','...', 'Faltan', 8760-tamano)

    else:
        print('Es bisiesto')
        
        if tamano  == 8784:
            print('La cantidad de datos esta completa')
        else:
            print('La cantidad de datos esta incompleta','...', 'Faltan', 8784-tamano)

else:
    print('No es bisiesto')
    
    if tamano == 8760:
        print('La cantidad de datos esta completa')
    else:
        print('La cantidad de datos esta incompleta','...', 'Faltan', 8760-tamano)

fechas_dat_incom= list()

#Procesar l'inea por linea del dataframe 
for ind in matriz_toga.index:

    fecha = str(matriz_toga["Date"][ind])

    if fecha[8:9] == "1":
        fecha_inicial = datetime.datetime(int(fecha[:4]), int(fecha[4:6]), int(fecha[6:8]))
    else:
        fecha_inicial = datetime.datetime(int(fecha[:4]), int(fecha[4:6]), int(fecha[6:8]), 12)

    # Cargar los 12 datos de la fila de datos
 #   for dat in ["D1", "D2", "D3", "D4",  "D5", "D6", "D7", "D8", "D9", "D10", "D11", "D12"]:
  #      if dat == None:
   #         fechas_dat_incom.append(fecha_inicial)
        
    #    fecha_inicial = fecha_inicial + datetime.timedelta(hours=1)
        
#print('Falta dato en las fechas: ', fechas_dat_incom)



#win.show()            
#sys.exit(app.exec_()) 
