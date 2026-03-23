import math
import random

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QColor

# Reduce if Pi CPU usage is too high
STAR_COUNT = 80
SPEED = 1.5  # pixels per frame at max depth — increase for faster warp


class AnimationLayer(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_NoSystemBackground)
        self.setStyleSheet("background: transparent;")

        self._stars: list[list] = []
        self._initialized = False

        self._timer = QTimer(self)
        self._timer.setInterval(50)  # 20 fps — smooth enough, easy on Pi
        self._timer.timeout.connect(self._tick)
        self._timer.start()

    def _make_star(self, w: int, h: int) -> list:
        # z: depth 1.0 (far) → 0.0 (close), starts randomly distributed
        z = random.random()
        return [
            random.uniform(-1.0, 1.0),  # nx: normalised x origin (-1..1)
            random.uniform(-1.0, 1.0),  # ny: normalised y origin (-1..1)
            z,                           # z: depth
        ]

    def _init_stars(self, w: int, h: int) -> None:
        self._stars = [self._make_star(w, h) for _ in range(STAR_COUNT)]
        self._initialized = True

    def _tick(self) -> None:
        w, h = self.width(), self.height()
        if w == 0 or h == 0:
            return
        if not self._initialized:
            self._init_stars(w, h)
            return

        cx, cy = w / 2, h / 2

        for star in self._stars:
            star[2] -= SPEED / 400.0  # move toward viewer
            if star[2] <= 0:
                # Reset to a new random far-away star
                star[0] = random.uniform(-1.0, 1.0)
                star[1] = random.uniform(-1.0, 1.0)
                star[2] = 1.0

            # Check if star has left the screen
            scale = 1.0 - star[2]
            if scale <= 0:
                continue
            sx = cx + star[0] * cx * scale * 2
            sy = cy + star[1] * cy * scale * 2
            if sx < 0 or sx > w or sy < 0 or sy > h:
                star[0] = random.uniform(-1.0, 1.0)
                star[1] = random.uniform(-1.0, 1.0)
                star[2] = 1.0

        self.update()

    def paintEvent(self, event) -> None:
        if not self._initialized:
            return

        w, h = self.width(), self.height()
        cx, cy = w / 2, h / 2

        painter = QPainter(self)
        painter.setPen(Qt.NoPen)

        for star in self._stars:
            scale = 1.0 - star[2]  # 0 when far, 1 when close
            if scale <= 0:
                continue

            sx = cx + star[0] * cx * scale * 2
            sy = cy + star[1] * cy * scale * 2

            # Brightness and size grow as star approaches
            alpha = int(scale * 220)
            size = max(1, int(scale * 10))

            painter.setBrush(QColor(255, 176, 0, alpha))
            painter.drawEllipse(int(sx - size // 2), int(sy - size // 2), size, size)

    def resizeEvent(self, event) -> None:
        w, h = self.width(), self.height()
        if w > 0 and h > 0:
            self._init_stars(w, h)
        super().resizeEvent(event)
