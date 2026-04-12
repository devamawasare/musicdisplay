#!/bin/bash
# One-time setup script for musicdisplay on Raspberry Pi.
# Run once after cloning the repo: bash init.sh

set -e

echo "==> Updating package lists..."
sudo apt-get update -y

echo "==> Installing system dependencies..."
sudo apt-get install -y \
    python3-pip \
    python3-pyqt5 \
    portaudio19-dev \
    libportaudio2

echo "==> Installing Python packages..."
pip3 install --break-system-packages \
    requests \
    sounddevice \
    soundfile \
    flask

echo "==> Done. Run 'bash start.sh' to launch the app."
