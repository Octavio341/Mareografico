from datetime import timedelta
import matplotlib.pyplot as plt
import pandas as pd
import datetime 
import sys
import os

# Verificar que se haya pasado el n'umero correcto de par'ametros
if len(sys.argv) < 2:
        print("No se ha proporcionado el nombre del archivo a graficar")
        quit()

# Nombre del archivo
nombre_archivo = sys.argv[1]
print("Se va a cargar el archivo: "+nombre_archivo)
###
#obtenemos solo el nombre base del archivo (sin ruta ni extension)
nombre_sin_ruta = os.path.splitext(os.path.basename(nombre_archivo))[0]
#creamos carpeta de salida sin no existe
os.makedirs("graficas-COD-9",exist_ok=True)
###
# Leer el archivo de datos y guardarlo en un dataframe de Pandas
matriz_toga = pd.read_csv(nombre_archivo, sep=r'\s+', names = ["StationID", "StationName", "Date", "D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "D10", "D11", "D12"], engine = 'python', skiprows = 1, na_values = "9999")

# Crear el 'indice que recorrer'a el dataframe
ind = 0;

# Realizar la gr'afica por mes
meses = ["01","02","03","04","05","06","07","08","09","10","11","12"]
for mes in meses:
    
    # Crear las listas de fechas y datos
    lista_fechas=list()
    lista_datos=list()

    # Cargar la fecha de la columna correspondiente
    fecha = str(matriz_toga["Date"][ind])

    while fecha[4:6] == mes and ind < len(matriz_toga.index):

        # Crear la fecha inicial
        if fecha[8:9] == "1":
            fecha_inicial = datetime.datetime(int(fecha[:4]), int(fecha[4:6]), int(fecha[6:8]))
        else:
            fecha_inicial = datetime.datetime(int(fecha[:4]), int(fecha[4:6]), int(fecha[6:8]), 12)

        # Cargar los 12 datos
        for dat in ["D1", "D2", "D3", "D4",  "D5", "D6", "D7", "D8", "D9", "D10", "D11", "D12"]:
            lista_fechas.append(fecha_inicial)
            lista_datos.append(matriz_toga[dat][ind])
            fecha_inicial = fecha_inicial + timedelta(hours=1)

        # Avanzar el indice
        ind = ind + 1

        # Cargar la nueva fecha si todavia hay datos
        if ind < len(matriz_toga.index):
            fecha = str(matriz_toga["Date"][ind])

    # Realizar la grafica del mes
    plt.figure(figsize=(20, 3), dpi=150)
    plt.plot(lista_fechas, lista_datos, "-b", linewidth=2)
    plt.title("Grafica del mes "+mes+" del archivo "+nombre_archivo)
    plt.xlabel("Fecha",fontweight='bold',fontsize=14)
    plt.ylabel("Nivel del mar (mm)",fontweight='bold',fontsize=14)
    plt.grid(True)
    ###
    #editamos por esta 
    #plt.savefig("graficas/"+mes+"-"+nombre_sin_ruta+".png")
    #guardamos la imagen dentro de 'graficas/'
    plt.savefig(f"graficas-COD-9/{mes}-{nombre_sin_ruta}.png")

    ###

print("Se ha finalizado la creacion de graficas.")
