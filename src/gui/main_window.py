from PyQt6.QtWidgets import (QMainWindow, QGridLayout, QPushButton, 
                           QWidget, QLabel, QVBoxLayout)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from .player_dialog import PlayerNameDialog

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
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Player info layout
        info_layout = QGridLayout()
        self.p1_label = QLabel(f"{self.player1_name} (X)")
        self.p2_label = QLabel(f"{self.player2_name} (O)")
        self.p1_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.p2_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_layout.addWidget(self.p1_label, 0, 0)
        info_layout.addWidget(self.p2_label, 0, 1)
        main_layout.addLayout(info_layout)
        
        # Game layout
        game_layout = QGridLayout()
        
        # Initialize game variables
        self.current_player = 'X'
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.buttons = []
        
        # Status label
        self.status_label = QLabel(f"{self.player1_name}'s turn (X)")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setFont(QFont('Arial', 16))
        main_layout.addWidget(self.status_label)
        
        # Create game board buttons
        for row in range(3):
            button_row = []
            for col in range(3):
                button = QPushButton()
                button.setFixedSize(100, 100)
                button.setFont(QFont('Arial', 48))
                button.clicked.connect(lambda checked, r=row, c=col: self.make_move(r, c))
                game_layout.addWidget(button, row, col)
                button_row.append(button)
            self.buttons.append(button_row)
        
        main_layout.addLayout(game_layout)
        
        # Reset button
        reset_button = QPushButton("Reset Game")
        reset_button.setFont(QFont('Arial', 16))
        reset_button.clicked.connect(self.reset_game)
        main_layout.addWidget(reset_button)
        
        # Highlight current player
        self.update_player_labels()

    def make_move(self, row, col):
        if self.board[row][col] == '' and not self.check_winner():
            self.board[row][col] = self.current_player
            self.buttons[row][col].setText(self.current_player)
            
            if self.check_winner():
                winner_name = self.player1_name if self.current_player == 'X' else self.player2_name
                self.status_label.setText(f"{winner_name} wins!")
                self.disable_board()
            elif self.is_board_full():
                self.status_label.setText("Game Draw!")
                self.disable_board()
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                current_name = self.player2_name if self.current_player == 'O' else self.player1_name
                self.status_label.setText(f"{current_name}'s turn ({self.current_player})")
                self.update_player_labels()

    def update_player_labels(self):
        # Highlight current player
        self.p1_label.setStyleSheet("font-weight: normal")
        self.p2_label.setStyleSheet("font-weight: normal")
        if self.current_player == 'X':
            self.p1_label.setStyleSheet("font-weight: bold; color: blue")
        else:
            self.p2_label.setStyleSheet("font-weight: bold; color: blue")

    def reset_game(self):
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
        
        for row in self.buttons:
            for button in row:
                button.setText('')
                button.setEnabled(True)
