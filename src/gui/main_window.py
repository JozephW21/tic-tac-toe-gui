from PyQt6.QtWidgets import (QMainWindow, QGridLayout, QPushButton, 
                           QWidget, QLabel, QVBoxLayout)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPalette, QColor
from .player_dialog import PlayerNameDialog

class TicTacToeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tic Tac Toe")
        self.setFixedSize(400, 500)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2C3E50;
            }
            QLabel {
                color: #ECF0F1;
                font-size: 16px;
                margin: 5px;
            }
            QPushButton {
                background-color: #34495E;
                color: #ECF0F1;
                border: 2px solid #45B39D;
                border-radius: 15px;
                min-height: 40px;
            }
            QPushButton:hover {
                background-color: #45B39D;
            }
            QPushButton:disabled {
                background-color: #7F8C8D;
                border-color: #95A5A6;
            }
        """)
        
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
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Player info layout
        info_layout = QGridLayout()
        self.p1_label = QLabel(f"{self.player1_name} (X)")
        self.p2_label = QLabel(f"{self.player2_name} (O)")
        self.p1_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.p2_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_layout.addWidget(self.p1_label, 0, 0)
        info_layout.addWidget(self.p2_label, 0, 1)
        main_layout.addLayout(info_layout)
        
        # Status label
        self.status_label = QLabel(f"{self.player1_name}'s turn (X)")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setFont(QFont('Arial', 16))
        self.status_label.setStyleSheet("""
            QLabel {
                background-color: #34495E;
                padding: 10px;
                border-radius: 10px;
                font-weight: bold;
            }
        """)
        main_layout.addWidget(self.status_label)
        
        # Game layout
        game_layout = QGridLayout()
        game_layout.setSpacing(10)
        
        # Initialize game variables
        self.current_player = 'X'
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.buttons = []
        
        # Create game board buttons
        for row in range(3):
            button_row = []
            for col in range(3):
                button = QPushButton()
                button.setFixedSize(100, 100)
                button.setFont(QFont('Arial', 48, QFont.Weight.Bold))
                button.setStyleSheet("""
                    QPushButton {
                        background-color: #34495E;
                        color: #ECF0F1;
                        border: 3px solid #45B39D;
                        border-radius: 15px;
                    }
                    QPushButton:hover {
                        background-color: #3D5A80;
                    }
                    QPushButton:disabled {
                        background-color: #2C3E50;
                        color: #95A5A6;
                        border-color: #7F8C8D;
                    }
                """)
                button.clicked.connect(lambda checked, r=row, c=col: self.make_move(r, c))
                game_layout.addWidget(button, row, col)
                button_row.append(button)
            self.buttons.append(button_row)
        
        main_layout.addLayout(game_layout)
        
        # Reset button
        reset_button = QPushButton("New Game")
        reset_button.setFont(QFont('Arial', 16))
        reset_button.setStyleSheet("""
            QPushButton {
                background-color: #E74C3C;
                color: white;
                border: none;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #C0392B;
            }
        """)
        reset_button.clicked.connect(self.reset_game)
        main_layout.addWidget(reset_button)
        
        # Footer labels
        footer_layout = QVBoxLayout()
        
        timestamp_label = QLabel("Created: 2024-01-14")
        timestamp_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        timestamp_label.setStyleSheet("color: #95A5A6; font-size: 12px;")
        footer_layout.addWidget(timestamp_label)
        
        creator_label = QLabel("Created by: JozephW21")
        creator_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        creator_label.setStyleSheet("color: #95A5A6; font-size: 12px;")
        footer_layout.addWidget(creator_label)
        
        main_layout.addLayout(footer_layout)
        
        # Highlight current player
        self.update_player_labels()

    def make_move(self, row, col):
        if self.board[row][col] == '' and not self.check_winner():
            self.board[row][col] = self.current_player
            button = self.buttons[row][col]
            button.setText(self.current_player)
            if self.current_player == 'X':
                button.setStyleSheet(button.styleSheet() + "color: #3498DB;")
            else:
                button.setStyleSheet(button.styleSheet() + "color: #E74C3C;")
            
            if self.check_winner():
                winner_name = self.player1_name if self.current_player == 'X' else self.player2_name
                self.status_label.setText(f"🎉 {winner_name} wins! 🎉")
                self.status_label.setStyleSheet("""
                    QLabel {
                        background-color: #27AE60;
                        color: white;
                        padding: 10px;
                        border-radius: 10px;
                        font-weight: bold;
                    }
                """)
                self.disable_board()
            elif self.is_board_full():
                self.status_label.setText("Game Draw! 🤝")
                self.status_label.setStyleSheet("""
                    QLabel {
                        background-color: #F39C12;
                        color: white;
                        padding: 10px;
                        border-radius: 10px;
                        font-weight: bold;
                    }
                """)
                self.disable_board()
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                current_name = self.player2_name if self.current_player == 'O' else self.player1_name
                self.status_label.setText(f"{current_name}'s turn ({self.current_player})")
                self.update_player_labels()

    def update_player_labels(self):
        inactive_style = """
            QLabel {
                color: #95A5A6;
                font-weight: normal;
                padding: 5px;
                border-radius: 5px;
            }
        """
        active_style = """
            QLabel {
                color: #45B39D;
                font-weight: bold;
                padding: 5px;
                border-radius: 5px;
                background-color: #34495E;
            }
        """
        
        self.p1_label.setStyleSheet(active_style if self.current_player == 'X' else inactive_style)
        self.p2_label.setStyleSheet(active_style if self.current_player == 'O' else inactive_style)

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
        # Ask for new player names
        dialog = PlayerNameDialog()
        if dialog.exec():
            self.player1_name, self.player2_name = dialog.get_player_names()
        
        self.current_player = 'X'
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.status_label.setText(f"{self.player1_name}'s turn (X)")
        self.status_label.setStyleSheet("""
            QLabel {
                background-color: #34495E;
                color: #ECF0F1;
                padding: 10px;
                border-radius: 10px;
                font-weight: bold;
            }
        """)
        
        # Update player labels
        self.p1_label.setText(f"{self.player1_name} (X)")
        self.p2_label.setText(f"{self.player2_name} (O)")
        self.update_player_labels()
        
        # Reset buttons
        for row in self.buttons:
            for button in row:
                button.setText('')
                button.setEnabled(True)
                button.setStyleSheet("""
                    QPushButton {
                        background-color: #34495E;
                        color: #ECF0F1;
                        border: 3px solid #45B39D;
                        border-radius: 15px;
                    }
                    QPushButton:hover {
                        background-color: #3D5A80;
                    }
                    QPushButton:disabled {
                        background-color: #2C3E50;
                        color: #95A5A6;
                        border-color: #7F8C8D;
                    }
                """)