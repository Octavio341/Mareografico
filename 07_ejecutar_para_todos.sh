#!/bin/bash

# Ejecutar el script para todos los archivos de un directorio
for i in `ls | grep '\.dat'`
do
	python comprobar_datos_toga.py $i 1
	echo "******PRESIONE ENTER PARA CONTINUAR CON EL SIGUIENTE ARCHIVO******"
	read
done
