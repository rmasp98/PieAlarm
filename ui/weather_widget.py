
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

icons = {"sunny":"ui/icons/sun.png"}

class WeatherWidget(QWidget):
    def __init__(self, parent=None):
        super(WeatherWidget, self).__init__(parent)
        self.Set(22, "sunny")
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)

    def Set(self, temp, weather):
        temp = QLabel(str(temp))
        temp.setAlignment(Qt.AlignCenter)
        # temp.setStyleSheet("border: 1px inset grey")

        pixmap = QPixmap(icons[weather])
        image = QLabel()
        image.setPixmap(pixmap.scaledToWidth(100))
        image.setAlignment(Qt.AlignCenter)
        # image.setStyleSheet("border: 1px inset grey")

        # layout = QVBoxLayout()
        # layout.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(image)
        self.layout.addWidget(temp)

        # self.setLayout(layout)
        