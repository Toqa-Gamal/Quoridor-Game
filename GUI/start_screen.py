from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
from GUI.board_screen import BoardView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quoridor Game")
        self.setGeometry(700, 300, 950, 820)

        self.ai_player = QPushButton("Play vs AI")
        self.human_player = QPushButton("Play vs Human")

        self.initUI()

        self.ai_player.clicked.connect(self.open_ai_mode)
        self.human_player.clicked.connect(self.open_human_mode)

    def initUI(self):

        # ===== Window Background =====
        self.setStyleSheet("""
        QMainWindow {
            background: qradialgradient(
                cx:0.5, cy:0.3, radius:1.4,
                stop:0 #FFF3E0,
                stop:0.55 #E1C699,
                stop:1 #8D6E63
            );
        }
        """)

        # ===== Main Card Frame =====
        frame = QFrame()
        frame.setStyleSheet("""
        QFrame {
            background: qlineargradient(
                x1:0, y1:0, x2:0, y2:1,
                stop:0 rgba(255,255,255,0.95),
                stop:1 rgba(240,220,195,0.95)
            );
            border-radius: 30px;
            padding: 45px;
            border: 4px solid #6D4C41;
        }
        """)

        self.addShadow(frame, blur=35, x=0, y=12)

        # ===== Layouts =====
        container_layout = QVBoxLayout()
        container_layout.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(frame)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(34)

        # ===== Title =====
        title = QLabel("QUORIDOR")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
        font-size: 48px;
        font-weight: 900;
        letter-spacing: 4px;
        color: #3E2723;
        """)

        subtitle = QLabel("Choose Game Mode")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("""
        font-size: 22px;
        color: #5D4037;
        margin-bottom: 10px;
        """)

        # ===== Button Style =====
        button_style = """
        QPushButton {
            background: qlineargradient(
                x1:0, y1:0, x2:0, y2:1,
                stop:0 #B08968,
                stop:1 #6D4C41
            );
            color: #FFF8E1;
            padding: 20px;
            font-size: 24px;
            font-weight: bold;
            border-radius: 22px;
            min-width: 280px;
            border: 3px solid #3E2723;
        }

        QPushButton:hover {
            background: #8D6E63;
        }

        QPushButton:pressed {
            background: #5D4037;
        }
        """

        self.ai_player.setStyleSheet(button_style)
        self.human_player.setStyleSheet(button_style)

        self.addShadow(self.ai_player, blur=25, x=0, y=8)
        self.addShadow(self.human_player, blur=25, x=0, y=8)

        # ===== Assemble =====
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(15)
        layout.addWidget(self.ai_player)
        layout.addWidget(self.human_player)

        frame.setLayout(layout)

        self.setCentralWidget(QWidget())
        self.centralWidget().setLayout(container_layout)

    # ===== Utilities =====
    def addShadow(self, widget, blur=20, x=0, y=6):
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(blur)
        shadow.setOffset(x, y)
        shadow.setColor(QColor(0, 0, 0, 140))
        widget.setGraphicsEffect(shadow)

    # ===== Navigation =====
    def open_ai_mode(self):
        self.board = BoardView("AI")
        self.board.show()
        self.close()

    def open_human_mode(self):
        self.board = BoardView("HUMAN")
        self.board.show()
        self.close()
