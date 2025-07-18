from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton, QFileDialog
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar
)
from matplotlib.figure import Figure
from PySide6.QtCore import Qt
import matplotlib.dates as mdates
from datetime import datetime, timedelta

class VentanaGrafica(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Zona visible por fechas")
        self.setGeometry(100, 100, 900, 600)

        self.nombres_archivos = [
            'completed-h316a52.dat', 'completed-h316a82.dat',
            'h316a52.dat', 'h316a53.dat', 'h316a54.dat',
            'h316a55.dat', 'h316a56.dat', 'h316a57.dat', 'h316a58.dat'
        ]

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.label_archivo = QLabel("Zona visible mostrada al guardar imagen")
        self.label_archivo.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label_archivo)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)

        self.inicio = datetime(1952, 4, 1)
        self.fechas = [self.inicio + timedelta(days=30*i) for i in range(84)]

        self.ax.plot(self.fechas, [i**0.5 * 10 for i in range(len(self.fechas))])
        self.ax.set_title("Zona visible actual en fechas")
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        self.ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
        self.figure.autofmt_xdate()

        self.toolbar = NavigationToolbar(self.canvas, self)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)

        self.boton_guardar = QPushButton("Guardar imagen (con rango de fechas)")
        self.boton_guardar.clicked.connect(self.guardar_con_nombre_personalizado)
        layout.addWidget(self.boton_guardar)
        
        self.canvas.mpl_connect("draw_event", self.actualizar_label_zona_visible)

    def actualizar_label_zona_visible(self, event):
        if self.canvas.figure.axes:
            ax = self.canvas.figure.axes[0]
            x_min, x_max = ax.get_xlim()

            try:
                x_min_dt = mdates.num2date(x_min).replace(tzinfo=None)
                x_max_dt = mdates.num2date(x_max).replace(tzinfo=None)
            except Exception as e:
                print("Error al convertir fechas:", e)
                return

            # Buscar el archivo correspondiente a la fecha mínima visible
            archivo_actual = self.buscar_archivo_por_fecha(x_min_dt)

            self.label_archivo.setText(
                f"Estás viendo: {archivo_actual} ({x_min_dt.strftime('%Y-%m')} a {x_max_dt.strftime('%Y-%m')})"
            )


    def buscar_archivo_por_fecha(self, fecha):
        year_suffix = fecha.strftime('%y')  # '52', '53', '54', etc.

        for archivo in self.nombres_archivos:
            if f"h316a{year_suffix}" in archivo:
                return archivo

        return "archivo desconocido"




    def guardar_con_nombre_personalizado(self):
        
        x_min, x_max = self.ax.get_xlim()
        x_min_dt = mdates.num2date(x_min).replace(tzinfo=None)
        x_max_dt = mdates.num2date(x_max).replace(tzinfo=None)

        archivo_actual = self.buscar_archivo_por_fecha(x_min_dt)  # SOLO x_min_dt define el archivo

        self.label_archivo.setText(
            f"Estás viendo: {archivo_actual} ({x_min_dt.strftime('%Y-%m')} a {x_max_dt.strftime('%Y-%m')})"
        )

        self.ax.set_title(f"Gráfica TOGA: {archivo_actual}")
        self.canvas.draw_idle()

        x1 = x_min_dt.strftime('%Y-%m')
        x2 = x_max_dt.strftime('%Y-%m')
        nombre_sugerido = f"grafica_toga_{archivo_actual.replace('.dat', '')}_{x1}_a_{x2}.png"

        ruta, _ = QFileDialog.getSaveFileName(self, "Guardar gráfica", nombre_sugerido, "Imagen PNG (*.png)")
        if ruta:
            self.figure.savefig(ruta)
            print(f"Gráfica guardada como: {ruta}")



if __name__ == "__main__":
    app = QApplication([])
    ventana = VentanaGrafica()
    ventana.show()
    app.exec()
