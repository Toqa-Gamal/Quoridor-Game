from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Core.board import Board

class BoardView(QWidget):
    GRID_SIZE = 9

    def __init__(self, mode):
        super().__init__()
        self.mode = mode
        self.setWindowTitle("Quoridor - Game Board")
        self.setGeometry(600, 200, 950, 900)

        self.cells = {}
        self.board_created = Board(self.mode == 'AI')
        self.initUI()

    def initUI(self):
   
        main_layout = QHBoxLayout()
        board_container = QVBoxLayout()

        # Background gradient
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    spread:pad, x1:0, y1:0, x2:1, y2:1,
                    stop:0 #F3E5F5, stop:1 #D1C4E9
                );
            }
        """)

     
        title = QLabel(f"Quoridor - {self.mode} Mode")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 34px;
            font-weight: bold;
            color: #4A148C;
            padding: 15px;
            border-radius: 15px;
            background-color: rgba(255,255,255,0.7);
            margin-bottom: 20px;
        """)
        board_container.addWidget(title)

        grid_widget = QWidget()
        grid_layout = QGridLayout()
        grid_layout.setSpacing(12)

        tile_style = """
            QPushButton {
                background-color: #F8F5FF;
                border: 2px solid #C7B7E5;
                border-radius: 10px;
                min-width: 60px;
                min-height: 60px;
                box-shadow: 3px 3px 8px rgba(0,0,0,0.3);
            }
            QPushButton:hover {
                background-color: #E5DAFF;
                border: 2px solid #9C7EDB;
            }
        """

        for r in range(self.GRID_SIZE):
            for c in range(self.GRID_SIZE):
                btn = QPushButton("")
                btn.setStyleSheet(tile_style)
                btn.setProperty("row", r)
                btn.setProperty("col", c)
                btn.clicked.connect(self.handleCellClick)

                self.cells[(r, c)] = btn
                grid_layout.addWidget(btn, r, c)

        grid_widget.setLayout(grid_layout)
        board_container.addWidget(grid_widget)

       
        p1_r, p1_c = self.board_created.pawns["P1"]
        p2_r, p2_c = self.board_created.pawns["P2"]

        self.placePawn(p1_r, p1_c, "#4A148C")
        self.placePawn(p2_r, p2_c, "#7E57C2")


        side_panel = QVBoxLayout()
        side_panel.setAlignment(Qt.AlignTop)

        self.label_turn = QLabel(f"Current Turn: {self.board_created.current_player}")
        self.label_turn.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #4A148C;
            padding: 10px;
            background-color: rgba(255,255,255, 0.8);
            border-radius: 14px;
        """)
        side_panel.addWidget(self.label_turn)

        # Buttons
        button_style = """
            QPushButton {
                background-color: #7E57C2;
                color: white;
                padding: 14px;
                border-radius: 16px;
                font-size: 19px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #6A45AF;
            }
        """

        reset_btn = QPushButton("Restart Game")
        reset_btn.setStyleSheet(button_style)
        reset_btn.clicked.connect(self.resetGame)

        back_btn = QPushButton("Back to Menu")
        back_btn.setStyleSheet(button_style)

        side_panel.addSpacing(40)
        side_panel.addWidget(reset_btn)
        side_panel.addWidget(back_btn)

        main_layout.addLayout(board_container, stretch=5)
        main_layout.addLayout(side_panel, stretch=2)

        self.setLayout(main_layout)

    def handleCellClick(self):
        btn = self.sender()
        r = btn.property("row")
        c = btn.property("col")

        current_player = self.board_created.current_player
        old_r, old_c = self.board_created.pawns[current_player]
        color = "#4A148C" if current_player == "P1" else "#7E57C2"

        moved = self.board_created.move_pawn(current_player, (r, c))

        if moved:
            self.clearCell(old_r, old_c)
            self.placePawn(r, c, color)
            self.label_turn.setText(f"Current Turn: {self.board_created.current_player}")
        else:
            print("Invalid move!")

    def clearCell(self, row, col):
        btn = self.cells[(row, col)]
        btn.setStyleSheet("""
            QPushButton {
                background-color: #F8F5FF;
                border: 2px solid #C7B7E5;
                border-radius: 10px;
                min-width: 60px;
                min-height: 60px;
            }
        """)

    def placePawn(self, row, col, color):
        btn = self.cells[(row, col)]
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                border-radius: 30px;
                border: 4px solid white;
                min-width: 60px;
                min-height: 60px;
                box-shadow: 0px 0px 15px rgba(0,0,0,0.4);
            }}
        """)

    def resetGame(self):
        for r in range(self.GRID_SIZE):
            for c in range(self.GRID_SIZE):
                self.clearCell(r, c)

        self.board_created = Board(self.mode == 'AI')

        p1_r, p1_c = self.board_created.pawns["P1"]
        p2_r, p2_c = self.board_created.pawns["P2"]

        self.placePawn(p1_r, p1_c, "#4A148C")
        self.placePawn(p2_r, p2_c, "#7E57C2")

        self.label_turn.setText(f"Current Turn: {self.board_created.current_player}")
