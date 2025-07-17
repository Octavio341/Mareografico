from datetime import timedelta
import matplotlib.pyplot as plt
import pandas as pd
import datetime 
import sys
import os


print("ejecutando: 06_comprobar_datos_toga.py")
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
matriz_toga = pd.read_csv(nombre_archivo,sep=r'\s+', names = ["StationID", "StationName", "Date", "D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "D10", "D11", "D12"], engine = 'python', skiprows = 1, na_values = "9999")

# Obtener el anio del archivo
fecha = str(matriz_toga["Date"][0])

# Crear la fecha de control 
fecha_control=datetime.datetime(int(fecha[:4]),1,1)
hora_control=1
dias_faltantes=0
dias_existentes=0
anio_final=int(fecha[:4])+1
ind = 0

# Calcular cu'antas lineas de datos se esperan
if es_bisiesto(int(fecha[:4])):
    dias_esperados=366*2
else:
    dias_esperados=365*2
    
print("Archivo "+nombre_archivo+" cargado, se han encontrado datos del anio "+fecha_control.strftime("%Y"))
print("El archivo debe contener "+str(dias_esperados)+" l'ineas de datos y se han encontrado "+str(len(matriz_toga.index)))

if len(matriz_toga.index) > dias_esperados:
    print("El archivo contiene m'as lineas de las que deber'ia tener, debe ser procesado para poder ser analizado.")
    quit()

# Generar una a una las fechas y compararlas con el dataframe
while fecha_control.year < anio_final:

    if ind < len(matriz_toga.index):

        # Cargar la fecha del dataframe
        fecha = str(matriz_toga["Date"][ind])

    # Verificar si la fecha de control y la fecha del dataframe son iguales
    if fecha == fecha_control.strftime("%Y%m%d")+str(hora_control):

        # Contar el dia existente
        dias_existentes = dias_existentes+1

    else:

        # Si la fecha de control y la fecha del dataframe no son iguales, avisar al usuario y contar la linea faltante
        print("No se encontr'o la fecha "+fecha_control.strftime("%Y%m%d")+str(hora_control))
        dias_faltantes=dias_faltantes+1

        # Avanzar con la fecha de control hasta que sea igual a la del dataframeo se acabe el año
        while fecha != fecha_control.strftime("%Y%m%d")+str(hora_control) and fecha_control.year < anio_final:
            # Avanzar la fecha de control
            if hora_control == 1:
                hora_control = 2
            else:
                hora_control = 1
                fecha_control=fecha_control+timedelta(days=1)
        
            if fecha == fecha_control.strftime("%Y%m%d")+str(hora_control):
                # Si la fecha de control y la fecha del dataframe son iguales, contarlo
                dias_existentes=dias_existentes+1
            else:
                # Si la fecha de control y la fecha del dataframe no son iguales, avisar al usuario y contar la linea faltante
                print("No se encontr'o la fecha "+fecha_control.strftime("%Y%m%d")+str(hora_control))
                dias_faltantes=dias_faltantes+1

    # Incrementar el indice del dataframe
    ind = ind + 1

    # Avanzar la fecha de control
    if hora_control == 1:
        hora_control = 2
    else:
        hora_control = 1
        fecha_control=fecha_control+timedelta(days=1)

# Notificar al usuario si el archivo est'a completo o no
if dias_faltantes == 0:
    print("Fin del analisis, el archivo esta completo, se han encontrado las "+str(dias_existentes)+" lineas de datos esperadas.")   
else:
    print("Fin del analisis, al archivo le hicieron falta "+str(dias_faltantes)+" filas de datos.")

datos_validos=(dias_faltantes+dias_existentes)*12-matriz_toga.isna().sum().sum()
print("Hay "+str(datos_validos)+" datos validos ("+str("{0:.2f}".format(datos_validos*100/((dias_faltantes+dias_existentes)*12)))+"%) y "+str(matriz_toga.isna().sum().sum())+" datos nulos ("+str("{0:.2f}".format(matriz_toga.isna().sum().sum()*100/((dias_faltantes+dias_existentes)*12)))+"%)")
