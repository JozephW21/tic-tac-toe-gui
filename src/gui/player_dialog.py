from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
                           QLabel, QLineEdit, QPushButton)
from PyQt6.QtCore import Qt

class PlayerNameDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Enter Player Names")
        self.setModal(True)
        
        layout = QVBoxLayout()
        
        # Player 1 input
        p1_layout = QHBoxLayout()
        p1_label = QLabel("Player 1 (X):")
        self.p1_input = QLineEdit()
        self.p1_input.setPlaceholderText("Enter name")
        p1_layout.addWidget(p1_label)
        p1_layout.addWidget(self.p1_input)
        
        # Player 2 input
        p2_layout = QHBoxLayout()
        p2_label = QLabel("Player 2 (O):")
        self.p2_input = QLineEdit()
        self.p2_input.setPlaceholderText("Enter name")
        p2_layout.addWidget(p2_label)
        p2_layout.addWidget(self.p2_input)
        
        # Start button
        start_button = QPushButton("Start Game")
        start_button.clicked.connect(self.accept)
        
        layout.addLayout(p1_layout)
        layout.addLayout(p2_layout)
        layout.addWidget(start_button)
        
        self.setLayout(layout)
    
    def get_player_names(self):
        return (self.p1_input.text() or "Player 1", 
                self.p2_input.text() or "Player 2")
