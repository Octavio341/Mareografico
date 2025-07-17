from PySide6.QtWidgets import QHBoxLayout,QFileDialog,QPushButton,QMainWindow,QWidget,QVBoxLayout,QApplication,QComboBox
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar
)
import pandas as pd
import datetime
import os

from matplotlib.figure import Figure
import numpy as np


class VentanaGrafica(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Grafica interactiva")
        self.setGeometry(100,100,800,600)

        # crear el widget central 
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        self.setCentralWidget(central_widget)

        #Crear la figura y canvas de matplotlib
        self.figure =Figure()# esto es un lienzo 
        self.canvas = FigureCanvas(self.figure) #generamos la grafica
        self.toolbar = NavigationToolbar(self.canvas,self)

        #agregar toolbar y canvas de matplotlib 
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)

        #crear eje para usar self.ax--- de esta forma ya se define
        self.ax = self.figure.add_subplot(111)

        #Dibujar la grafica
        
        self.boton = QPushButton("Seleccionar archivo .DAT ")
        self.boton.clicked.connect(self.seleccionar_archivo)
        layout.addWidget(self.boton)
        self.setLayout(layout)


    def seleccionar_archivo(self):
        archivo,_ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar el archivo Toga..",
            filter="Archivo DAT (*.dat)"

        )
        if archivo:
            print("Archivo seleccionado", archivo)
        else:
            print("No se seleciono ningun archivo.")

        nombre_completo = archivo
        nombre_archivo= os.path.basename(nombre_completo)
        
        print("nombre archivo",nombre_archivo)

        if nombre_completo:
            #leer el archivo de datos
            
            matriz_toga =  pd.read_csv(nombre_completo,sep=r'\s+', names = ["StationID", "StationName", "Date", "D1", "D2", "D3","D4", "D5", "D6", "D7", "D8", "D9", "D10", "D11", "D12"], engine = 'python', skiprows = 1, na_values = "9999")
            print("matriz toga",matriz_toga.head())

            lista_fechas=list()
            lista_datos=list()

            for ind in matriz_toga.index:
                fecha = str(matriz_toga["Date"][ind])

                if fecha[8:9] == "1":
                    fecha_inicial = datetime.datetime(int(fecha[:4]),int(fecha[4:6]),int(fecha[6:8]))
                else:
                    fecha_inicial=datetime.datetime(int(fecha[:4]),int(fecha[4:6]),int(fecha[6:8]),12)
                
                for dat in  ["D1", "D2", "D3", "D4",  "D5", "D6", "D7", "D8", "D9", "D10", "D11", "D12"]:
                    lista_fechas.append(fecha_inicial)
                    lista_datos.append(matriz_toga[dat][ind])
                    fecha_inicial=fecha_inicial + datetime.timedelta(hours=1)

        else:
            print("el archivo no ha sido seleccionado")
        
        
        self.ax.plot(lista_fechas,lista_datos,"-b",linewidth=1)
        self.ax.set_title("Grafica del archivo Toga")
        self.ax.set_xlabel("Fecha",fontweight='bold',fontsize=14)
        self.ax.set_ylabel("Nivel del mar (mm)",fontweight='bold',fontsize=14)
        self.ax.tick_params(axis='x',rotation=45)
        self.canvas.draw()
    
    

app = QApplication([])
ventana = VentanaGrafica()
ventana.show()
app.exec()



