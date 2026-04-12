from PyQt5.QtCore import QObject, QTimer, QThread, pyqtSignal
from recognizer import Track, recognizer_worker


class Orchestrator(QObject):
    trackUpdated       = pyqtSignal(Track)
    noTrack            = pyqtSignal()
    recognizingChanged = pyqtSignal(bool)

    def __init__(self, poll_ms: int = 20000):
        super().__init__()
        self.last_track: str | None = None
        self.recognizing = False
        self._normal_poll_ms = poll_ms
        self._failure_count = 0

        self.timer = QTimer(self)
        self.timer.setInterval(poll_ms)
        self.timer.timeout.connect(self.trigger_recognition)

        self.thread = QThread(self)
        self.worker = recognizer_worker()
        self.worker.moveToThread(self.thread)
        self.thread.start()

        self.worker.trackFound.connect(self.on_track_found)
        self.worker.nothingFound.connect(self.on_nothing_found)
        self.worker.error.connect(self.on_error)

    def start(self):
        self.timer.start()

    def pause_polling(self):
        self.timer.stop()

    def resume_polling(self):
        self.timer.start()

    def stop(self):
        self.timer.stop()
        self.thread.quit()
        self.thread.wait()

    def trigger_recognition(self):
        if self.recognizing:
            return
        self.recognizing = True
        self.recognizingChanged.emit(True)
        QTimer.singleShot(0, self.worker.try_recognition)

    def on_track_found(self, track: Track):
        self.recognizing = False
        self.recognizingChanged.emit(False)
        self._failure_count = 0
        if self.timer.interval() != self._normal_poll_ms:
            self.timer.setInterval(self._normal_poll_ms)
        if track.title != self.last_track:
            self.last_track = track.title
            self.trackUpdated.emit(track)

    def _handle_failure(self):
        self.recognizing = False
        self.recognizingChanged.emit(False)
        self._failure_count += 1
        self.noTrack.emit()
        if self._failure_count >= 3 and self.timer.interval() == self._normal_poll_ms:
            self.timer.setInterval(self._normal_poll_ms * 3)

    def on_nothing_found(self):
        self._handle_failure()

    def on_error(self, e: str):
        self._handle_failure()
