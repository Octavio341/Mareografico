from PyQt5 import QtWidgets, QtGui
import matplotlib.pyplot as plt
import sys, ntpath, os
import pandas as pd
import datetime

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Funci'on que lee el archivo TOGA, grafica los datos y muestra la grafica en la ventana
def plotTOGA():
    filename = QtWidgets.QFileDialog.getOpenFileName(win, "Seleccione el archivo TOGA...", filter="Archivos DAT (*.dat)")
    nombre_archivo = str(filename[0])
   
    # Realizar el proceso solo si el usuario regres'o un nombre de archivo v'alido
    if nombre_archivo:

        # Leer el archivo de datos
        matriz_toga = pd.read_csv(nombre_archivo,sep=r'\s+', names = ["StationID", "StationName", "Date", "D1", "D2", "D3","D4", "D5", "D6", "D7", "D8", "D9", "D10", "D11", "D12"], engine = 'python', skiprows = 1, na_values = "9999")

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
            else:
                fecha_inicial = datetime.datetime(int(fecha[:4]), int(fecha[4:6]), int(fecha[6:8]), 12)

            # Cargar los 12 datos de la fila de datos
            for dat in ["D1", "D2", "D3", "D4",  "D5", "D6", "D7", "D8", "D9", "D10", "D11", "D12"]:
                lista_fechas.append(fecha_inicial)
                lista_datos.append(matriz_toga[dat][ind])
                fecha_inicial = fecha_inicial + datetime.timedelta(hours=1)

        # Realizar la grafica
        plt.plot(lista_fechas, lista_datos, "-b", linewidth=1)
        plt.title("Grafica del archivo TOGA")
        plt.xlabel("Fecha",fontweight='bold',fontsize=14)
        plt.ylabel("Nivel del mar (mm)",fontweight='bold',fontsize=14)
        plt.grid(True)
        plt.savefig(os.path.splitext(nombre_archivo)[0]+".png")

        # Mostrar la grafica en la ventana
        pixmap = QtGui.QPixmap(os.path.splitext(nombre_archivo)[0]+".png")
        label.setPixmap(pixmap)
        label.resize(pixmap.width(),pixmap.height())
        win.setGeometry(400,400,pixmap.width(),pixmap.height())
        
        print(check1.isChecked())
        dialogBox.exec()

#####################################################
# Crear la ventana principal junto con una etiqueta #
#####################################################

# Inicializar y crear la ventana
app = QtWidgets.QApplication(sys.argv)                      # Inicializar el programa PyQt
win = QtWidgets.QMainWindow()                               # Instanciar el objeto ventana
win.setWindowTitle("Sistema de control de calidad SMN")     # Texto que aparecer'a en la parte superior izquierde de la ventana
win.setGeometry(400,400,400,200)                            # Establecer la posici'on y tamanio inicial de la ventana
label = QtWidgets.QLabel(win)                               # Crear la etiqueta y asignarla a la ventana principal

###########################################
# Crear las acciones del men'u y el men'u #
###########################################

# Crear la accion de abrir archivo
openFile = QtWidgets.QAction('&Abrir TOGA', win)            # Crear el nombre que ser'a mostrado en el men'u
openFile.setShortcut("Ctrl+O")                              # Crear el shortcut para esta opci'on
openFile.setStatusTip('Abrir archivo TOGA')                 # Crear la pista de esta opci'on
openFile.triggered.connect(plotTOGA)                        # Asignar la acci'on que ser'a ejecutada al dar clic en esta opci'on

# Crear la accion de salir del programa
exitAction = QtWidgets.QAction('&Salir', win)               # Crear el nombre que ser'a mostrado en el men'u
exitAction.setShortcut("Ctrl+O")                            # Crear el shortcut para esta opci'on
exitAction.setStatusTip('Cerrar el programa')               # Crear la pista de esta opci'on
exitAction.triggered.connect(QtWidgets.qApp.quit)           # Asignar la acci'on que ser'a ejecutada al dar clic en esta opci'on

# Crear el menu y agregar las acciones
menuBar = win.menuBar()                                     # Crear el objeto men'u asignado a la ventana principal
fileMenu = menuBar.addMenu('&Archivo')                      # Crear el t'itulo principal del men'u
fileMenu.addAction(openFile)                                # Agregar al men'u la opci'on de abrir archivo
fileMenu.addAction(exitAction)                              # Agregar al men'u la opci'on de cerrar programa

################################################################
# Crear la ventana de selecci'on de procesos automaticos de QC #
################################################################

dialogBox = QtWidgets.QDialog()
dialogBox.setWindowTitle("Seleccionar procesos de QC")
dialogBox.setFixedSize(450, 300)

# Crear el checkbox 1
check1 = QtWidgets.QCheckBox(dialogBox)
check1.setText("Detección de picos")
check1.move(100,50)

# Crear el checkbox 2
check2 = QtWidgets.QCheckBox(dialogBox)
check2.setText("Detección de bloqueos")
check2.move(100,100)

# Crear el checkbox 3
check3 = QtWidgets.QCheckBox(dialogBox)
check3.setText("Detección de valores fuera de rango")
check3.move(100,150)

# Crear el Qline 1
line1 = QtWidgets.QLineEdit(dialogBox)
line1.setFixedWidth(40)
line1.move(100,200)

# Crear el Qline 2
line2 = QtWidgets.QLineEdit(dialogBox)
line2.setFixedWidth(40)
line2.move(160,200)

# Crear el boton de "Aceptar"
button = QtWidgets.QPushButton(dialogBox, text="Aceptar")
button.move(200,250)
button.clicked.connect(dialogBox.close)

# Mostrar la ventana
win.show()                                                  # Mostrar la ventana
sys.exit(app.exec_())                                       # Cerrar limpiamente la aplicacion al salir
