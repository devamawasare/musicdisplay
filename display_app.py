import sys
from PyQt5.QtWidgets import QApplication
from orchestrator import Orchestrator
from display_window import DisplayWidget
from remote_bridge import RemoteControlBridge
from api_server import start_api_server


def main():
    app = QApplication(sys.argv)
    ui = DisplayWidget()
    ui.show()

    orchestrate = Orchestrator()
    orchestrate.trackUpdated.connect(ui.setTrack)
    orchestrate.noTrack.connect(ui.clearTrack)
    ui.paused.connect(orchestrate.pause_polling)
    ui.resumed.connect(orchestrate.resume_polling)

    bridge = RemoteControlBridge()

    # Qt → Bridge: keep AppState in sync
    orchestrate.trackUpdated.connect(bridge.on_track_updated)
    orchestrate.noTrack.connect(bridge.on_no_track)
    orchestrate.recognizingChanged.connect(bridge.on_recognizing_changed)
    ui.paused.connect(bridge.on_paused)
    ui.resumed.connect(bridge.on_resumed)

    # Bridge → Qt: remote commands
    bridge.pauseRequested.connect(ui.remote_pause)
    bridge.resumeRequested.connect(ui.remote_resume)
    bridge.scanRequested.connect(orchestrate.trigger_recognition)

    start_api_server(bridge, port=5000)
    orchestrate.start()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
