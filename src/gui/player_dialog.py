from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
                           QLabel, QLineEdit, QPushButton)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPalette, QColor

class PlayerNameDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Enter Player Names")
        self.setModal(True)
        self.setFixedSize(600, 400)  # Even larger window size
        
        # Set background color
        self.setStyleSheet("""
            QDialog {
                background-color: #2C3E50;
            }
            QLabel {
                color: #ECF0F1;
                font-size: 18px;  /* Larger font size */
                font-weight: bold;
                margin: 8px;
            }
            QLineEdit {
                padding: 15px;  /* More padding */
                font-size: 18px;  /* Larger font size */
                border: 2px solid #3498DB;
                border-radius: 10px;
                background-color: #34495E;
                color: #ECF0F1;
                margin: 10px;
                min-height: 30px;  /* Taller input fields */
            }
            QLineEdit:focus {
                border: 2px solid #2ECC71;
            }
            QPushButton {
                background-color: #3498DB;
                color: white;
                border: none;
                padding: 20px 40px;  /* More padding */
                font-size: 20px;  /* Larger font size */
                font-weight: bold;
                border-radius: 10px;
                min-width: 250px;  /* Wider button */
                margin: 25px;
            }
            QPushButton:hover {
                background-color: #2980B9;
            }
            QPushButton:pressed {
                background-color: #2574A9;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(25)  # More spacing between elements
        layout.setContentsMargins(50, 40, 50, 40)  # Larger margins
        
        # Title with more prominent styling
        title = QLabel("Welcome to Tic Tac Toe!")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            font-size: 36px;  /* Even larger title */
            color: #3498DB;
            margin-bottom: 30px;
            font-weight: bold;
            padding: 10px;
        """)
        layout.addWidget(title)
        
        # Spacer after title
        layout.addSpacing(20)
        
        # Player 1 input
        p1_layout = QVBoxLayout()
        p1_layout.setSpacing(12)  # More spacing
        p1_label = QLabel("Player 1 (X):")
        self.p1_input = QLineEdit()
        self.p1_input.setPlaceholderText("Enter name")
        self.p1_input.setMinimumHeight(50)  # Taller input field
        p1_layout.addWidget(p1_label)
        p1_layout.addWidget(self.p1_input)
        
        # Space between player inputs
        layout.addLayout(p1_layout)
        layout.addSpacing(20)
        
        # Player 2 input
        p2_layout = QVBoxLayout()
        p2_layout.setSpacing(12)  # More spacing
        p2_label = QLabel("Player 2 (O):")
        self.p2_input = QLineEdit()
        self.p2_input.setPlaceholderText("Enter name")
        self.p2_input.setMinimumHeight(50)  # Taller input field
        p2_layout.addWidget(p2_label)
        p2_layout.addWidget(self.p2_input)
        layout.addLayout(p2_layout)
        
        # Space before button
        layout.addSpacing(20)
        
        # Start button
        button_layout = QHBoxLayout()
        start_button = QPushButton("Start Game")
        start_button.setCursor(Qt.CursorShape.PointingHandCursor)
        start_button.clicked.connect(self.validate_and_accept)
        button_layout.addStretch()
        button_layout.addWidget(start_button)
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        # Space before info
        layout.addSpacing(20)
        
        # Info section with updated styling
        info_layout = QVBoxLayout()
        timestamp_label = QLabel("Created: 2024-11-14 18:43:24 UTC")
        creator_label = QLabel("Created by: JozephW21")
        
        info_style = """
            color: #95A5A6;
            font-size: 14px;  /* Slightly larger info text */
            margin-top: 8px;
            padding: 5px;
        """
        timestamp_label.setStyleSheet(info_style)
        creator_label.setStyleSheet(info_style)
        
        timestamp_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        creator_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        info_layout.addWidget(timestamp_label)
        info_layout.addWidget(creator_label)
        layout.addLayout(info_layout)
        
        # Add final spacing
        layout.addSpacing(10)
        
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