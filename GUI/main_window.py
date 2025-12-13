import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel,QVBoxLayout,QWidget,QPushButton,QStackedWidget,  QGraphicsOpacityEffect
from PyQt5.QtGui import QIcon,QPixmap,QFont,QMovie
from PyQt5.QtCore import Qt,QPropertyAnimation, QEasingCurve


class WelcomePage(QWidget):
    def __init__(self, go_next_func):
        super().__init__()
        self.setStyleSheet("background-color: #F5F5F5;")  # Dark background

        # Title
        self.title = QLabel("Welcome to Quorridor Game")
        self.title.setFont(QFont("Arial", 24, QFont.Bold))
        self.title.setStyleSheet("color: #2C3E50; background-color: transparent;")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setWordWrap(True)

        # Animated dice
        self.dice_label = QLabel()
        self.dice_label.setAlignment(Qt.AlignCenter)
        self.dice_label.setStyleSheet("background-color: transparent;")  # transparent
        self.dice_label.setFixedSize(200, 200)  # adjust size
        self.dice_label.setScaledContents(True)  # scale GIF to fit

        self.dice_movie = QMovie("dice.gif")  # replace with your GIF path
        self.dice_label.setMovie(self.dice_movie)
        self.dice_movie.start()

        # Play button
        self.play_btn = QPushButton("Play")
        self.play_btn.setFixedSize(250, 80)
        self.play_btn.setStyleSheet("""
            QPushButton {
                background-color: #F1C40F;
                font-size: 29px;
                border-radius: 12px;
                color: #2C3E50;
            }
            QPushButton:hover {
                background-color: #FFD700;

            }
            QPushButton:pressed {
                background-color: #D35400;
            }
        """)
        self.play_btn.clicked.connect(go_next_func)

        # Layout
        layout = QVBoxLayout()
        layout.addStretch()
        layout.addWidget(self.title, alignment=Qt.AlignCenter)
        layout.addSpacing(20)
        layout.addWidget(self.dice_label, alignment=Qt.AlignCenter)
        layout.addSpacing(20)
        layout.addWidget(self.play_btn, alignment=Qt.AlignCenter)
        layout.addStretch()
        self.setLayout(layout)

class Page1(QWidget):
    def __init__(self, go_ai_func, go_human_func):
        super().__init__()
        self.setStyleSheet("background-color:#FFF9E6")
        self.button_ai = QPushButton("AI Opponent")
        self.button_ai.setStyleSheet("""
                    QPushButton {
                        background-color: #FFFFFF; 
                        font-size: 30px; 
                        border-radius: 10px;
                    }
                    QPushButton:hover {
                        background-color: #F1C40F; 
                    }
                """)
        self.button_ai.setFixedSize(300, 100)
        self.button_ai.clicked.connect(go_ai_func)
        self.button_human  = QPushButton("Human Opponent")
        self.button_human .setStyleSheet("""
            QPushButton {
                background-color: #FFFFFF; 
                font-size: 30px; 
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #F1C40F; 
            }
        """)
        self.button_human .setFixedSize(300, 100)
        self.button_human.clicked.connect(go_human_func)
        vbox = QVBoxLayout()
        vbox.addStretch()
        vbox.addWidget(self.button_ai, alignment=Qt.AlignCenter)
        vbox.addWidget(self.button_human, alignment=Qt.AlignCenter)
        vbox.addStretch()
        vbox.setSpacing(30)
        self.setLayout(vbox)
class Page2(QWidget):
    def __init__(self,go_back_func):
        super().__init__()
        self.setStyleSheet("background-color: #FFF9E6;")  # beige
        # Back button
        self.back_btn = QPushButton("Back to Menu")
        self.back_btn.setFixedSize(300, 100)
        self.back_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #FFFFFF; 
                        font-size: 30px; 
                        border-radius: 10px;
                        color: #2C3E50;
                    }
                    QPushButton:hover {
                        background-color: #F1C40F; 
                    }
                """)
        self.back_btn.clicked.connect(go_back_func)

        # Layout
        layout = QVBoxLayout()
        layout.addStretch()
        layout.addWidget(self.back_btn, alignment=Qt.AlignCenter)
        layout.addStretch()
        self.setLayout(layout)
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()


        self.setWindowTitle("Quorridor Game")
        self.setWindowIcon(QIcon("unnamedas.jpg"))
        self.setGeometry(700, 300, 500, 500)

        self.stack=QStackedWidget()
        self.setCentralWidget(self.stack)
        # Create pages and add to stack
        self.welcome_page = WelcomePage(self.go_to_page1)
        self.page1 = Page1(self.go_to_page2, self.go_to_page2)  # connect buttons to functions
        self.page2 = Page2(self.go_to_page1)
        # Add pages to the stack
        self.stack.addWidget(self.welcome_page)
        self.stack.addWidget(self.page1)  # index 1
        self.stack.addWidget(self.page2)  # index 2

    def go_to_page1(self):
        self.stack.setCurrentIndex(1)

    def go_to_page2(self):
        self.stack.setCurrentIndex(2)

def main():
    app=QApplication(sys.argv)
    window=MainWindow()
    window.show()
    sys.exit(app.exec_())
if __name__=='__main__':
    main()