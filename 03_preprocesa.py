from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QPushButton, QCheckBox, QAction, qApp, QFileDialog, QLabel
from PyQt5 import QtGui
import matplotlib.pyplot as plt
import sys, ntpath, os
import pandas as pd
import datetime

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("SMN - Control de Calidad")
        self.setGeometry(400, 400, 400, 200)
        
        # Crear las listas de fechas, datos y etiquetas
        self.lista_fechas = list()
        self.lista_datos = list()
        self.lista_etiquetas = list()

        # Crear la etiqueta donde se mostrar'an las gr'aficas
        self.label = QLabel(self)

        # Crear la acci'on de abrir archivo
        openFile = QAction('&Abrir TOGA', self)
        openFile.setShortcut("Ctrl+O")
        openFile.setStatusTip('Abrir archivo TOGA')
        openFile.triggered.connect(self.plot_toga)

        # Crear la accion de salir del programa
        exitAction = QAction('&Salir', self)
        exitAction.setShortcut("Ctrl+O")
        exitAction.setStatusTip('Cerrar el programa')
        exitAction.triggered.connect(qApp.quit)

        # Crear el men'u y agregar las acciones
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&Archivo')
        fileMenu.addAction(openFile)
        fileMenu.addAction(exitAction)

    def show_dialog(self):
        dialog = Dialog(self)  # self hace referencia al padre
        dialog.show()

    def plot_toga(self):

        # Obtener la ruta y el nombre del archivo a graficar
        filename = QFileDialog.getOpenFileName(self, "Seleccione el archivo TOGA...", filter="Archivos DAT (*.dat)")
        nombre_archivo = str(filename[0])

        # Realizar el proceso solo si el usuario regres'o un nombre de archivo v'alido
        if nombre_archivo:

            # Leer el archivo de datos
            matriz_toga = pd.read_csv(nombre_archivo, sep=r'\s+', names = ["StationID", "StationName", "Date", "D1", "D2","D3","D4", "D5", "D6", "D7", "D8", "D9", "D10", "D11", "D12"], engine = 'python', skiprows = 1, na_values = "9999")

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
                    self.lista_fechas.append(fecha_inicial)
                    self.lista_datos.append(matriz_toga[dat][ind])
                    self.lista_etiquetas.append(0)
                    fecha_inicial = fecha_inicial + datetime.timedelta(hours=1)

            # Realizar la grafica
            plt.plot(self.lista_fechas, self.lista_datos, "-b", linewidth=2)
            plt.title("Grafica del archivo TOGA")
            plt.xlabel("Fecha",fontweight='bold',fontsize=14)
            plt.ylabel("Nivel del mar (mm)",fontweight='bold',fontsize=14)
            plt.grid(True)
            plt.savefig(os.path.splitext(nombre_archivo)[0]+".png")

            # Mostrar la grafica en la ventana
            pixmap = QtGui.QPixmap(os.path.splitext(nombre_archivo)[0]+".png")
            self.label.setPixmap(pixmap)
            self.label.resize(pixmap.width(),pixmap.height())
            self.setGeometry(400,400,pixmap.width(),pixmap.height())

            # Mostrar la ventana de proceso autom'atico
            self.show_dialog()

class Dialog(QDialog):

    def __init__(self, *args, **kwargs):
        super(Dialog, self).__init__(*args, **kwargs)
        self.setWindowTitle("Seleccionar procesos de QC")
        self.setFixedSize(300, 200)

        # Crear el checkbox
        self.check1 = QCheckBox(self)
        self.check1.setText("Remover picos")
        self.check1.move(100,50)

        # Crear el boton de "Aceptar"
        self.button = QPushButton(self, text="Aceptar")
        self.button.move(100,150)
        self.button.clicked.connect(self.realizar_cc_automatico)

    def realizar_cc_automatico(self):
        if self.check1.isChecked():
            #Hacer el control automatico
            print("Hacer el control automatico")
        
        # Cerrar el cuadro de dialogo
        self.close()

if __name__ == "__main__":  
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
