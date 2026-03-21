import datetime

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QPixmap, QColor, QPainter
from recognizer import Track

PHOSPHOR     = "#ffb000"
PHOSPHOR_DIM = "#996800"
FONT_MONO    = "Courier New, Consolas, monospace"


class ScanlineOverlay(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_NoSystemBackground)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(0, 0, 0, 40))
        y = 0
        while y < self.height():
            painter.drawRect(0, y, self.width(), 1)
            y += 3


class DisplayWidget(QWidget):
    paused  = pyqtSignal()
    resumed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Music Display")
        self.setStyleSheet("background-color: black;")

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        self.art_label = QLabel()
        self.art_label.setFixedSize(300, 300)
        self.art_label.setAlignment(Qt.AlignCenter)
        self.art_label.setScaledContents(True)

        self.status_label = QLabel("Listening...")
        self.title_label  = QLabel("-")
        self.artist_label = QLabel("-")
        self.album_label  = QLabel("-")

        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet(
            f"font-size: 24px; color: {PHOSPHOR_DIM}; font-family: {FONT_MONO};"
        )

        for lbl in (self.title_label, self.artist_label, self.album_label):
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setWordWrap(True)

        self.title_label.setStyleSheet(
            f"font-size: 48px; font-weight: bold; color: {PHOSPHOR}; font-family: {FONT_MONO};"
        )
        self.artist_label.setStyleSheet(
            f"font-size: 32px; color: {PHOSPHOR}; font-family: {FONT_MONO};"
        )
        self.album_label.setStyleSheet(
            f"font-size: 32px; color: {PHOSPHOR_DIM}; font-family: {FONT_MONO};"
        )

        for lbl in (self.status_label, self.title_label, self.artist_label, self.album_label):
            lbl.setGraphicsEffect(self._make_glow())

        layout.addWidget(self.art_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.title_label)
        layout.addWidget(self.artist_label)
        layout.addWidget(self.album_label)
        layout.addWidget(self.status_label)

        self.clock_label = QLabel()
        self.clock_label.setAlignment(Qt.AlignCenter)
        self.clock_label.setStyleSheet(
            f"font-size: 96px; font-weight: bold; color: {PHOSPHOR}; font-family: {FONT_MONO};"
        )
        self.clock_label.setGraphicsEffect(self._make_glow())
        self.clock_label.setVisible(False)
        layout.addWidget(self.clock_label)

        self._paused = False
        self._clock_timer = QTimer(self)
        self._clock_timer.setInterval(1000)
        self._clock_timer.timeout.connect(self._tick_clock)

        self._overlay = ScanlineOverlay(self)

        self.setLayout(layout)
        self.showFullScreen()

    def _make_glow(self) -> QGraphicsDropShadowEffect:
        fx = QGraphicsDropShadowEffect(self)
        fx.setBlurRadius(18)
        fx.setColor(QColor(PHOSPHOR))
        fx.setOffset(0, 0)
        return fx

    def resizeEvent(self, event):
        self._overlay.resize(self.size())
        super().resizeEvent(event)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            self._enter_paused_state() if not self._paused else self._enter_active_state()
        else:
            super().keyPressEvent(event)

    def _tick_clock(self):
        self.clock_label.setText(datetime.datetime.now().strftime("%H:%M:%S"))

    def _enter_paused_state(self):
        self._paused = True
        for w in (self.art_label, self.title_label, self.artist_label,
                  self.album_label, self.status_label):
            w.setVisible(False)
        self.clock_label.setVisible(True)
        self._tick_clock()
        self._clock_timer.start()
        self.paused.emit()

    def _enter_active_state(self):
        self._paused = False
        self._clock_timer.stop()
        self.clock_label.setVisible(False)
        for w in (self.art_label, self.title_label, self.artist_label,
                  self.album_label, self.status_label):
            w.setVisible(True)
        self.resumed.emit()

    def setTrack(self, track: Track):
        if self._paused:
            return
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
        if self._paused:
            return
        self.status_label.setText(text)
