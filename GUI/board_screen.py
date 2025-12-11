from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *



class BoardView(QWidget):
    def __init__(self,mode):
        super().__init__()
        self.mode=mode
        self.setWindowTitle("Quoridor - Board")
        self.setGeometry(700, 300, 900, 800)
        layout = QVBoxLayout()
        title = QLabel(f"Game Mode: {self.mode}")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 28px; font-weight: bold;")

        layout.addWidget(title)
        self.setLayout(layout)
        