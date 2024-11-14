from PyQt6.QtWidgets import (QMainWindow, QGridLayout, QPushButton, 
                           QWidget, QLabel, QVBoxLayout, QFrame)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor, QPalette
from .player_dialog import PlayerNameDialog

class TicTacToeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tic Tac Toe")
        self.setFixedSize(500, 600)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2C3E50;
            }
            QLabel {
                color: #ECF0F1;
                padding: 10px;
            }
            QPushButton {
                background-color: #34495E;
                color: #ECF0F1;
                border: 2px solid #2980B9;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #2980B9;
            }
            QPushButton:disabled {
                background-color: #7F8C8D;
                border: 2px solid #95A5A6;
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
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Game title
        title_label = QLabel("Tic Tac Toe")
        title_label.setFont(QFont('Arial', 24, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #3498DB; padding: 20px;")
        main_layout.addWidget(title_label)
        
        # Player info layout
        info_frame = QFrame()
        info_frame.setStyleSheet("""
            QFrame {
                background-color: #34495E;
                border-radius: 15px;
                padding: 10px;
            }
        """)
        info_layout = QGridLayout(info_frame)
        
        self.p1_label = QLabel(f"{self.player1_name} (X)")
        self.p2_label = QLabel(f"{self.player2_name} (O)")
        self.p1_label.setFont(QFont('Arial', 14))
        self.p2_label.setFont(QFont('Arial', 14))
        self.p1_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.p2_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_layout.addWidget(self.p1_label, 0, 0)
        info_layout.addWidget(self.p2_label, 0, 1)
        main_layout.addWidget(info_frame)
        
        # Status label
        self.status_label = QLabel(f"{self.player1_name}'s turn (X)")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setFont(QFont('Arial', 16))
        self.status_label.setStyleSheet("""
            background-color: #34495E;
            border-radius: 15px;
            padding: 10px;
        """)
        main_layout.addWidget(self.status_label)
        
        # Game board frame
        game_frame = QFrame()
        game_frame.setStyleSheet("""
            QFrame {
                background-color: #34495E;
                border-radius: 15px;
                padding: 20px;
            }
        """)
        game_layout = QGridLayout(game_frame)
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
                button.setFixedSize(120, 120)
                button.setFont(QFont('Arial', 48, QFont.Weight.Bold))
                button.clicked.connect(lambda checked, r=row, c=col: self.make_move(r, c))
                button.setStyleSheet("""
                    QPushButton {
                        background-color: #2C3E50;
                        color: #ECF0F1;
                        border: 3px solid #3498DB;
                        border-radius: 15px;
                    }
                    QPushButton:hover {
                        background-color: #3498DB;
                    }
                    QPushButton:disabled {
                        background-color: #34495E;
                        border: 3px solid #7F8C8D;
                        color: #95A5A6;
                    }
                """)
                game_layout.addWidget(button, row, col)
                button_row.append(button)
            self.buttons.append(button_row)
        
        main_layout.addWidget(game_frame)
        
        # Reset button
        reset_button = QPushButton("New Game")
        reset_button.setFont(QFont('Arial', 16))
        reset_button.setStyleSheet("""
            QPushButton {
                background-color: #27AE60;
                color: white;
                border: none;
                border-radius: 15px;
                padding: 15px;
                min-height: 50px;
            }
            QPushButton:hover {
                background-color: #2ECC71;
            }
        """)
        reset_button.clicked.connect(self.reset_game)
        main_layout.addWidget(reset_button)
        
        # Footer frame
        footer_frame = QFrame()
        footer_frame.setStyleSheet("""
            QFrame {
                background-color: #34495E;
                border-radius: 15px;
                padding: 5px;
            }
            QLabel {
                color: #BDC3C7;
                font-size: 10px;
            }
        """)
        footer_layout = QVBoxLayout(footer_frame)
        
        # Add timestamp label
        timestamp_label = QLabel("Created: 2024-11-14 18:30:16 UTC")
        timestamp_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer_layout.addWidget(timestamp_label)
        
        # Add creator label
        creator_label = QLabel("Created by: JozephW21")
        creator_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer_layout.addWidget(creator_label)
        
        main_layout.addWidget(footer_frame)
        
        # Highlight current player
        self.update_player_labels()

    def make_move(self, row, col):
        if self.board[row][col] == '' and not self.check_winner():
            self.board[row][col] = self.current_player
            button = self.buttons[row][col]
            button.setText(self.current_player)
            if self.current_player == 'X':
                button.setStyleSheet(button.styleSheet() + "\ncolor: #3498DB;")
            else:
                button.setStyleSheet(button.styleSheet() + "\ncolor: #E74C3C;")
            
            if self.check_winner():
                winner_name = self.player1_name if self.current_player == 'X' else self.player2_name
                self.status_label.setText(f"🎉 {winner_name} wins! 🎉")
                self.status_label.setStyleSheet("""
                    background-color: #27AE60;
                    color: white;
                    border-radius: 15px;
                    padding: 10px;
                """)
                self.disable_board()
            elif self.is_board_full():
                self.status_label.setText("🤝 Game Draw! 🤝")
                self.status_label.setStyleSheet("""
                    background-color: #F39C12;
                    color: white;
                    border-radius: 15px;
                    padding: 10px;
                """)
                self.disable_board()
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                current_name = self.player2_name if self.current_player == 'O' else self.player1_name
                self.status_label.setText(f"{current_name}'s turn ({self.current_player})")
                self.update_player_labels()

    def update_player_labels(self):
        inactive_style = """
            color: #BDC3C7;
            font-weight: normal;
            padding: 10px;
        """
        active_style = """
            color: #3498DB;
            font-weight: bold;
            padding: 10px;
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
            background-color: #34495E;
            color: #ECF0F1;
            border-radius: 15px;
            padding: 10px;
        """)
        
        # Update player labels
        self.p1_label.setText(f"{self.player1_name} (X)")
        self.p2_label.setText(f"{self.player2_name} (O)")
        self.update_player_labels()
        
        for row in self.buttons:
            for button in row:
                button.setText('')
                button.setEnabled(True)
                button.setStyleSheet("""
                    QPushButton {
                        background-color: #2C3E50;
                        color: #ECF0F1;
                        border: 3px solid #3498DB;
                        border-radius: 15