# MusicDisplay

A Raspberry Pi music recognition display with an Android remote control app.

The Pi listens to ambient audio, identifies the currently playing song via [ACRCloud](https://www.acrcloud.com/), and shows the album art, track info, and a live clock on a full-screen display. An Android app lets you control it over your local network.

---

## Features

- **Music recognition** — records a short audio clip every ~20 seconds and identifies the track
- **Full-screen display** — album art, title, artist, album, clock, date, and weather
- **Idle mode** — shows a clock and weather when nothing is playing
- **Starfield background** — subtle animated star warp effect
- **Android remote** — pause, resume, force scan, and restart the app from your phone
- **Auto-update on boot** — `git pull` runs before startup so the Pi always runs the latest code

---

## Architecture

```
Raspberry Pi
├── display_app.py       Qt app (main thread)
├── display_window.py    Full-screen PyQt5 UI
├── orchestrator.py      Recognition polling loop
├── recognizer.py        ACRCloud API worker thread
├── api_server.py        Flask REST API (port 5000)
├── remote_bridge.py     Thread-safe Qt ↔ Flask bridge
├── weather_service.py   Open-Meteo weather polling
└── animation_layer.py   Starfield background animation

Android App (android-remote/)
└── Kotlin/Jetpack app — polls /status, sends commands
```

---

## Pi Setup

### Prerequisites

- Raspberry Pi with a desktop environment (X11/Wayland)
- Microphone connected (USB or 3.5mm)
- ACRCloud account with an audio recognition project

### First-time setup

```bash
git clone <this-repo> ~/repositories/musicdisplay
cd ~/repositories/musicdisplay
bash init.sh
```

`init.sh` will:
1. Install system packages (`python3-venv`, `python3-pyqt5`, `portaudio19-dev`, etc.)
2. Create a Python venv at `~/musicdisplay-venv`
3. Install Python dependencies into the venv
4. Register and enable the `musicdisplay` systemd service
5. Grant passwordless `sudo systemctl restart musicdisplay` permission

The app will start automatically on every boot. Safe to re-run.

### Configuration

Edit `config.ini` before running:

```ini
[weather]
latitude = 51.5
longitude = -0.1
units = celsius          ; or fahrenheit
weather_refresh_minutes = 15
```

Add your ACRCloud credentials to `acrcloud_api.py`:

```python
ACCESS_KEY = "your_access_key"
SECRET_KEY = "your_secret_key"
HOST       = "your_host.acrcloud.com"
```

### Manual control

```bash
# Start / stop / restart
sudo systemctl start musicdisplay
sudo systemctl stop musicdisplay
sudo systemctl restart musicdisplay

# View live logs
journalctl -u musicdisplay -f
```

---

## REST API

The Pi exposes a REST API on port `5000`.

| Method | Endpoint   | Description                        |
|--------|------------|------------------------------------|
| GET    | `/status`  | Current state (paused, track info) |
| GET    | `/art`     | Album art as base64 image          |
| POST   | `/pause`   | Pause recognition                  |
| POST   | `/resume`  | Resume recognition                 |
| POST   | `/scan`    | Trigger an immediate scan          |
| POST   | `/restart` | Restart the systemd service        |

### Example

```bash
curl http://192.168.1.91:5000/status
```

```json
{
  "paused": false,
  "recognizing": true,
  "track": {
    "title": "Bohemian Rhapsody",
    "artist": "Queen",
    "album": "A Night at the Opera",
    "has_art": true
  }
}
```

---

## Android App

Open `android-remote/` in Android Studio and build. On first launch, go to **Settings** and enter your Pi's IP address (default: `192.168.1.91`).

The app polls `/status` every 3 seconds and shows the current track. Buttons let you pause/resume, force a scan, or restart the Pi app.

**Minimum SDK:** Android 8.0 (API 26)

---

## Dependencies

| Dependency | Purpose |
|---|---|
| PyQt5 | Full-screen display UI |
| Flask | REST API server |
| sounddevice / soundfile | Audio recording |
| requests | HTTP calls (ACRCloud, Spotify, weather) |
| ACRCloud | Music fingerprint recognition |
| Open-Meteo | Free weather API (no key required) |
| Retrofit + OkHttp | Android HTTP client |
| Jetpack DataStore | Android settings persistence |
