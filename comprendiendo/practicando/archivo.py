import sys
import subprocess
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ejecutor de Scripts BAT")
        self.setGeometry(200, 200, 300, 200)

        # Crear layout y botones
        layout = QVBoxLayout()

        # Botón 1
        boton1 = QPushButton("Ejecutar Script 1")
        boton1.clicked.connect(self.ejecutar_bat1)
        layout.addWidget(boton1)

        # Botón 2
        boton2 = QPushButton("Ejecutar Script 2")
        boton2.clicked.connect(self.ejecutar_bat2)
        layout.addWidget(boton2)

        # Contenedor principal
        contenedor = QWidget()
        contenedor.setLayout(layout)
        self.setCentralWidget(contenedor)

    def ejecutar_bat1(self):
        # Cambia la ruta por la de tu archivo .bat
        subprocess.run(["start", "ruta\\a\\tu_script1.bat"], shell=True)

    def ejecutar_bat2(self):
        subprocess.run(["start", "ruta\\a\\tu_script2.bat"], shell=True)

# Ejecutar la app
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec())
