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
    #orchestrate.status.connect(lambda s: print(s))
    orchestrate.start()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()