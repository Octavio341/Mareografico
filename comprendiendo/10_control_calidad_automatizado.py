# Sistema de control de calidad autom'atico de datos de nivel del mar V1.0
# 'Ultima revisi'on: 8 de abril de 2021
# Autor: Octavio Gomez Ramos

from datetime import timedelta
import pandas as pd
import datetime
import sys
import os
# Funci'on que determina si un anio es bisiesto o no
def es_bisiesto(anio):
    resto = anio % 4
    if resto == 0:
        resto = anio % 100
        if resto == 0:
            resto = anio % 400
            if resto == 0:
                return True
            else:
                return False
        else:
            return True
    else:
        return False

# Verificar que se haya pasado el n'umero correcto de par'ametros
if len(sys.argv) < 2:
    print("No se ha proporcionado el nombre del archivo a verificar")
    quit()

# Obtener el nombre del archivo de entrada a procesar de la lista de par'ametros
nombre_archivo = sys.argv[1]
print("Se va a cargar el archivo: "+nombre_archivo)
print("")
# Leer el archivo de datos y guardarlo en un dataframe de Pandas
matriz_toga = pd.read_csv(nombre_archivo, sep=r'\s+', names = ["StationID", "StationName", "Date", "D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "D10", "D11", "D12"], engine = 'python', skiprows = 1, na_values = "9999")

# Obtener el anio del archivo
fecha = str(matriz_toga["Date"][0])
print("Se ha cargado el archivo "+nombre_archivo+" y se han encontrado datos del anio "+fecha[0:4]+".")
print("***** Inicio de la revision del archivo *****")

###################################################
# Revisi'on de numero correcto de l'ineas de datos#
###################################################

print("Comprobando que el archivo contenga el numero correcto de lineas de datos ",end = '')

# Calcular cu'antas lineas de datos se esperan
if es_bisiesto(int(fecha[:4])):
    dias_esperados=366*2
else:
    dias_esperados=365*2

if len(matriz_toga.index) == dias_esperados:
    print("[OK]")
else:
    print("[FAIL]")
    print("ERROR: se esperaban "+str(dias_esperados)+" lineas de datos y se han encontrado "+str(len(matriz_toga.index))+".")
    print("Favor de corregir este problema para poder realizar los procesos automatizados de control de calidad.")
    sys.exit(1)

####################################################
# Revisi'on del incremento cronol'ogico del tiempo #
####################################################

print("Comprobando que el tiempo se incremente cronologicamente en los datos ",end = '')

# Crear la fecha de control
fecha_control=datetime.datetime(int(fecha[:4]),1,1)
hora_control=1
dias_faltantes=0
dias_existentes=0
anio_final=int(fecha[:4])+1
ind = 0

# Generar una a una las fechas y compararlas con el dataframe
while fecha_control.year < anio_final:

    if ind < len(matriz_toga.index):

        # Cargar la fecha del dataframe
        fecha = str(matriz_toga["Date"][ind])

        # Verificar si la fecha de control y la fecha del dataframe son iguales
        if fecha != fecha_control.strftime("%Y%m%d")+str(hora_control):
            print("[FAIL]")
            print("ERROR: El tiempo no se incrementa cronologicamente en los datos, se esperaba la fecha "+fecha_control.strftime("%Y%m%d")+str(hora_control)+" y se ha encontrado la fecha "+fecha+".")
            print("Favor de corregir este problema para poder realizar los procesos automatizados de control de calidad.")
            sys.exit(1)

        # Incrementar el indice del dataframe
        ind = ind + 1

        # Avanzar la fecha de control
        if hora_control == 1:
            hora_control = 2
        else:
            hora_control = 1
            fecha_control=fecha_control+timedelta(days=1)

if fecha_control.year == anio_final:
    print("[OK]")
else:
    print("[FAIL]")
    print("ERROR: El tiempo no se incrementa cronologicamente en los datos")
    print("Favor de corregir este problema para poder realizar los procesos automatizados de control de calidad.")
    sys.exit(1)

#######################################
# Detecci'on de caracteres inv'alidos #
#######################################

print("Detectando si las columnas de datos contienen caracteres invalidos ",end = '')

# Verificar si alguna columna de datos contiene valores no num'ericos
if str(matriz_toga["Date"].dtypes) == "object" or str(matriz_toga["D1"].dtypes) == "object" or str(matriz_toga["D2"].dtypes) == "object" or str(matriz_toga["D3"].dtypes) == "object" or str(matriz_toga["D4"].dtypes) == "object" or str(matriz_toga["D5"].dtypes) == "object" or str(matriz_toga["D6"].dtypes) == "object" or str(matriz_toga["D7"].dtypes) == "object" or str(matriz_toga["D8"].dtypes) == "object" or str(matriz_toga["D9"].dtypes) == "object" or str(matriz_toga["D10"].dtypes) == "object" or str(matriz_toga["D11"].dtypes) == "object" or str(matriz_toga["D12"].dtypes) == "object":
    print("[FAIL]")
    print("ERROR: Se han detectado las siguientes columnas de datos que contienen valores no numericos: ",end = '')
    for colname in ["Date", "D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "D10", "D11", "D12"]:
        if matriz_toga[colname].dtypes == "object":
            print(colname+" ",end = '')
    print("\nFavor de corregir este problema para poder realizar los procesos automatizados de control de calidad.")
else:
    print("[OK]")

########################################################################
# Crear el array de fechas, valores y etiquetas a partir del dataframe #
########################################################################

lista_fechas = list()
lista_datos = list()
lista_etiquetas = list()
ind = 0

# Recorrer todo el dataframe
while ind < len(matriz_toga.index):

    # Cargar la fecha de la columna correspondiente
    fecha = str(matriz_toga["Date"][ind])

    # Crear la fecha inicial
    if fecha[8:9] == "1":
        fecha_inicial = datetime.datetime(int(fecha[:4]), int(fecha[4:6]), int(fecha[6:8]))
    else:
        fecha_inicial = datetime.datetime(int(fecha[:4]), int(fecha[4:6]), int(fecha[6:8]), 12)

    # Cargar los 12 datos
    for dat in ["D1", "D2", "D3", "D4",  "D5", "D6", "D7", "D8", "D9", "D10", "D11", "D12"]:
        lista_fechas.append(fecha_inicial)
        lista_datos.append(matriz_toga[dat][ind])
        lista_etiquetas.append(0)
        fecha_inicial = fecha_inicial + timedelta(hours=1)

    # Avanzar el 'indice
    ind = ind + 1

##########################
# Prueba de l'inea recta #
##########################

print("Realizando prueba de estabilidad (linea recta)")

stuckcount = 0
stuckvalue = lista_datos[0]

# Recorrer todo el arreglo de datos
for ind in range(len(lista_datos)):

    # Comenzar a partir del segundo dato
    if ind > 0:

        # Verificar si el dato que se está revisando actualmente no es igual al stuckvalue
        if stuckvalue == lista_datos[ind]:
            stuckcount = stuckcount + 1
        else:
            stuckvalue == lista_datos[ind]
            stuckcount = 0

        if stuckcount > 1:
            # Etiquetar el stuckvalue actual
            print("---Se han encontrado y etiquetado valores iguales consecutivos (stuck values).")
            lista_etiquetas[ind]=3

            # Si se trata de los primeros tres valores, etiquetar los dos valores previos
            if stuckcount == 2:
                lista_etiquetas[ind-1]=3
                lista_etiquetas[ind-2]=3

##################################
# Prueba de valor fuera de rango #
##################################

# Nota, esta prueba 'unicamente se realiza si el usuario ha proporcionado el rango a verificar
if len(sys.argv) > 2:

    print ("El usuario ha proporcionado un rango de valores a verificar, se hará la prueba de rango.")

    # Obtener el rango proporcionado por el usuario
    rinf = float(sys.argv[2])
    rsup = float(sys.argv[3])


    # Recorrer todo el arreglo de datos y verificar si los valores se encuentran en rango
    for ind in range(len(lista_datos)):

        if lista_datos[ind] < rinf or lista_datos[ind] > rsup:
            lista_etiquetas[ind] = 4
            print("El valor "+str(lista_datos[ind])+" ha sido etiquetado como fuera de rango.")


#####################################################
# Escribir el archivo de texto de datos etiquetados #
#####################################################

print("Se va a proceder a escribir el archivo de salida con los datos etiquetados.")

# Crear el archivo de salida etiquetado
#archivo_salida = open("acapulco",nombre_archivo, 'w+')

#######
### CREAR NUEVA CARPETA
#######
carpeta_base="nueva_carpeta-COD-10"
ruta_salida= os.path.join(carpeta_base,nombre_archivo)

#crear todas las carpetas necesarias(si no existen)
os.makedirs(os.path.dirname(ruta_salida),exist_ok=True)

#abrir (crear o sobrescribir) el archivo 
with open(ruta_salida,'w+')as archivo_salida:
    archivo_salida.write("Contenido de prueba\n")
    print("archivo",archivo_salida)
    # Recorrer el arreglo de datos para escribirlo en un archivo de texto
    for ind in range(len(lista_datos)):
        archivo_salida.write(lista_fechas[ind].strftime("%Y-%m-%d %H:%M:%S")+" "+str(lista_datos[ind])+" "+str(lista_etiquetas[ind])+"\n")

# Cerrar el archivo de texto
archivo_salida.close()

print("Se ha creado el archivo de salida etiquetado labeled-"+nombre_archivo+".")
print("***** Fin de la revision del archivo *****")
