import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel,QVBoxLayout,QWidget,QPushButton,QStackedWidget,  QGraphicsOpacityEffect,QHBoxLayout,QGridLayout
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
        self.title = QLabel("Choose opponent")
        self.title.setFont(QFont("Arial", 24, QFont.Bold))
        self.title.setStyleSheet("color: #2C3E50; background-color: transparent;")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setWordWrap(True)

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
        vbox.addWidget(self.title, alignment=Qt.AlignCenter)
        vbox.addWidget(self.button_ai, alignment=Qt.AlignCenter)
        vbox.addWidget(self.button_human, alignment=Qt.AlignCenter)
        vbox.addStretch()
        vbox.setSpacing(40)
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


class Page3(QWidget):
    def __init__(self, go_back_func):
        super().__init__()
        self.setStyleSheet("background-color: #FFF9E6;")  # beige background

        self.current_turn = 1  # 1 for P1, 2 for P2

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(10)

        # Player turn label
        self.turn_label = QLabel("Player Turn: P1")
        self.turn_label.setFont(QFont("Arial", 18, QFont.Bold))
        self.turn_label.setAlignment(Qt.AlignCenter)
        self.turn_label.setStyleSheet("color: #2C3E50;")
        main_layout.addWidget(self.turn_label, alignment=Qt.AlignCenter)

        # Board grid
        grid = QGridLayout()
        grid.setSpacing(2)  # spacing between cells and walls

        cell_size = 50
        wall_thickness = 10

        # Colors
        cell_color = "#D9CBA3"  # off-white cell
        wall_color = "#8B4513"  # brown walls
        inter_color = "#D2B48C"  # lighter intersection

        self.cells = [[None for _ in range(9)] for _ in range(9)]

        for i in range(9):
            for j in range(9):
                cell = QLabel()
                cell.setFixedSize(cell_size, cell_size)
                cell.setStyleSheet(
                    f"background-color: {cell_color}; border-radius: 5px; border: 1px solid #7F8C8D;")
                cell.setAlignment(Qt.AlignCenter)
                grid.addWidget(cell, i * 2, j * 2)
                self.cells[i][j] = cell

                # Add mouse click support
                cell.mousePressEvent = lambda e, x=i, y=j: self.cell_clicked(x, y)

                # Horizontal wall
                if i < 8:
                    h_wall = QLabel()
                    h_wall.setFixedSize(cell_size, wall_thickness)
                    h_wall.setStyleSheet(f"background-color: {wall_color}; border-radius: 3px;")
                    grid.addWidget(h_wall, i * 2 + 1, j * 2)

                # Vertical wall
                if j < 8:
                    v_wall = QLabel()
                    v_wall.setFixedSize(wall_thickness, cell_size)
                    v_wall.setStyleSheet(f"background-color: {wall_color}; border-radius: 3px;")
                    grid.addWidget(v_wall, i * 2, j * 2 + 1)

                # Intersection
                if i < 8 and j < 8:
                    inter = QLabel()
                    inter.setFixedSize(wall_thickness, wall_thickness)
                    inter.setStyleSheet(f"background-color: {inter_color}; border-radius: 2px;")
                    grid.addWidget(inter, i * 2 + 1, j * 2 + 1)

        # Player icons
        self.player1_icon = QPixmap("player1.png").scaled(cell_size - 10, cell_size - 10, Qt.KeepAspectRatio,
                                                          Qt.SmoothTransformation)
        self.player2_icon = QPixmap("player2.jpg").scaled(cell_size - 10, cell_size - 10, Qt.KeepAspectRatio,
                                                          Qt.SmoothTransformation)

        # Initial positions
        self.player_positions = {1: (0, 4), 2: (8, 4)}
        self.update_players()

        main_layout.addLayout(grid)
        self.setLayout(main_layout)

    def update_players(self):
        # Clear all cells first
        for i in range(9):
            for j in range(9):
                self.cells[i][j].clear()
        # Place players
        p1_x, p1_y = self.player_positions[1]
        p2_x, p2_y = self.player_positions[2]
        self.cells[p1_x][p1_y].setPixmap(self.player1_icon)
        self.cells[p2_x][p2_y].setPixmap(self.player2_icon)

        # Update turn label
        self.turn_label.setText(f"Player Turn: P{self.current_turn}")

    def cell_clicked(self, x, y):
        # Current player
        player = self.current_turn
        px, py = self.player_positions[player]

        # Check if clicked cell is adjacent (orthogonal)
        if (abs(px - x) == 1 and py == y) or (abs(py - y) == 1 and px == x):
            # Update player position
            self.player_positions[player] = (x, y)
            # Switch turn
            self.current_turn = 2 if self.current_turn == 1 else 1
            self.update_players()

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
        self.page1 = Page1(self.go_to_page3, self.go_to_page3)
        self.page2 = Page2(self.go_to_page1)
        self.page3 = Page3(self.go_to_page2)
        # Add pages to the stack
        self.stack.addWidget(self.welcome_page)
        self.stack.addWidget(self.page1)  # index 1
        self.stack.addWidget(self.page2)  # index 2
        self.stack.addWidget(self.page3)
    def go_to_page1(self):
        self.stack.setCurrentIndex(1)

    def go_to_page2(self):
        self.stack.setCurrentIndex(2)
    def go_to_page3(self):
        self.stack.setCurrentIndex(3)

def main():
    app=QApplication(sys.argv)
    window=MainWindow()
    window.show()
    sys.exit(app.exec_())
if __name__=='__main__':
    main()