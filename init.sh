#!/bin/bash
# One-time setup script for musicdisplay on Raspberry Pi.
# Run once after cloning the repo: bash init.sh
# Safe to run multiple times.

set -e

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$HOME/musicdisplay-venv"
SERVICE_FILE="/etc/systemd/system/musicdisplay.service"

echo "==> Updating package lists..."
sudo apt-get update -y

echo "==> Installing system dependencies..."
sudo apt-get install -y \
    python3-pip \
    python3-venv \
    python3-pyqt5 \
    portaudio19-dev \
    libportaudio2

echo "==> Creating virtual environment at $VENV_DIR..."
[ -d "$VENV_DIR" ] || python3 -m venv --system-site-packages "$VENV_DIR"

echo "==> Installing Python packages into venv..."
"$VENV_DIR/bin/pip" install \
    requests \
    sounddevice \
    soundfile \
    flask

echo "==> Installing systemd service..."
sudo tee "$SERVICE_FILE" > /dev/null <<EOF
[Unit]
Description=Music Display
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$REPO_DIR
ExecStartPre=$REPO_DIR/start.sh
ExecStart=$VENV_DIR/bin/python3 display_app.py
Restart=on-failure
RestartSec=5
Environment=DISPLAY=:0

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable musicdisplay.service

echo "==> Granting passwordless restart permission..."
SUDOERS_LINE="$USER ALL=(ALL) NOPASSWD: /bin/systemctl restart musicdisplay"
SUDOERS_FILE="/etc/sudoers.d/musicdisplay"
echo "$SUDOERS_LINE" | sudo tee "$SUDOERS_FILE" > /dev/null
sudo chmod 0440 "$SUDOERS_FILE"

echo "==> Done. Service enabled — it will start automatically on next boot."
echo "    To start now: sudo systemctl start musicdisplay"
