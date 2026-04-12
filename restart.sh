#!/bin/bash
# Restart the music display service — pulls latest changes and relaunches.
# Usage: bash restart.sh

sudo systemctl restart musicdisplay
echo "Restarted. Status:"
sudo systemctl status musicdisplay --no-pager -l
