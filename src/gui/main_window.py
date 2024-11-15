from PyQt6.QtWidgets import (QMainWindow, QGridLayout, QPushButton, 
                           QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame)
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QFont, QPainter, QPen, QColor
from .player_dialog import PlayerNameDialog

# Keep PlayerStats and WinningLine classes as they are...

class PlayerStats:
    def __init__(self, name):
        self.name = name
        self.wins = 0
        self.losses = 0
        self.draws = 0

    def add_win(self):
        self.wins += 1

    def add_loss(self):
        self.losses += 1

    def add_draw(self):
        self.draws += 1

    def get_stats_string(self):
        return f"W: {self.wins} | L: {self.losses} | D: {self.draws}"

class WinningLine(QWidget):
    def __init__(self, start_pos, end_pos, parent=None):
        super().__init__(parent)
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.setStyleSheet("background: transparent;")

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen(QColor("#E74C3C"), 8)
        painter.setPen(pen)
        painter.drawLine(self.start_pos, self.end_pos)

class TicTacToeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tic Tac Toe")
        self.setFixedSize(600, 800)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2C3E50;
            }
        """)
        
        # Initialize game variables
        self.current_player = 'X'
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.buttons = []
        self.winning_line = None
        
        # Get player names
        dialog = PlayerNameDialog()
        if dialog.exec():
            self.player1_name, self.player2_name = dialog.get_player_names()
        else:
            self.player1_name, self.player2_name = "Player 1", "Player 2"
            
        # Initialize player stats
        self.player1_stats = PlayerStats(self.player1_name)
        self.player2_stats = PlayerStats(self.player2_name)
        
        # Create central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        main_layout = QVBoxLayout(self.central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(30, 20, 30, 20)
        
        # Title
        title = QLabel("Tic Tac Toe")
        title.setStyleSheet("""
            QLabel {
                color: #3498DB;
                font-size: 32px;
                font-weight: bold;
                padding: 5px;
            }
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)
        
        # Player info layout
        player_frame = QFrame()
        player_frame.setStyleSheet("""
            QFrame {
                background-color: #34495E;
                border-radius: 10px;
                padding: 8px;
            }
            QLabel {
                color: #ECF0F1;
                font-size: 16px;
                padding: 5px;
            }
        """)
        info_layout = QGridLayout(player_frame)
        
        # Player names and stats
        self.p1_label = QLabel(f"{self.player1_name} (X)")
        self.p2_label = QLabel(f"{self.player2_name} (O)")
        self.p1_stats_label = QLabel(self.player1_stats.get_stats_string())
        self.p2_stats_label = QLabel(self.player2_stats.get_stats_string())
        
        self.p1_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.p2_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.p1_stats_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.p2_stats_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        info_layout.addWidget(self.p1_label, 0, 0)
        info_layout.addWidget(self.p2_label, 0, 1)
        info_layout.addWidget(self.p1_stats_label, 1, 0)
        info_layout.addWidget(self.p2_stats_label, 1, 1)
        main_layout.addWidget(player_frame)
        
        # Game container
        self.game_container = QFrame()
        self.game_container.setStyleSheet("""
            QFrame {
                background-color: #34495E;
                border-radius: 10px;
                padding: 20px;
                margin: 10px 0;
            }
        """)
        self.game_layout = QGridLayout(self.game_container)
        self.game_layout.setSpacing(10)
        main_layout.addWidget(self.game_container)
        
        # Create game board buttons
        button_style = """
            QPushButton {
                background-color: #2C3E50;
                color: #ECF0F1;
                font-size: 48px;
                font-weight: bold;
                border: 3px solid #34495E;
                border-radius: 10px;
                margin: 3px;
            }
            QPushButton:hover {
                background-color: #243442;
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
                button.setFixedSize(120, 120)
                button.setFont(QFont('Arial', 48))
                button.setStyleSheet(button_style)
                button.clicked.connect(lambda checked, r=row, c=col: self.make_move(r, c))
                self.game_layout.addWidget(button, row, col)
                button_row.append(button)
            self.buttons.append(button_row)
        
        # Status label
        self.status_label = QLabel(f"{self.player1_name}'s turn (X)")
        self.status_label.setStyleSheet("""
            QLabel {
                color: #ECF0F1;
                font-size: 18px;
                font-weight: bold;
                padding: 8px;
                background-color: #34495E;
                border-radius: 10px;
            }
        """)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.status_label)
        
        # Buttons container
        buttons_frame = QFrame()
        buttons_layout = QHBoxLayout(buttons_frame)
        buttons_layout.setSpacing(10)
        
        # Play Again button (same players)
        play_again_button = QPushButton("Play Again")
        play_again_button.setStyleSheet("""
            QPushButton {
                background-color: #2ECC71;
                color: white;
                padding: 12px;
                font-size: 16px;
                font-weight: bold;
                border-radius: 10px;
                min-width: 160px;
            }
            QPushButton:hover {
                background-color: #27AE60;
            }
        """)
        play_again_button.clicked.connect(self.play_again)
        
        # New Game button (new players)
        new_game_button = QPushButton("New Game")
        new_game_button.setStyleSheet("""
            QPushButton {
                background-color: #3498DB;
                color: white;
                padding: 12px;
                font-size: 16px;
                font-weight: bold;
                border-radius: 10px;
                min-width: 160px;
            }
            QPushButton:hover {
                background-color: #2980B9;
            }
        """)
        new_game_button.clicked.connect(self.new_game)
        
        buttons_layout.addWidget(play_again_button)
        buttons_layout.addWidget(new_game_button)
        main_layout.addWidget(buttons_frame)
        
        # Info section
        info_frame = QFrame()
        info_frame.setStyleSheet("""
            QFrame {
                background: none;
            }
            QLabel {
                color: #95A5A6;
                font-size: 12px;
            }
        """)
        info_layout = QVBoxLayout(info_frame)
        timestamp_label = QLabel("Created: 2024-11-15 13:34:25 UTC")
        creator_label = QLabel("Created by: JozephW21")
        timestamp_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        creator_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_layout.addWidget(timestamp_label)
        info_layout.addWidget(creator_label)
        main_layout.addWidget(info_frame)
        
        # Update player labels
        self.update_player_labels()

    def make_move(self, row, col):
        if self.board[row][col] == '' and not self.check_winner():
            self.board[row][col] = self.current_player
            self.buttons[row][col].setText(self.current_player)
            
            if self.check_winner():
                winner_name = self.player1_name if self.current_player == 'X' else self.player2_name
                self.status_label.setText(f"{winner_name} wins!")
                # Update stats
                if self.current_player == 'X':
                    self.player1_stats.add_win()
                    self.player2_stats.add_loss()
                else:
                    self.player2_stats.add_win()
                    self.player1_stats.add_loss()
                self.update_stats_display()
                self.draw_winning_line()
                self.disable_board()
            elif self.is_board_full():
                self.status_label.setText("Game Draw!")
                self.player1_stats.add_draw()
                self.player2_stats.add_draw()
                self.update_stats_display()
                self.disable_board()
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                current_name = self.player2_name if self.current_player == 'O' else self.player1_name
                self.status_label.setText(f"{current_name}'s turn ({self.current_player})")
                self.update_player_labels()

    def update_stats_display(self):
        """Update the stats display labels"""
        self.p1_stats_label.setText(self.player1_stats.get_stats_string())
        self.p2_stats_label.setText(self.player2_stats.get_stats_string())

    def play_again(self):
        if self.winning_line:
            self.winning_line.deleteLater()
            self.winning_line = None
        
        self.current_player = 'X'
        self.board = [['' for _ in range(3)] for _ in range(3)]
        
        for row in self.buttons:
            for button in row:
                button.setText('')
                button.setEnabled(True)
        
        self.status_label.setText(f"{self.player1_name}'s turn (X)")
        self.update_player_labels()

    def new_game(self):
        """Start a completely new game with new players"""
        if self.winning_line:
            self.winning_line.deleteLater()
            self.winning_line = None
            
        dialog = PlayerNameDialog()
        if dialog.exec():
            self.player1_name, self.player2_name = dialog.get_player_names()
            self.player1_stats = PlayerStats(self.player1_name)
            self.player2_stats = PlayerStats(self.player2_name)
            
            # Reset game state
            self.current_player = 'X'
            self.board = [['' for _ in range(3)] for _ in range(3)]
            
            # Clear and enable all buttons
            for row in self.buttons:
                for button in row:
                    button.setText('')
                    button.setEnabled(True)
            
            # Update labels
            self.p1_label.setText(f"{self.player1_name} (X)")
            self.p2_label.setText(f"{self.player2_name} (O)")
            self.status_label.setText(f"{self.player1_name}'s turn (X)")
            self.update_stats_display()
            self.update_player_labels()

    def draw_winning_line(self):
        """Draw a line through the winning combination"""
        winning_combo = self.get_winning_combination()
        if winning_combo:
            if self.winning_line:
                self.winning_line.deleteLater()
            
            start_button = self.buttons[winning_combo[0][0]][winning_combo[0][1]]
            end_button = self.buttons[winning_combo[2][0]][winning_combo[2][1]]
            
            start_global_pos = start_button.mapTo(self.game_container, 
                                                QPoint(start_button.width()//2, 
                                                      start_button.height()//2))
            end_global_pos = end_button.mapTo(self.game_container, 
                                            QPoint(end_button.width()//2, 
                                                  end_button.height()//2))
            
            self.winning_line = WinningLine(start_global_pos, end_global_pos, self.game_container)
            self.winning_line.setGeometry(0, 0, 
                                        self.game_container.width(), 
                                        self.game_container.height())
            self.winning_line.show()

    def get_winning_combination(self):
        """Return the winning combination if there is one"""
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
        """Check if there is a winner"""
        return self.get_winning_combination() is not None

    def is_board_full(self):
        """Check if the board is full (draw)"""
        return all(all(cell != '' for cell in row) for row in self.board)

    def disable_board(self):
        """Disable all buttons on the board"""
        for row in self.buttons:
            for button in row:
                button.setEnabled(False)

    def update_player_labels(self):
        """Update the player labels to show who's turn it is"""
        inactive_style = """
            color: #ECF0F1;
            font-weight: normal;
        """
        active_style = """
            color: #3498DB;
            font-weight: bold;
        """
        self.p1_label.setStyleSheet(inactive_style)
        self.p2_label.setStyleSheet(inactive_style)
        if self.current_player == 'X':
            self.p1_label.setStyleSheet(active_style)
        else:
            self.p2_label.setStyleSheet(active_style)