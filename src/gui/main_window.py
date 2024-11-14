from PyQt6.QtWidgets import QMainWindow, QGridLayout, QPushButton, QWidget, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class TicTacToeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tic Tac Toe")
        self.setFixedSize(400, 450)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QGridLayout(central_widget)
        
        # Initialize game variables
        self.current_player = 'X'
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.buttons = []
        
        # Status label
        self.status_label = QLabel(f"Player {self.current_player}'s turn")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setFont(QFont('Arial', 16))
        layout.addWidget(self.status_label, 0, 0, 1, 3)
        
        # Create game board buttons
        for row in range(3):
            button_row = []
            for col in range(3):
                button = QPushButton()
                button.setFixedSize(100, 100)
                button.setFont(QFont('Arial', 48))
                button.clicked.connect(lambda checked, r=row, c=col: self.make_move(r, c))
                layout.addWidget(button, row + 1, col)
                button_row.append(button)
            self.buttons.append(button_row)
        
        # Reset button
        reset_button = QPushButton("Reset Game")
        reset_button.setFont(QFont('Arial', 16))
        reset_button.clicked.connect(self.reset_game)
        layout.addWidget(reset_button, 4, 0, 1, 3)

    def make_move(self, row, col):
        if self.board[row][col] == '' and not self.check_winner():
            self.board[row][col] = self.current_player
            self.buttons[row][col].setText(self.current_player)
            
            if self.check_winner():
                self.status_label.setText(f"Player {self.current_player} wins!")
                self.disable_board()
            elif self.is_board_full():
                self.status_label.setText("Game Draw!")
                self.disable_board()
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                self.status_label.setText(f"Player {self.current_player}'s turn")

    def check_winner(self):
        # Check rows
        for row in range(3):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] != '':
                return True
        
        # Check columns
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != '':
                return True
        
        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != '':
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != '':
            return True
        
        return False

    def is_board_full(self):
        return all(all(cell != '' for cell in row) for row in self.board)

    def disable_board(self):
        for row in self.buttons:
            for button in row:
                button.setEnabled(False)

    def reset_game(self):
        self.current_player = 'X'
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.status_label.setText(f"Player {self.current_player}'s turn")
        
        for row in self.buttons:
            for button in row:
                button.setText('')
                button.setEnabled(True)
