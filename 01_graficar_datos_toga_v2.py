import matplotlib.pyplot as plt
import pandas as pd
import datetime
import sys
import os

from datetime import timedelta
from pandas.plotting import register_matplotlib_converters # registrador de fechas 
register_matplotlib_converters()

nombre_archivo = str(sys.argv[1])   # Obtener el nombre del archivo

matriz_toga = pd.read_csv(nombre_archivo, sep=r'\s+', names = ["StationID", "StationName", "Date", "D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "D10", "D11", "D12"], engine = 'python', skiprows = 1, na_values = "9999")

lista_fechas = list() # Crear una lista para las fechas
lista_datos = list()  # Crear una lista para los datos

for ind in matriz_toga.index:   # Procesar el dataframe fila a fila

    fecha = str(matriz_toga["Date"][ind])       # Obtener la fecha
    if fecha[8:9] == "1":                       # Crear la fecha inicial
        fecha_inicial = datetime.datetime(int(fecha[:4]), int(fecha[4:6]), int(fecha[6:8]))         # Si la fecha inicia las 00 hrs.
    elif fecha[8:9] == "2": 
        fecha_inicial = datetime.datetime(int(fecha[:4]), int(fecha[4:6]), int(fecha[6:8]), 12)     # Si la fecha inicia a las 12:00 hrs.
    else:
        break

    for dat in ["D1", "D2", "D3", "D4",  "D5", "D6", "D7", "D8", "D9", "D10", "D11", "D12"]:        # Agregar una a una cada hora de datos 
        lista_fechas.append(fecha_inicial)
        lista_datos.append(matriz_toga[dat][ind])
        fecha_inicial = fecha_inicial + timedelta(hours=1)
        
nombre_archivo =os.path.basename(nombre_archivo)
plt.plot(lista_fechas, lista_datos, "-b", linewidth=2)              # Realizar la gr'afica
plt.title("Grafica del archivo TOGA "+nombre_archivo)               # T'itulo de la gr'afica
plt.xlabel("Fecha",fontweight='bold',fontsize=14)                   # Etiqueta del eje y
plt.ylabel("Nivel del mar (mm)",fontweight='bold',fontsize=14)      # Etiqueta del eje x
plt.grid(True)                                                      # Mostrar la cuadr'icula de fondo
plt.savefig(nombre_archivo[:len(nombre_archivo)-4]+".png")          # Guardar el archivo de imagen
