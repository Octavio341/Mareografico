from datetime import timedelta
import pandas as pd
import datetime 
import sys
import os

# Verificar que se haya pasado el n'umero correcto de par'ametros
if len(sys.argv) < 2:
        print("No se ha proporcionado el nombre del archivo a acompletar")
        quit()

# Obtener el nombre del archivo de entrada a procesar de la lista de par'ametros
nombre_archivo = sys.argv[1]
print("Se va a trabajar con el archivo: "+nombre_archivo)

#extraer solo el nombre del archivo sin ruta 
nombre_sin_ruta = os.path.basename(nombre_archivo)

# Crear el archivo de salida corregido
archivo_salida = open("completed-"+nombre_sin_ruta, 'w+')

# Leer el encabezado del archivo de entrada y escribirlo en el archivo de salida
archivo_entrada = open(nombre_archivo, "r")
if archivo_entrada.mode == 'r':
    archivo_salida.write(archivo_entrada.readline())
archivo_entrada.close()

# Leer el archivo de datos de entrada y guardarlo en un dataframe de Pandas
matriz_toga = pd.read_csv(nombre_archivo, sep=r'\s+', names = ["StationID", "StationName", "Date", "D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "D10", "D11", "D12"], engine = 'python', skiprows = 1)
print("Filas leidas:",len(matriz_toga))
print(matriz_toga.head())
ind = 0

# Obtener el anio del archivo, as'i como el ID de estaci'on y el nombre de la estaci'on
print("¿esta vacio el dataframe? ", matriz_toga.empty) #//cambio// si realmente ahi un archivo
fecha = str(matriz_toga["Date"].iloc[0])
id_estacion = str(matriz_toga["StationID"][0])
nombre_estacion = str(matriz_toga["StationName"][0])

# Crear la fecha de control 
fecha_control=datetime.datetime(int(fecha[:4]),1,1)
hora_control=1
anio_final=int(fecha[:4])+1

# Generar datos para cada fecha del anio
while fecha_control.year < anio_final and ind < matriz_toga["Date"].size:

    # Cargar la fecha del dataframe
    fecha = str(matriz_toga["Date"][ind])

    # Verificar si la fecha de control y la fecha del dataframe son iguales
    if fecha == fecha_control.strftime("%Y%m%d")+str(hora_control):

        # Si la fecha de control y la fecha del dataframe son iguales, escribir los datos
        archivo_salida.write(id_estacion+" "+nombre_estacion+" "+fecha_control.strftime("%Y%m%d")+str(hora_control)+" "+"{:.0f}".format(matriz_toga["D1"][ind])+" "+"{:.0f}".format(matriz_toga["D2"][ind])+" "+"{:.0f}".format(matriz_toga["D3"][ind])+" "+"{:.0f}".format(matriz_toga["D4"][ind])+" "+"{:.0f}".format(matriz_toga["D5"][ind])+" "+"{:.0f}".format(matriz_toga["D6"][ind])+" "+"{:.0f}".format(matriz_toga["D7"][ind])+" "+"{:.0f}".format(matriz_toga["D8"][ind])+" "+"{:.0f}".format(matriz_toga["D9"][ind])+" "+"{:.0f}".format(matriz_toga["D10"][ind])+" "+"{:.0f}".format(matriz_toga["D11"][ind])+" "+"{:.0f}".format(matriz_toga["D12"][ind])+"\n")

    else:

        # Si la fecha de control y la fecha del dataframe no son iguales, escribir la linea de datos nulos
        archivo_salida.write(id_estacion+" "+nombre_estacion+" "+fecha_control.strftime("%Y%m%d")+str(hora_control)+" 9999 9999 9999 9999 9999 9999 9999 9999 9999 9999 9999 9999\n")

        # Avanzar con la fecha de control hasta que sea igual a la del dataframeo se acabe el año
        while fecha != fecha_control.strftime("%Y%m%d")+str(hora_control) and fecha_control.year < anio_final:

            # Avanzar la fecha de control
            if hora_control == 1:
                hora_control = 2
            else:
                hora_control = 1
                fecha_control=fecha_control+timedelta(days=1)

            # Si la fecha de control y la fecha del dataframe son iguales, escribir los datos
            if fecha == fecha_control.strftime("%Y%m%d")+str(hora_control):

                # Si la fecha de control y la fecha del dataframe son iguales, escribir los datos
                archivo_salida.write(id_estacion+" "+nombre_estacion+" "+fecha_control.strftime("%Y%m%d")+str(hora_control)+" "+"{:.0f}".format(matriz_toga["D1"][ind])+" "+"{:.0f}".format(matriz_toga["D2"][ind])+" "+"{:.0f}".format(matriz_toga["D3"][ind])+" "+"{:.0f}".format(matriz_toga["D4"][ind])+" "+"{:.0f}".format(matriz_toga["D5"][ind])+" "+"{:.0f}".format(matriz_toga["D6"][ind])+" "+"{:.0f}".format(matriz_toga["D7"][ind])+" "+"{:.0f}".format(matriz_toga["D8"][ind])+" "+"{:.0f}".format(matriz_toga["D9"][ind])+" "+"{:.0f}".format(matriz_toga["D10"][ind])+" "+"{:.0f}".format(matriz_toga["D11"][ind])+" "+"{:.0f}".format(matriz_toga["D12"][ind])+"\n")

            else:

                # Si la fecha de control aun no alcanza la fecha del dataframe, escribir la linea de datos nulos
                archivo_salida.write(id_estacion+" "+nombre_estacion+" "+fecha_control.strftime("%Y%m%d")+str(hora_control)+" 9999 9999 9999 9999 9999 9999 9999 9999 9999 9999 9999 9999\n")

    # Incrementar el indice del dataframe
    ind = ind + 1
     
    # Avanzar la fecha de control
    if hora_control == 1:
        hora_control = 2
    else:
        hora_control = 1
        fecha_control=fecha_control+timedelta(days=1)

# Avanzar con la fecha de control hasta que se acabe el año de ser necesario
while fecha_control.year < anio_final:
    
    # Escribir la linea de datos nulos
    archivo_salida.write(id_estacion+" "+nombre_estacion+" "+fecha_control.strftime("%Y%m%d")+str(hora_control)+" 9999 9999 9999 9999 9999 9999 9999 9999 9999 9999 9999 9999\n")
        
    # Avanzar la fecha de control
    if hora_control == 1:
        hora_control = 2
    else:
        hora_control = 1
        fecha_control=fecha_control+timedelta(days=1)

# Cerrar el archivo de texto
archivo_salida.close()

print("Fin del analisis, se ha creado el archivo: completed-"+nombre_archivo)
