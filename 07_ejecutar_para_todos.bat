@echo off 
rem Oculta los comando que se ejecutan para qu la consola se vea limpia
setlocal enabledelayedexpansion
:inicio
cls 
rem cls limpia la pantalla


echo ===================================
echo            MENU PRINCIPAL
echo ===================================
echo escriba el numero para realizar la accion
echo.
echo 1. 02_menu_graficar_toga.py
echo 2. 03_preprocesa.py
echo 3. 04_menu_graficar_toga.py
echo 4. Desde el terminal
echo.
echo 10. Salir
echo.

set /p opcion= Selecciona una opcion:

if "%opcion%"=="1" goto 1
if "%opcion%"=="2" goto 2
if "%opcion%"=="3" goto 3
if "%opcion%"=="4" goto 4
if "%opcion%"=="10" goto 10

echo Opcion invalida, intanta de nuevo.
pause
goto inicio


:1
echo estas en la 1
python 02_menu_graficar_toga.py
echo finalizado
pause
goto inicio
:2
echo esta en la 2
python 03_preprocesa.py
echo finalizado
rem ejecutamos un archivo python en de esta forma ya que estamos en la misma carpeta

pause
goto inicio
:3
echo estas en la 3
python 04_menu_graficar_toga.py
echo finalizado
goto inicio


rem ESTA ES EL TERMINAL //////////////////////////////////////////////
:4
cls
setlocal
endlocal
echo ===================================
echo          Desde el terminal
echo ===================================
echo como quiere interactuar con los datos 
echo.
echo 1. selecciona un dato 
echo 2. datos de forma secuencial 
echo.
echo 3. Regresar a Menu principal
echo.
set /p opcion= selecciona su opcion:

if "%opcion%"=="1" goto seleccion
if "%opcion%"=="2" goto enFila
if "%opcion%"=="3" goto inicio
echo Opcion invalida, intanta de nuevo.
rem procedemos a ejecutar el script de python intengrando los datos
echo.
pause
goto inicio

:10
exit

rem /////////////////  MODO SELECTIVO  ///////////////////////////

:seleccion 
cls
echo ================ Estas en modo seleccion ===================
echo.
setlocal
cd /d C:\Users\octav\OneDrive\Escritorio\-TRABAJANDO-\3- ESTANCIAS\CODIG\1 actividad\scripts\comprendiendo\datos\acapulco
echo archivos en la carpeta:
dir /b /a-d
echo.
set /p archivo= Escribe el nombre del archivo que quieres ver:
echo %archivo%
if exist "%archivo%" (
    echo.
    echo El archivo: %archivo% existe.
    goto Eleccion
    rem set /p decision= Quieres seguir? preciona -si- s  x-no-
    rem echo datos  !decision!
    rem if "!decision!"=="s" (
    rem    goto Eleccion
    rem) else (
    rem    endlocal
    rem    goto inicio
    rem )
    rem podemos usar type "%archivo%" para mostrar el contenido del archivo
) else (
    echo El archivo no existe.
)
pause 
endlocal
goto inicio

rem 
:Eleccion
cls
setlocal
    echo Buscando archivo en la carpeta %archivo%

    cd /d C:\Users\octav\OneDrive\Escritorio\-TRABAJANDO-\3- ESTANCIAS\CODIG\1 actividad\scripts\comprendiendo\datos\acapulco
    set  datos=../datos/acapulco/
    echo %datos%
        echo.
        echo ===================================
        echo          Modo secuencial
        echo ===================================
        echo seleccione donde desea iniciar
        echo.
        echo 1. 05_TogaChecker.py
        echo 2. 06_comprobar_datos_toga.py
        echo 3. 08_agregar_fechas_faltantes.py
        echo 4. 09_graficar_datos_por_mes.py
        echo 5. 10_control_calidad_automatizado.py
        echo 6. 11_control_calidad_automatizado.py
        echo.
        echo 7. mostrar todo los datos
        echo.
        echo 8. Retroceder
        echo 9. Regresar al MENU
        echo.
        cd /d C:\Users\octav\OneDrive\Escritorio\-TRABAJANDO-\3- ESTANCIAS\CODIG\1 actividad\scripts\comprendiendo
        rem para ver si se esta accediendo=  dir /b /a-d
        set /p accion= indica donde quieres empezar el analisis:
        echo %archivo%
    echo -------------------------------------------------------------------------
    if "%accion%"=="1" python 05_TogaChecker.py datos\acapulco\%archivo%
    if "%accion%"=="2" python 06_comprobar_datos_toga.py datos\acapulco\%archivo%
    if "%accion%"=="3" python 08_agregar_fechas_faltantes.py datos\acapulco\%archivo%
    if "%accion%"=="4" python 09_graficar_datos_por_mes.py datos\acapulco\%archivo%
    if "%accion%"=="5" python 10_control_calidad_automatizado.py datos\acapulco\%archivo%
    if "%accion%"=="6" python 11_control_calidad_automatizado.py datos\acapulco\%archivo%
    rem abrir los datos
    if "%accion%"=="7" (
        cls
        type datos\acapulco\%archivo%
        pause
        goto Eleccion
    )
    if "%accion%"=="8" goto seleccion
    if "%accion%"=="9" goto inicio
    echo -------------------------------------------------------------------------
    pause 
    goto Eleccion

rem   ////////////////      MODO SECUENCIAL //////////////////
:enFila
echo ================ Estas en modo en fila ===================
cls
set "Carpeta=datos\acapulco"
echo Buscando archivo en la carpeta %Carpeta%
echo.
echo ===================================
echo          Modo secuencial
echo ===================================
echo seleccione donde desea iniciar
echo.
echo 1. 05_TogaChecker.py
echo 2. 06_comprobar_datos_toga.py
echo 3. 08_agregar_fechas_faltantes.py
echo 4. 09_graficar_datos_por_mes.py
echo 5. 10_control_calidad_automatizado.py
echo 6. 11_control_calidad_automatizado.py
echo.
echo 7. Retroceder a modos
echo.
setlocal 
set /p accion= indica donde quieres empezar el analisis:
set /a contador=0
cls
for %%i in ("%Carpeta%\*.dat") do (
    set /a contador+=1
    echo.
    echo =========================================================
    echo      Archivo encontrado:  %%i        ====Archivo: !contador!             
    echo =========================================================
    echo -------------------------------------------------------------------------
    if "%accion%"=="1" python 05_TogaChecker.py "%%i" 1
    if "%accion%"=="2" python 06_comprobar_datos_toga.py "%%i" 1
    if "%accion%"=="3" python 08_agregar_fechas_faltantes.py "%%i" 1
    if "%accion%"=="4" python 09_graficar_datos_por_mes.py "%%i" 1
    if "%accion%"=="5" python 10_control_calidad_automatizado.py "%%i" 
    if "%accion%"=="6" python 11_control_calidad_automatizado.py "%%i" 
    if "%accion%"=="7" goto 4
    echo -------------------------------------------------------------------------
    echo.
    echo ............... Presione doble ENTER para continuar con el siguiente archivo ..............
    set /p sal=si desea salir precione x
    if /i "!sal!"=="x" (
        echo saliendo
        pause
        endlocal
        goto enFila
    )
    pause >nul
    echo no se preseono x seguimos con el siguiente
    echo.
    rem podemos usar type "%%i" para mostrar el contenido del archivo
    
)
