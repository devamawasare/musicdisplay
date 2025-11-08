from PyQt5.QtCore import QObject, QTime, QTimer, QThread, pyqtSignal
from recognizer import Track
from recognizer import recognizer_worker

class Orchestrator(QObject):
    trackUpdated = pyqtSignal(Track)
    status = pyqtSignal(str)

    def __init__(self, poll_ms: int = 20000):
        super().__init__()
        self.last_track: str | None = None
        self.recognizing = False

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
            self.status.emit("Polling Started")

        def stop(self):
            self.timer.stop()
            self.thread.quit()
            self.thread.wait()

        def trigger_recognition(self):
            if self.recognizing:
                return
            self.recognizing = True
            QTimer.singleShot(0, self.worker.try_recognition)

        def on_track_found(self, track: Track):
            self.recognizing = False
            if track.title != self.last_track:
                self.last_track = track.title
                self.trackUpdated.emit(track)

        def on_nothing_found(self):
            self.recognizing = False
            self.status.emit("No Track Found")

        def on_error(self, e: str):
            self.recognizing = False
            self.status.emit(f"Recognition Error - {e}")


