from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from recognizer import Track


class DisplayWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Music Display")
        self.setStyleSheet("background-color: black; color: white;")

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        self.art_label = QLabel()
        self.art_label.setFixedSize(300, 300)
        self.art_label.setAlignment(Qt.AlignCenter)
        self.art_label.setScaledContents(True)

        self.status_label = QLabel("Listening...")
        self.title_label = QLabel("-")
        self.artist_label = QLabel("-")
        self.album_label = QLabel("-")

        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("font-size: 24px; color: #888888;")

        for lbl in (self.title_label, self.artist_label, self.album_label):
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setWordWrap(True)

        self.title_label.setStyleSheet("font-size: 48px; font-weight: bold;")
        self.artist_label.setStyleSheet("font-size: 32px;")
        self.album_label.setStyleSheet("font-size: 32px; color: #aaaaaa;")

        layout.addWidget(self.art_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.title_label)
        layout.addWidget(self.artist_label)
        layout.addWidget(self.album_label)
        layout.addWidget(self.status_label)

        self.setLayout(layout)
        self.showFullScreen()

    def setTrack(self, track: Track):
        self.title_label.setText(track.title or "-")
        self.artist_label.setText(track.artist or "-")
        self.album_label.setText(track.album or "-")
        self.status_label.setText("")

        if track.cover_bytes:
            pixmap = QPixmap()
            pixmap.loadFromData(track.cover_bytes)
            self.art_label.setPixmap(pixmap)
        else:
            self.art_label.clear()

    def setStatus(self, text: str):
        self.status_label.setText(text)
