#!/bin/bash

# Ejecutar el script para todos los archivos de un directorio
for i in datos/acapulco/*.dat
do
	python 06_comprobar_datos_toga.py $i 1
	echo "******PRESIONE ENTER PARA CONTINUAR CON EL SIGUIENTE ARCHIVO******"
	read
done
