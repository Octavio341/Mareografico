from PySide6.QtWidgets import QHBoxLayout,QFileDialog,QPushButton,QMainWindow,QWidget,QVBoxLayout,QApplication,QComboBox
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar
)
import pandas as pd
import datetime
import os
import sys

from matplotlib.figure import Figure
import numpy as np

from os.path import basename
#esto es para ejecutar un script de python 
import subprocess


class VentanaGrafica(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Grafica interactiva")
        self.setGeometry(100,100,800,600)

        self.contador = 0
        self.archivos_cargados = []

        # crear el widget central 
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        self.setCentralWidget(central_widget)

        #Crear la figura y canvas de matplotlib
        self.figure =Figure()# esto es un lienzo 
        self.canvas = FigureCanvas(self.figure) #generamos la grafica
        self.toolbar = NavigationToolbar(self.canvas,self)

        #botón de recetear
        self.boton_reset=QPushButton("Resetear")
        self.boton_reset.setFixedSize(100,40)
        self.boton_reset.setStyleSheet("""QPushButton{background-color:gray;
                                       color:white;
                                       }""")
        self.boton_reset.clicked.connect(self.resetear_interfaz)
        layout.addWidget(self.boton_reset)

        self.boton = QPushButton("Seleccionar archivo .DAT ")
        self.boton.setFixedSize(200,40)
        self.boton.clicked.connect(self.seleccionar_archivo)
        self.boton.setStyleSheet("""QPushButton{background-color:blak;
                                       color:white;
                                    }""")
        
        layout.addWidget(self.toolbar)
        fila_botones= QHBoxLayout()
        fila_botones.addWidget(self.boton)
        fila_botones.addWidget(self.boton_reset)
        layout.addLayout(fila_botones)

        self.setLayout(layout)


        #agregar toolbar y canvas de matplotlib 
        
        layout.addWidget(self.canvas)

        #crear eje para usar self.ax--- de esta forma ya se define
        self.ax = self.figure.add_subplot(111)

        #Dibujar la grafica
        

    def resetear_interfaz(self):
            self.ax.clear()
            self.canvas.draw()
            self.datos=None
            self.contador=0
            self.archivos_cargados=[]#lo inicializamos 
        
            self.nombre_archivo = ""
            print("=========  Se ha Reseteado el programa  ===========")  

    print("############################################################################")
    print("######################### AGREGANDO NUEVOS DATOS     #######################")
    print("############################################################################")
    
    def seleccionar_archivo(self):
        #archivo,_ = QFileDialog.getOpenFileName(
        archivos,_ = QFileDialog.getOpenFileNames(
            self,
            "Seleccionar el archivo Toga..",
            filter="Archivo DAT (*.dat)"
        )
        
        if archivos:
            
            for ruta in archivos:
                ya_registrado = False  # bandera para saber si ya existe

                nombre_archivo = basename(ruta)
                for revision in self.archivos_cargados:
                    if revision == nombre_archivo:
                        print("----------------------------------------------------------------------------------------")
                        print(f"======  El archivo '{revision}'ya ha se ha registrado")
                        ya_registrado = True  # marcar como duplicado
                if not ya_registrado:
                    self.archivos_cargados.append(nombre_archivo)
                    print("")
                    print("agregado",self.archivos_cargados)
                    print("")
                    self.contador += 1
                    print("----------------------------------------------------------------------------------------")
                    print("Nombre del archivo:",nombre_archivo,"                    <---- datos toga [",self.contador,"]")
                    print("")
                    ruta_script="C:/Users/octav/OneDrive/Escritorio/-TRABAJANDO-/3- ESTANCIAS/CODIG/1 actividad/scripts/comprendiendo/06_comprobar_datos_toga.py"
                    try:
                        subprocess.run(["python",ruta_script,ruta],check=True)
                        print("")
                        print("Script ejetado correctamente")
                        print("")
                    except subprocess.CalledProcessError as e:
                        print("Hubo un error al ejecutarse el script:",e)
                        print("")


                    #aqui puedes leer el archivo 
                    matriz_toga =  pd.read_csv(ruta,sep=r'\s+', names = ["StationID", "StationName", "Date", "D1", "D2", "D3","D4", "D5", "D6", "D7", "D8", "D9", "D10", "D11", "D12"], engine = 'python', skiprows = 1, na_values = "9999")
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

                    print("")
                    self.ax.plot(lista_fechas,lista_datos,"-b",linewidth=1)
                    self.ax.set_title("Grafica del archivo Toga")
                    self.ax.set_xlabel("Fecha",fontweight='bold',fontsize=14)
                    self.ax.set_ylabel("Nivel del mar (mm)",fontweight='bold',fontsize=14)
                    self.ax.tick_params(axis='x',rotation=45)
                    self.ax.grid(True,linestyle='--',color='gray',alpha=0.7)
                    self.canvas.draw()
        else:
            print("el archivo no ha sido seleccionado")


app = QApplication([])
ventana = VentanaGrafica()
ventana.show()
app.exec()



