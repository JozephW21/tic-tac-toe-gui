from PyQt6.QtWidgets import (QMainWindow, QGridLayout, QPushButton, 
                           QWidget, QLabel, QVBoxLayout)
from PyQt6.QtCore import Qt, QLine, QPoint
from PyQt6.QtGui import QFont, QPainter, QPen, QColor
from .player_dialog import PlayerNameDialog

class WinningLine(QWidget):
    def __init__(self, start_pos, end_pos, parent=None):
        super().__init__(parent)
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.setStyleSheet("background: transparent;")

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen(QColor("#FF0000"), 5)  # Red color, 5px width
        painter.setPen(pen)
        painter.drawLine(self.start_pos, self.end_pos)

class TicTacToeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tic Tac Toe")
        self.setFixedSize(400, 500)
        
        # Get player names
        dialog = PlayerNameDialog()
        if dialog.exec():
            self.player1_name, self.player2_name = dialog.get_player_names()
        else:
            self.player1_name, self.player2_name = "Player 1", "Player 2"
        
        # Create central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        main_layout = QVBoxLayout(self.central_widget)
        
        # Player info layout
        info_layout = QGridLayout()
        self.p1_label = QLabel(f"{self.player1_name} (X)")
        self.p2_label = QLabel(f"{self.player2_name} (O)")
        self.p1_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.p2_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_layout.addWidget(self.p1_label, 0, 0)
        info_layout.addWidget(self.p2_label, 0, 1)
        main_layout.addLayout(info_layout)
        
        # Game layout with container for the grid and winning line
        self.game_container = QWidget()
        self.game_layout = QGridLayout(self.game_container)
        self.game_layout.setSpacing(5)
        main_layout.addWidget(self.game_container)
        
        # Initialize game variables
        self.current_player = 'X'
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.buttons = []
        self.winning_line = None
        
        # Status label
        self.status_label = QLabel(f"{self.player1_name}'s turn (X)")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setFont(QFont('Arial', 16))
        main_layout.addWidget(self.status_label)
        
        # Create game board buttons
        button_style = """
            QPushButton {
                background-color: #34495E;
                color: #ECF0F1;
                font-size: 48px;
                font-weight: bold;
                border: 2px solid #2C3E50;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #2C3E50;
            }
            QPushButton:disabled {
                color: #ECF0F1;
                background-color: #2C3E50;
            }
        """
        
        for row in range(3):
            button_row = []
            for col in range(3):
                button = QPushButton()
                button.setFixedSize(100, 100)
                button.setFont(QFont('Arial', 48))
                button.setStyleSheet(button_style)
                button.clicked.connect(lambda checked, r=row, c=col: self.make_move(r, c))
                self.game_layout.addWidget(button, row, col)
                button_row.append(button)
            self.buttons.append(button_row)
        
        # Reset button
        reset_button = QPushButton("Reset Game")
        reset_button.setFont(QFont('Arial', 16))
        reset_button.setStyleSheet("""
            QPushButton {
                background-color: #3498DB;
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980B9;
            }
        """)
        reset_button.clicked.connect(self.reset_game)
        main_layout.addWidget(reset_button)
        
        # Update player labels
        self.update_player_labels()

    def make_move(self, row, col):
        if self.board[row][col] == '' and not self.check_winner():
            self.board[row][col] = self.current_player
            self.buttons[row][col].setText(self.current_player)
            
            if self.check_winner():
                winner_name = self.player1_name if self.current_player == 'X' else self.player2_name
                self.status_label.setText(f"{winner_name} wins!")
                self.draw_winning_line()
                self.disable_board()
            elif self.is_board_full():
                self.status_label.setText("Game Draw!")
                self.disable_board()
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                current_name = self.player2_name if self.current_player == 'O' else self.player1_name
                self.status_label.setText(f"{current_name}'s turn ({self.current_player})")
                self.update_player_labels()

    def draw_winning_line(self):
        winning_combo = self.get_winning_combination()
        if winning_combo:
            # Remove existing line if present
            if self.winning_line:
                self.winning_line.deleteLater()
            
            # Calculate start and end positions for the line
            start_button = self.buttons[winning_combo[0][0]][winning_combo[0][1]]
            end_button = self.buttons[winning_combo[2][0]][winning_combo[2][1]]
            
            # Get the center points of the buttons
            start_pos = QPoint(start_button.x() + start_button.width()//2,
                             start_button.y() + start_button.height()//2)
            end_pos = QPoint(end_button.x() + end_button.width()//2,
                           end_button.y() + end_button.height()//2)
            
            # Create and show the winning line
            self.winning_line = WinningLine(start_pos, end_pos, self.game_container)
            self.winning_line.setGeometry(0, 0, self.game_container.width(), self.game_container.height())
            self.winning_line.show()

    def get_winning_combination(self):
        # Check rows
        for row in range(3):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] != '':
                return [(row, 0), (row, 1), (row, 2)]
        
        # Check columns
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != '':
                return [(0, col), (1, col), (2, col)]
        
        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != '':
            return [(0, 0), (1, 1), (2, 2)]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != '':
            return [(0, 2), (1, 1), (2, 0)]
        
        return None

    def check_winner(self):
        return self.get_winning_combination() is not None

    def is_board_full(self):
        return all(all(cell != '' for cell in row) for row in self.board)

    def disable_board(self):
        for row in self.buttons:
            for button in row:
                button.setEnabled(False)

    def update_player_labels(self):
        self.p1_label.setStyleSheet("font-weight: normal")
        self.p2_label.setStyleSheet("font-weight: normal")
        if self.current_player == 'X':
            self.p1_label.setStyleSheet("font-weight: bold; color: #3498DB")
        else:
            self.p2_label.setStyleSheet("font-weight: bold; color: #3498DB")

    def reset_game(self):
        # Remove winning line if it exists
        if self.winning_line:
            self.winning_line.deleteLater()
            self.winning_line = None
            
        # Ask for new player names
        dialog = PlayerNameDialog()
        if dialog.exec():
            self.player1_name, self.player2_name = dialog.get_player_names()
        
        self.current_player = 'X'
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.status_label.setText(f"{self.player1_name}'s turn (X)")
        
        # Update player labels
        self.p1_label.setText(f"{self.player1_name} (X)")
        self.p2_label.setText(f"{self.player2_name} (O)")
        self.update_player_labels()
        
        # Reset buttons
        for row in self.buttons:
            for button in row:
                button.setText('')
                button.setEnabled(True)