"""
UI preview — cycles through all display states with fake data.
No audio hardware or API credentials required.

States cycled:
  clock (idle, amber)    3s
  album art + metadata   4s
  clock (idle, amber)    3s
  paused (green clock)   4s
  ... repeat
"""

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from display_window import DisplayWidget
from track import Track

FAKE_TRACK = Track(
    title="Bohemian Rhapsody",
    artist="Queen",
    album="A Night at the Opera",
    cover_bytes=None,
)

SEQUENCE = [
    ("clock",  3000),
    ("art",    4000),
    ("clock",  3000),
    ("paused", 4000),
]


def main():
    app = QApplication(sys.argv)
    ui = DisplayWidget()

    step = [0]

    def next_step():
        if ui._paused:
            ui._enter_active_state()

        state, delay = SEQUENCE[step[0] % len(SEQUENCE)]
        step[0] += 1

        if state == "clock":
            ui.clearTrack()
        elif state == "art":
            ui.setTrack(FAKE_TRACK)
        elif state == "paused":
            ui._enter_paused_state()

        QTimer.singleShot(delay, next_step)

    next_step()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
