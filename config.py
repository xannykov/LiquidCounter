from pathlib import Path
import os
import sys

APP_NAME = "LiquidCounter"
APP_VERSION = "1.1.0"

WINDOW_WIDTH = 285
WINDOW_HEIGHT = 95

WINDOW_MARGIN_RIGHT = 32
WINDOW_MARGIN_TOP = 36

IDLE_OPACITY = 0.3
HOVER_OPACITY = 1.0

AUTOSAVE_DELAY_MS = 500

REPEAT_INITIAL_DELAY_MS = 400
REPEAT_INTERVAL_MS = 80


DEFAULT_SETTINGS = {
    "theme": "dark",
    "idle_opacity": IDLE_OPACITY,
    "autostart": False,
    "hotkeys": {
        "increment": "Ctrl+Up",
        "decrement": "Ctrl+Down",
    },
}

LOCAL_APP_DATA = Path(
    os.environ.get(
        "LOCALAPPDATA",
        Path.home() / "AppData" / "Local"
    )
)

APP_DATA_DIR = (LOCAL_APP_DATA/ APP_NAME)
DATA_FILE = (APP_DATA_DIR/ "data.json")

if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys._MEIPASS)
else:
    BASE_DIR = Path(__file__).resolve().parent

ASSETS_DIR = BASE_DIR / "assets"

HISTORY_ICON = ASSETS_DIR / "icon-history.png"
SETTINGS_ICON = ASSETS_DIR / "icon-settings.png"
CLOSE_ICON = ASSETS_DIR / "icon-close.png"
MINUS_ICON = ASSETS_DIR / "icon-minus.png"
PLUS_ICON = ASSETS_DIR / "icon-plus.png"
PIN_ICON = ASSETS_DIR / "icon-pin.png"