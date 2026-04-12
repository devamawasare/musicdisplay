import subprocess
import threading
from flask import Flask, jsonify, abort

app = Flask(__name__)
_bridge = None  # set by start_api_server()


def start_api_server(bridge, host="0.0.0.0", port=5000):
    global _bridge
    _bridge = bridge
    t = threading.Thread(
        target=lambda: app.run(host=host, port=port, debug=False, use_reloader=False),
        daemon=True,
    )
    t.start()
    return t


@app.get("/status")
def get_status():
    state = _bridge.get_state_snapshot()
    body = {
        "paused": state.paused,
        "recognizing": state.recognizing,
        "track": None,
    }
    if state.track_title:
        body["track"] = {
            "title": state.track_title,
            "artist": state.track_artist,
            "album": state.track_album,
            "has_art": state.cover_b64 is not None,
        }
    return jsonify(body)


@app.get("/art")
def get_art():
    state = _bridge.get_state_snapshot()
    if state.cover_b64 is None:
        abort(404)
    return jsonify({"image_b64": state.cover_b64})


@app.post("/pause")
def post_pause():
    _bridge.pauseRequested.emit()
    return jsonify({"ok": True})


@app.post("/resume")
def post_resume():
    _bridge.resumeRequested.emit()
    return jsonify({"ok": True})


@app.post("/scan")
def post_scan():
    _bridge.scanRequested.emit()
    return jsonify({"ok": True})


@app.post("/restart")
def post_restart():
    def _do_restart():
        import time
        time.sleep(0.5)  # let the HTTP response go out before systemd kills us
        subprocess.run(["sudo", "systemctl", "restart", "musicdisplay"])
    threading.Thread(target=_do_restart, daemon=True).start()
    return jsonify({"ok": True})
