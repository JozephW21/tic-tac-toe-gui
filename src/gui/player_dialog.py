from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
                           QLabel, QLineEdit, QPushButton)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPalette, QColor

class PlayerNameDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Enter Player Names")
        self.setModal(True)
        self.setFixedSize(400, 200)
        
        # Set background color
        self.setStyleSheet("""
            QDialog {
                background-color: #2C3E50;
            }
            QLabel {
                color: #ECF0F1;
                font-size: 14px;
                font-weight: bold;
                margin: 5px;
            }
            QLineEdit {
                padding: 8px;
                font-size: 14px;
                border: 2px solid #3498DB;
                border-radius: 8px;
                background-color: #34495E;
                color: #ECF0F1;
            }
            QLineEdit:focus {
                border: 2px solid #2ECC71;
            }
            QPushButton {
                background-color: #3498DB;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 16px;
                font-weight: bold;
                border-radius: 8px;
                min-width: 150px;
            }
            QPushButton:hover {
                background-color: #2980B9;
            }
            QPushButton:pressed {
                background-color: #2574A9;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("Welcome to Tic Tac Toe!")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            font-size: 24px;
            color: #3498DB;
            margin-bottom: 10px;
        """)
        layout.addWidget(title)
        
        # Player 1 input
        p1_layout = QVBoxLayout()
        p1_label = QLabel("Player 1 (X):")
        self.p1_input = QLineEdit()
        self.p1_input.setPlaceholderText("Enter name")
        p1_layout.addWidget(p1_label)
        p1_layout.addWidget(self.p1_input)
        
        # Player 2 input
        p2_layout = QVBoxLayout()
        p2_label = QLabel("Player 2 (O):")
        self.p2_input = QLineEdit()
        self.p2_input.setPlaceholderText("Enter name")
        p2_layout.addWidget(p2_label)
        p2_layout.addWidget(self.p2_input)
        
        # Add player inputs to main layout
        layout.addLayout(p1_layout)
        layout.addLayout(p2_layout)
        
        # Start button
        button_layout = QHBoxLayout()
        start_button = QPushButton("Start Game")
        start_button.setCursor(Qt.CursorShape.PointingHandCursor)
        start_button.clicked.connect(self.validate_and_accept)
        button_layout.addStretch()
        button_layout.addWidget(start_button)
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        # Set initial focus
        self.p1_input.setFocus()

    def validate_and_accept(self):
        # If names are empty, set default names
        if not self.p1_input.text().strip():
            self.p1_input.setText("Player 1")
        if not self.p2_input.text().strip():
            self.p2_input.setText("Player 2")
        self.accept()

    def get_player_names(self):
        return (
            self.p1_input.text().strip() or "Player 1",
            self.p2_input.text().strip() or "Player 2"
        )

    def keyPressEvent(self, event):
        # Allow Enter key to submit the dialog
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            self.validate_and_accept()
        else:
            super().keyPressEvent(event)