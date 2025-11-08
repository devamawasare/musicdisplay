from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from recognizer import Track

class DisplayWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Music Display")
        layout = QVBoxLayout(self)
        self.title_label = QLabel("-")
        self.album_label = QLabel("-")
        for lbl in (self.title_label, self.album_label):
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setStyleSheet("font-size: 28px;")
        layout.addWidget(self.title_label)
        layout.addWidget(self.artist_label)
        self.setLayout(layout)
        self.resize(600, 200)

    def setTrack(self, track: Track):
        self.title_label.setText(track.title or "-")
        self.album_label.setText(track.album or "-")