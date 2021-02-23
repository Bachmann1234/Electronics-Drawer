#!/bin/bash
source /home/pi/eink_art_display/.env
python3 /home/pi/Pimoroni/inky/examples/7color/clear.py
# Yes, do it twice. Once does not seem to clear it well
python3 /home/pi/Pimoroni/inky/examples/7color/clear.py
python3 /home/pi/eink_art_display/find_art.py
