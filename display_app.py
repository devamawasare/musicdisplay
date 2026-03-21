import sys
from PyQt5.QtWidgets import QApplication
from orchestrator import Orchestrator
from display_window import DisplayWidget


def main():
    app = QApplication(sys.argv)
    ui = DisplayWidget()
    ui.show()

    orchestrate = Orchestrator()
    orchestrate.trackUpdated.connect(ui.setTrack)
    orchestrate.noTrack.connect(ui.clearTrack)
    ui.paused.connect(orchestrate.pause_polling)
    ui.resumed.connect(orchestrate.resume_polling)
    orchestrate.start()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
