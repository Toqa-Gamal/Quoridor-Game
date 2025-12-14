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
        self.setGeometry(600, 200, 980, 900)

        self.cells = {}
        self.board_created = Board(self.mode == 'AI')

        self.initUI()

    def initUI(self):
        main_layout = QHBoxLayout()
        board_container = QVBoxLayout()

        # ===== Global Style =====
        self.setStyleSheet("""
        QWidget {
            background: qradialgradient(
                cx:0.5, cy:0.3, radius:1.2,
                stop:0 #FFF3E0,
                stop:0.5 #E6C9A8,
                stop:1 #B08968
            );
        }
        QLabel {
            font-family: 'Segoe UI';
        }
        """)

        # ===== Title =====
        title = QLabel(f"Quoridor - {self.mode} Mode")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
        font-size: 36px;
        font-weight: 900;
        letter-spacing: 1px;
        color: #3E2723;
        padding: 18px;
        background: qlineargradient(
            x1:0, y1:0, x2:1, y2:0,
            stop:0 #FFF8E1,
            stop:1 #EAD7B7
        );
        border-radius: 18px;
        border: 3px solid #8D6E63;
        """)
        board_container.addWidget(title)

        # ===== Board Grid =====
        grid_widget = QWidget()
        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)

        tile_style = """
        QPushButton {
            background: qlineargradient(
                x1:0, y1:0, x2:0, y2:1,
                stop:0 #F7E7CE,
                stop:1 #E2C9A1
            );
            border: 2px solid #9E7C52;
            border-radius: 16px;
            min-width: 68px;
            min-height: 68px;
        }

        QPushButton:hover {
            background: #EAD4B2;
            border: 2px solid #7A5736;
        }
        """

        for r in range(self.GRID_SIZE):
            for c in range(self.GRID_SIZE):
                btn = QPushButton()
                btn.setStyleSheet(tile_style)
                btn.setProperty("row", r)
                btn.setProperty("col", c)
                btn.clicked.connect(self.handleCellClick)

                self.addShadow(btn, blur=10, x=3, y=3)

                self.cells[(r, c)] = btn
                grid_layout.addWidget(btn, r, c)

        grid_widget.setLayout(grid_layout)
        board_container.addWidget(grid_widget)

        # ===== Place Pawns =====
        p1_r, p1_c = self.board_created.pawns["P1"]
        p2_r, p2_c = self.board_created.pawns["P2"]

        self.placePawn(p1_r, p1_c, "#6D4C41")   # Player 1
        self.placePawn(p2_r, p2_c, "#A1887F")   # Player 2

        # ===== Side Panel =====
        side_panel = QVBoxLayout()
        side_panel.setAlignment(Qt.AlignTop)

        self.label_turn = QLabel(f"Current Turn: {self.board_created.current_player}")
        self.label_turn.setStyleSheet("""
        font-size: 24px;
        font-weight: bold;
        color: #3E2723;
        padding: 14px;
        background-color: rgba(255,248,230,0.95);
        border-radius: 16px;
        border: 2px solid #8D6E63;
        """)
        side_panel.addWidget(self.label_turn)

        button_style = """
        QPushButton {
            background: qlineargradient(
                x1:0, y1:0, x2:0, y2:1,
                stop:0 #A97458,
                stop:1 #6D4C41
            );
            color: #FFF8E1;
            padding: 16px;
            border-radius: 20px;
            font-size: 20px;
            font-weight: bold;
            border: 2px solid #3E2723;
        }

        QPushButton:hover {
            background: #8D6E63;
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

    # ================= Game Logic =================

    def handleCellClick(self):
        btn = self.sender()
        r = btn.property("row")
        c = btn.property("col")

        current_player = self.board_created.current_player
        old_r, old_c = self.board_created.pawns[current_player]

        color = "#6D4C41" if current_player == "P1" else "#A1887F"

        moved = self.board_created.move_pawn(current_player, (r, c))
        if moved:
            self.clearCell(old_r, old_c)
            self.placePawn(r, c, color)
            self.label_turn.setText(f"Current Turn: {self.board_created.current_player}")
        else:
            print("Invalid move!")

    def clearCell(self, row, col):
        btn = self.cells[(row, col)]
        btn.setGraphicsEffect(None)
        btn.setStyleSheet("""
        QPushButton {
            background: qlineargradient(
                x1:0, y1:0, x2:0, y2:1,
                stop:0 #F7E7CE,
                stop:1 #E2C9A1
            );
            border: 2px solid #9E7C52;
            border-radius: 16px;
            min-width: 68px;
            min-height: 68px;
        }
        """)
        self.addShadow(btn, blur=10, x=3, y=3)

    def placePawn(self, row, col, base_color):
        btn = self.cells[(row, col)]
        btn.setGraphicsEffect(None)

        btn.setStyleSheet(f"""
        QPushButton {{
            background: qradialgradient(
                cx:0.3, cy:0.3, radius:0.8,
                stop:0 #FFFFFF,
                stop:0.35 {base_color},
                stop:1 #3E2723
            );
            border-radius: 34px;
            border: 4px solid #FFF8E1;
            min-width: 68px;
            min-height: 68px;
        }}
        """)

        glow = QGraphicsDropShadowEffect(self)
        glow.setBlurRadius(25)
        glow.setOffset(0, 0)
        glow.setColor(QColor(255, 255, 255, 180))
        btn.setGraphicsEffect(glow)

    def addShadow(self, widget, blur=12, x=2, y=2):
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(blur)
        shadow.setOffset(x, y)
        shadow.setColor(QColor(0, 0, 0, 120))
        widget.setGraphicsEffect(shadow)

    def resetGame(self):
        for r in range(self.GRID_SIZE):
            for c in range(self.GRID_SIZE):
                self.clearCell(r, c)

        self.board_created = Board(self.mode == 'AI')

        p1_r, p1_c = self.board_created.pawns["P1"]
        p2_r, p2_c = self.board_created.pawns["P2"]

        self.placePawn(p1_r, p1_c, "#6D4C41")
        self.placePawn(p2_r, p2_c, "#A1887F")

        self.label_turn.setText(f"Current Turn: {self.board_created.current_player}")
