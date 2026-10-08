from pathlib import Path
import os

APP_NAME = "LiquidCounter"

WINDOW_WIDTH = 285
WINDOW_HEIGHT = 95

WINDOW_MARGIN_RIGHT = 32
WINDOW_MARGIN_TOP = 36

IDLE_OPACITY = 0.3
HOVER_OPACITY = 1.0


LOCAL_APP_DATA = Path(
    os.environ.get(
        "LOCALAPPDATA",
        Path.home() / "AppData" / "Local"
    )
)

APP_DATA_DIR = (
    LOCAL_APP_DATA
    / APP_NAME
)

DATA_FILE = (
    APP_DATA_DIR
    / "data.json"
)


BASE_DIR = Path(__file__).resolve().parent

ASSETS_DIR = (
    BASE_DIR
    / "assets"
)

HISTORY_ICON = (
    ASSETS_DIR
    / "icon-history.png"
)

SAVE_ICON = (
    ASSETS_DIR
    / "icon-save.png"
)

CLOSE_ICON = (
    ASSETS_DIR
    / "icon-close.png"
)

MINUS_ICON = (
    ASSETS_DIR
    / "icon-minus.png"
)

PLUS_ICON = (
    ASSETS_DIR
    / "icon-plus.png"
)

PIN_ICON = (
    ASSETS_DIR
    / "icon-pin.png"
)