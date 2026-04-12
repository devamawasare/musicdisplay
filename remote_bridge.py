import threading
import base64
from copy import copy
from dataclasses import dataclass
from typing import Optional

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

from track import Track


@dataclass
class AppState:
    """Plain Python dataclass written only from the Qt main thread."""
    paused: bool = False
    recognizing: bool = False
    track_title: Optional[str] = None
    track_artist: Optional[str] = None
    track_album: Optional[str] = None
    cover_b64: Optional[str] = None  # base64-encoded image bytes


class RemoteControlBridge(QObject):
    """
    Lives on the Qt main thread.
    Flask reads _state via lock; emits signals to mutate Qt state.
    """

    # Emitted from the Flask thread — Qt delivers them as QueuedConnection
    pauseRequested = pyqtSignal()
    resumeRequested = pyqtSignal()
    scanRequested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._lock = threading.Lock()
        self._state = AppState()

    # ── Slots called from Qt main thread only ────────────────────────────

    @pyqtSlot()
    def on_paused(self):
        with self._lock:
            self._state.paused = True

    @pyqtSlot()
    def on_resumed(self):
        with self._lock:
            self._state.paused = False

    @pyqtSlot(object)
    def on_track_updated(self, track: Track):
        b64 = None
        if track.cover_bytes:
            b64 = base64.b64encode(track.cover_bytes).decode("ascii")
        with self._lock:
            self._state.track_title = track.title
            self._state.track_artist = track.artist
            self._state.track_album = track.album
            self._state.cover_b64 = b64

    @pyqtSlot()
    def on_no_track(self):
        with self._lock:
            self._state.track_title = None
            self._state.track_artist = None
            self._state.track_album = None
            self._state.cover_b64 = None

    @pyqtSlot(bool)
    def on_recognizing_changed(self, recognizing: bool):
        with self._lock:
            self._state.recognizing = recognizing

    # ── Called from Flask thread (read-only snapshot) ────────────────────

    def get_state_snapshot(self) -> AppState:
        with self._lock:
            return copy(self._state)
