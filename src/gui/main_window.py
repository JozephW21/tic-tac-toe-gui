from PyQt6.QtWidgets import (QMainWindow, QGridLayout, QPushButton, 
                           QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame)
from PyQt6.QtCore import Qt, QTimer, QPoint
from PyQt6.QtGui import QFont, QPainter, QPen, QColor
from .player_dialog import PlayerNameDialog

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

class WinningLine(QFrame):
    def __init__(self, start_point, end_point, parent=None):
        super().__init__(parent)
        self.start_point = start_point
        self.end_point = end_point
        self.setStyleSheet("background: transparent;")

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen(QColor("#3498DB"), 5)
        painter.setPen(pen)
        painter.drawLine(self.start_point, self.end_point)

class TicTacToeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tic Tac Toe")
        self.setFixedSize(700, 900)
        
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
        
        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        self.main_layout = QVBoxLayout(main_widget)

        # Player info frame
        self.player_frame = QFrame()
        self.player_frame.setStyleSheet("""
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
        
        # Create layout for player frame
        player_layout = QGridLayout()
        self.player_frame.setLayout(player_layout)
        
        # Player names and stats
        self.p1_label = QLabel(f"{self.player1_name} (X)")
        self.p2_label = QLabel(f"{self.player2_name} (O)")
        self.p1_stats_label = QLabel(self.player1_stats.get_stats_string())
        self.p2_stats_label = QLabel(self.player2_stats.get_stats_string())
        
        # Add timer label
        self.timer_label = QLabel("00:00")
        self.timer_label.setStyleSheet("""
            QLabel {
                color: #3498DB;
                font-size: 24px;
                font-weight: bold;
                padding: 5px;
                background-color: #2C3E50;
                border-radius: 8px;
                min-width: 100px;
                text-align: center;
            }
        """)
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Setup timer
        self.game_timer = QTimer()
        self.seconds_elapsed = 0
        self.game_timer.timeout.connect(self.update_timer)
        
        # Layout arrangement for player frame
        player_layout.addWidget(self.p1_label, 0, 0)
        player_layout.addWidget(self.timer_label, 0, 1)
        player_layout.addWidget(self.p2_label, 0, 2)
        player_layout.addWidget(self.p1_stats_label, 1, 0)
        player_layout.addWidget(self.p2_stats_label, 1, 2)
        
        # Add player frame to main layout
        self.main_layout.addWidget(self.player_frame)

        # Game container
        self.game_container = QFrame()
        self.game_container.setStyleSheet("""
            QFrame {
                background-color: #34495E;
                border-radius: 10px;
                padding: 30px;
                margin: 20px 0;
            }
        """)
        self.game_layout = QGridLayout(self.game_container)
        self.game_layout.setSpacing(20)
        self.game_layout.setContentsMargins(20, 20, 20, 20)
        
        # Create game board buttons
        button_style = """
            QPushButton {
                background-color: #2C3E50;
                color: #ECF0F1;
                font-size: 48px;
                font-weight: bold;
                border: 3px solid #34495E;
                border-radius: 10px;
                margin: 5px;
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
                button.setFixedSize(150, 150)
                button.setFont(QFont('Arial', 60))
                button.setStyleSheet(button_style)
                button.clicked.connect(lambda checked, r=row, c=col: self.make_move(r, c))
                self.game_layout.addWidget(button, row, col)
                button_row.append(button)
            self.buttons.append(button_row)
        
        # Add game container to main layout
        self.main_layout.addWidget(self.game_container)

        # Status label
        self.status_label = QLabel(f"{self.player1_name}'s turn (X)")
        self.status_label.setStyleSheet("""
            QLabel {
                color: #ECF0F1;
                font-size: 18px;
                font-weight: bold;
                padding: 8px;
            }
        """)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.status_label)

        # Control buttons
        button_layout = QHBoxLayout()
        
        self.play_again_button = QPushButton("Play Again")
        self.play_again_button.setStyleSheet("""
            QPushButton {
                background-color: #2ECC71;
                color: #ECF0F1;
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
        self.play_again_button.clicked.connect(self.play_again)
        
        self.new_game_button = QPushButton("New Game")
        self.new_game_button.setStyleSheet("""
            QPushButton {
                background-color: #3498DB;
                color: #ECF0F1;
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
        self.new_game_button.clicked.connect(self.new_game)
        
        button_layout.addWidget(self.play_again_button)
        button_layout.addWidget(self.new_game_button)
        self.main_layout.addLayout(button_layout)
        
        # Start the timer
        self.game_timer.start(1000)

    def update_timer(self):
        """Update the timer display"""
        self.seconds_elapsed += 1
        minutes = self.seconds_elapsed // 60
        seconds = self.seconds_elapsed % 60
        self.timer_label.setText(f"{minutes:02d}:{seconds:02d}")

    def make_move(self, row, col):
        """Handle a player's move"""
        if self.board[row][col] == '' and not self.check_winner():
            self.board[row][col] = self.current_player
            self.buttons[row][col].setText(self.current_player)
            
            if self.check_winner():
                winner_name = self.player1_name if self.current_player == 'X' else self.player2_name
                self.status_label.setText(f"{winner_name} wins!")
                # Stop timer when game ends
                self.game_timer.stop()
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
                # Stop timer when game ends
                self.game_timer.stop()
                self.player1_stats.add_draw()
                self.player2_stats.add_draw()
                self.update_stats_display()
                self.disable_board()
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                current_name = self.player2_name if self.current_player == 'O' else self.player1_name
                self.status_label.setText(f"{current_name}'s turn ({self.current_player})")
                self.update_player_labels()

    def check_winner(self):
        """Check if there's a winner"""
        # Check rows
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != '':
                self.winning_line_coords = [(i, 0), (i, 2)]
                return True

        # Check columns
        for i in range(3):
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != '':
                self.winning_line_coords = [(0, i), (2, i)]
                return True

        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != '':
            self.winning_line_coords = [(0, 0), (2, 2)]
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != '':
            self.winning_line_coords = [(0, 2), (2, 0)]
            return True

        return False

    def is_board_full(self):
        """Check if the board is full"""
        return all(all(cell != '' for cell in row) for row in self.board)

    def disable_board(self):
        """Disable all board buttons"""
        for row in self.buttons:
            for button in row:
                button.setEnabled(False)

    def update_stats_display(self):
        """Update the display of player statistics"""
        self.p1_stats_label.setText(self.player1_stats.get_stats_string())
        self.p2_stats_label.setText(self.player2_stats.get_stats_string())

    def update_player_labels(self):
        """Update player labels to show current turn"""
        if self.current_player == 'X':
            self.p1_label.setStyleSheet("QLabel { color: #3498DB; font-weight: bold; }")
            self.p2_label.setStyleSheet("QLabel { color: #ECF0F1; }")
        else:
            self.p1_label.setStyleSheet("QLabel { color: #ECF0F1; }")
            self.p2_label.setStyleSheet("QLabel { color: #3498DB; font-weight: bold; }")

    def draw_winning_line(self):
        """Draw the winning line"""
        if hasattr(self, 'winning_line_coords'):
            self.winning_line = WinningLine(
                self.game_container,
                self.buttons[self.winning_line_coords[0][0]][self.winning_line_coords[0][1]],
                self.buttons[self.winning_line_coords[1][0]][self.winning_line_coords[1][1]]
            )
            self.winning_line.show()

    def play_again(self):
        """Reset the game board but keep the same players and their scores"""
        if self.winning_line:
            self.winning_line.deleteLater()
            self.winning_line = None
        
        self.current_player = 'X'
        self.board = [['' for _ in range(3)] for _ in range(3)]
        
        # Reset timer
        self.seconds_elapsed = 0
        self.timer_label.setText("00:00")
        self.game_timer.start()
        
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
            
            # Reset game state and timer
            self.current_player = 'X'
            self.board = [['' for _ in range(3)] for _ in range(3)]
            self.seconds_elapsed = 0
            self.timer_label.setText("00:00")
            self.game_timer.start()
            
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

class WinningLine(QWidget):
    def __init__(self, parent, start_button, end_button):
        super().__init__(parent)
        self.start_button = start_button
        self.end_button = end_button
        self.resize(parent.size())
        self.show()

    def paintEvent(self, event):
        if self.start_button and self.end_button:
            painter = QPainter(self)
            pen = QPen(QColor("#2ECC71"), 5)
            painter.setPen(pen)
            
            start_pos = self.start_button.geometry().center()
            end_pos = self.end_button.geometry().center()
            
            painter.drawLine(start_pos, end_pos)