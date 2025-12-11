from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
from GUI.board_screen import BoardView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quoridor Game")
        self.setGeometry(700, 300, 900, 800)

        self.ai_player = QPushButton("Play vs AI")
        self.human_player = QPushButton("Play vs Human")

        self.initUI()

        self.ai_player.clicked.connect(self.open_ai_mode)
        self.human_player.clicked.connect(self.open_human_mode)

    def initUI(self):

        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(
                    spread:pad, x1:0, y1:0, x2:1, y2:1,
                    stop:0 #EDE7F6, stop:1 #D1C4E9
                );
            }
        """)


        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 25px;
                padding: 40px;
                border: 4px solid #B39DDB;
            }
        """)

        container_layout = QVBoxLayout()
        container_layout.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(frame, alignment=Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(30)

        title = QLabel("Quoridor Game")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 42px;
            font-weight: 900;
            color: #4A148C;
            margin-bottom: 20px;
        """)

        subtitle = QLabel("Choose a Game Mode")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("""
            font-size: 22px;
            color: #6A1B9A;
            margin-bottom: 35px;
        """)

   
        button_style = """
            QPushButton {
                background-color: qlineargradient(
                    spread:pad, x1:0, y1:0, x2:1, y2:1,
                    stop:0 #AB47BC, stop:1 #7E57C2
                );
                color: white;
                padding: 18px;
                font-size: 24px;
                font-weight: bold;
                border-radius: 18px;
                min-width: 250px;
                letter-spacing: 1px;
            }
            QPushButton:hover {
                background-color: #9C27B0;
                transform: scale(1.05);
            }
            QPushButton:pressed {
                background-color: #6A1B9A;
            }
        """

        self.ai_player.setStyleSheet(button_style)
        self.human_player.setStyleSheet(button_style)


        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(self.ai_player)
        layout.addWidget(self.human_player)

        frame.setLayout(layout)
        self.setCentralWidget(QWidget())
        self.centralWidget().setLayout(container_layout)

 
    def open_ai_mode(self):
        self.board = BoardView("AI")
        self.board.show()
        self.close()

    def open_human_mode(self):
        self.board = BoardView("HUMAN")
        self.board.show()
        self.close()
