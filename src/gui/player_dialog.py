from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
                           QLabel, QLineEdit, QPushButton, QFrame)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class PlayerNameDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Enter Player Names")
        self.setModal(True)
        self.setFixedSize(600, 600)  # Increased height further
        
        # Main layout with proper spacing
        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)  # Remove default spacing
        main_layout.setContentsMargins(40, 40, 40, 40)  # Consistent margins
        
        # Container widget for content
        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                background-color: #2C3E50;
                border-radius: 15px;
            }
        """)
        
        # Content layout
        content_layout = QVBoxLayout(container)
        content_layout.setSpacing(30)  # Explicit spacing between elements
        content_layout.setContentsMargins(30, 30, 30, 30)
        
        # Title
        title = QLabel("Welcome to Tic Tac Toe!")
        title.setStyleSheet("""
            QLabel {
                color: #3498DB;
                font-size: 36px;
                font-weight: bold;
                padding: 0px;
                margin: 0px;
                background: none;
            }
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(title)
        
        # Player 1 section
        p1_container = QFrame()
        p1_container.setStyleSheet("""
            QFrame {
                background: none;
                border: none;
                padding: 0px;
                margin: 0px;
            }
            QLabel {
                color: #ECF0F1;
                font-size: 20px;
                font-weight: bold;
                padding: 0px;
                margin: 0px 0px 10px 0px;
                background: none;
            }
            QLineEdit {
                background-color: #34495E;
                color: #ECF0F1;
                font-size: 18px;
                padding: 15px;
                border: 2px solid #3498DB;
                border-radius: 10px;
                margin: 0px;
            }
            QLineEdit:focus {
                border: 2px solid #2ECC71;
            }
        """)
        p1_layout = QVBoxLayout(p1_container)
        p1_layout.setSpacing(5)
        p1_layout.setContentsMargins(0, 0, 0, 0)
        
        p1_label = QLabel("Player 1 (X):")
        self.p1_input = QLineEdit()
        self.p1_input.setPlaceholderText("Enter name")
        self.p1_input.setMinimumHeight(50)
        p1_layout.addWidget(p1_label)
        p1_layout.addWidget(self.p1_input)
        content_layout.addWidget(p1_container)
        
        # Player 2 section
        p2_container = QFrame()
        p2_container.setStyleSheet(p1_container.styleSheet())  # Same style as p1
        p2_layout = QVBoxLayout(p2_container)
        p2_layout.setSpacing(5)
        p2_layout.setContentsMargins(0, 0, 0, 0)
        
        p2_label = QLabel("Player 2 (O):")
        self.p2_input = QLineEdit()
        self.p2_input.setPlaceholderText("Enter name")
        self.p2_input.setMinimumHeight(50)
        p2_layout.addWidget(p2_label)
        p2_layout.addWidget(self.p2_input)
        content_layout.addWidget(p2_container)
        
        # Start button
        start_button = QPushButton("Start Game")
        start_button.setStyleSheet("""
            QPushButton {
                background-color: #3498DB;
                color: white;
                border: none;
                padding: 15px;
                font-size: 20px;
                font-weight: bold;
                border-radius: 10px;
                min-width: 250px;
                margin: 10px 0px;
            }
            QPushButton:hover {
                background-color: #2980B9;
            }
            QPushButton:pressed {
                background-color: #2574A9;
            }
        """)
        start_button.setCursor(Qt.CursorShape.PointingHandCursor)
        start_button.clicked.connect(self.validate_and_accept)
        
        button_container = QFrame()
        button_container.setStyleSheet("background: none; border: none;")
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.addStretch()
        button_layout.addWidget(start_button)
        button_layout.addStretch()
        content_layout.addWidget(button_container)
        
        # Info section
        info_container = QFrame()
        info_container.setStyleSheet("""
            QFrame {
                background: none;
                border: none;
            }
            QLabel {
                color: #95A5A6;
                font-size: 14px;
                padding: 0px;
                margin: 0px;
            }
        """)
        info_layout = QVBoxLayout(info_container)
        info_layout.setSpacing(5)
        info_layout.setContentsMargins(0, 0, 0, 0)
        
        timestamp_label = QLabel("Created: 2024-11-14 18:48:46 UTC")
        creator_label = QLabel("Created by: JozephW21")
        
        timestamp_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        creator_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        info_layout.addWidget(timestamp_label)
        info_layout.addWidget(creator_label)
        content_layout.addWidget(info_container)
        
        # Add container to main layout
        main_layout.addWidget(container)
        self.setLayout(main_layout)
        
        # Set initial focus
        self.p1_input.setFocus()

    def validate_and_accept(self):
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
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            self.validate_and_accept()
        else:
            super().keyPressEvent(event)