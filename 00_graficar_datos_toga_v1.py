from datetime import timedelta
import matplotlib.pyplot as plt
import pandas as pd
import datetime 

# Leer el archivo de datos y guardarlo en un dataframe de Pandas
matriz_toga = pd.read_table("datos/acapulco/h316a52.dat", delim_whitespace = True, names = ["StationID", "StationName", "Date", "D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "D10", "D11", "D12"], engine = 'python', skiprows = 1, na_values = "9999")

# Crear las listas de fechas y datos
lista_fechas=list()
lista_datos=list()
 
# Procesar l'inea por linea del dataframe
for ind in matriz_toga.index:

    # Cargar la fecha de la columna correspondiente
    fecha = str(matriz_toga["Date"][ind])

    # Crear la fecha inicial
    if fecha[8:9] == "1":
        fecha_inicial = datetime.datetime(int(fecha[:4]), int(fecha[4:6]), int(fecha[6:8]))
    elif fecha[8:9] == "2":
        fecha_inicial = datetime.datetime(int(fecha[:4]), int(fecha[4:6]), int(fecha[6:8]), 12)
    else:
        print("No se encontro el identificador 1 o 2 en la fecha: "+fecha)
        break

    # Cargar los 12 datos
    for dat in ["D1", "D2", "D3", "D4",  "D5", "D6", "D7", "D8", "D9", "D10", "D11", "D12"]:
        lista_fechas.append(fecha_inicial)
        lista_datos.append(matriz_toga[dat][ind])
        fecha_inicial = fecha_inicial + timedelta(hours=1)

# Realizar la grafica
plt.plot(lista_fechas, lista_datos, "-b", linewidth=2)
plt.title("Grafica del archivo TOGA h316a1952.dat")
plt.xlabel("Fecha",fontweight='bold',fontsize=14)
plt.ylabel("Nivel del mar (mm)",fontweight='bold',fontsize=14)
plt.grid(True)
plt.savefig("h316a1952.png")
