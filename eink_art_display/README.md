# Eink Art Display

Shows random art from Reddit (r/art) and DeviantArt (Daily Deviations) on a Pimoroni Inky display. Runs on a Pi Zero W with either an Inky wHAT or an Inky Impression 7 colour; `find_art.py` works out which panel it is on.

Each image shown is saved to `~/art_history` (the last 50, set with `ART_HISTORY_KEEP`), and `~/art_history/history.log` keeps a line with a link for every image ever shown. `index.html` there is a gallery of the saved images; the `@reboot` line in `example_crontab` serves it on `http://<pi>:8080`.

## Setup

On Raspberry Pi OS Lite (trixie):

```
sudo raspi-config nonint do_spi 0
sudo raspi-config nonint do_i2c 0
# inky drives the chip select pin itself, keep the kernel off it
echo dtoverlay=spi0-0cs | sudo tee -a /boot/firmware/config.txt
sudo apt install git python3-numpy python3-pil
sudo reboot

git clone https://github.com/Bachmann1234/Electronics-Drawer.git ~/Electronics-Drawer
cd ~/Electronics-Drawer/eink_art_display
# system site packages so numpy and pillow come from apt, building them on a pi zero takes forever
python3 -m venv --system-site-packages venv
venv/bin/pip install -r requirements.txt
```

Then create `.env` next to `go.sh` with the API credentials:

```
export DEVIANT_ART_CLIENT_ID=...
export DEVIANT_ART_CLIENT_SECRET=...
export REDDIT_CLIENT_ID=...
export REDDIT_CLIENT_SECRET=...
export REDDIT_USER_AGENT=...
```

Try it with `./go.sh` (output goes to `~/art.log`), then add the lines from `example_crontab` with `crontab -e`.
