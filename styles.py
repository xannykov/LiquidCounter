MAIN_STYLE = """
QWidget {
    font-family: "Segoe UI";
}

QPushButton {
    border: none;
    outline: none;
}
"""

GLASS_BUTTON_STYLE = """
QPushButton {
    color: rgba(255, 255, 255, 235);
    background-color: rgba(255, 255, 255, 25);
    border: 1px solid rgba(255, 255, 255, 45);
    border-radius: 12px;
    padding: 0px;
    font-size: 9px;
    font-weight: 600;
}

QPushButton:hover {
    background-color: rgba(255, 255, 255, 48);
    border: 1px solid rgba(255, 255, 255, 80);
}

QPushButton:pressed {
    background-color: rgba(255, 255, 255, 70);
}
"""


CLOSE_BUTTON_STYLE = """
QPushButton {
    border-radius: 11px;
}
QPushButton:hover {
    background: rgba(255,80,90,150);
    border: 1px solid rgba(255,120,130,180);
}
"""


ICON_BUTTON_STYLE = """
QPushButton {
    border-radius: 11px;
}
QPushButton:hover {
    background-color: rgba(255, 255, 255, 48);
    border: 1px solid rgba(255, 255, 255, 80);
}
"""


COUNTER_BUTTON_STYLE = """
QPushButton {
    color: white;
    background-color: rgba(255,255,255,25);
    border: 1px solid rgba(255,255,255,55);
    border-radius: 18px;
    font-size: 18px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: rgba(255,255,255,60);
    border: 1px solid rgba(255,255,255,100);
}

QPushButton:pressed {
    background-color: rgba(255,255,255,85);
}
"""


SAVE_BUTTON_SUCCESS_STYLE = """
QPushButton,
QPushButton:hover,
QPushButton:pressed {
    color: white;
    background-color: rgba(120, 220, 160, 90);
    border: 1px solid rgba(120, 255, 180, 160);
    border-radius: 12px;
    padding: 0px;
    font-size: 9px;
    font-weight: 600;
}
"""


HISTORY_WIDGET_STYLE = """
QFrame#historyWidget {
    background: transparent;
    border: none;
}
"""


HISTORY_TITLE_STYLE = """
QLabel {
    color: white;
    background: transparent;
    font-size: 12px;
    font-weight: 600;
    padding: 0;
}
"""


HISTORY_ITEM_STYLE = """
QFrame#historyItem {
    background-color: rgba(255, 255, 255, 22);
    border: 1px solid rgba(255, 255, 255, 32);
    border-radius: 12px;
}
"""


HISTORY_ITEM_DATE_STYLE = """
QLabel {
    color: rgba(255, 255, 255, 195);
    background: transparent;
    font-size: 14px;
}
"""


HISTORY_ITEM_VALUE_STYLE = """
QLabel {
    color: white;
    background: transparent;
    font-size: 16px;
    font-weight: 600;
    padding-right: 5px;
}
"""


HISTORY_EMPTY_STYLE = """
QLabel {
    color: rgba(255, 255, 255, 100);
    background: transparent;
    padding: 12px;
}
"""


HISTORY_SCROLL_STYLE = """
QScrollArea {
    background: transparent;
    border: none;
}
QScrollBar:vertical {
    background: rgba(255, 255, 255, 15);
    width: 6px;
    border-radius: 3px;
    margin: 0;
}
QScrollBar::handle:vertical {
    background: rgba(255, 255, 255, 80);
    border-radius: 3px;
    min-height: 20px;
}
QScrollBar::handle:vertical:hover {
    background: rgba(255, 255, 255, 140);
}
QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0;
}
QScrollBar::add-page:vertical,
QScrollBar::sub-page:vertical {
    background: transparent;
}
"""


DELETE_BUTTON_STYLE = """
QPushButton {
    color: rgba(255, 120, 130, 220);
    background-color: rgba(255, 80, 100, 15);
    border: 1px solid rgba(255, 100, 120, 25);
    border-radius: 10px;
    font-size: 24px;
    padding-bottom: 7px;
    text-align: center;
}
QPushButton:hover {
    color: white;
    background-color: rgba(255, 80, 100, 55);
    border: 1px solid rgba(255, 120, 130, 70);
}
"""


HISTORY_BUTTON_ACTIVE_STYLE = """
QPushButton {
    color: white;
    background-color: rgba(120, 180, 255, 70);
    border: 1px solid rgba(140, 200, 255, 140);
    border-radius: 12px;
    padding: 0 10px;
    font-size: 9px;
    font-weight: 600;
}
QPushButton:hover {
    background-color: rgba(120, 180, 255, 100);
    border: 1px solid rgba(140, 200, 255, 180);
}
"""


PIN_BUTTON_ACTIVE_STYLE = """
QPushButton {
    background-color: rgba(120, 180, 255, 90);
    border: 1px solid rgba(140, 200, 255, 160);
    border-radius: 11px;
}
QPushButton:hover {
    background-color: rgba(120, 180, 255, 130);
    border: 1px solid rgba(140, 200, 255, 200);
}
"""