from pathlib import Path

from PySide6.QtCore import Qt, QSize, QTimer
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QPushButton

from styles import GLASS_BUTTON_STYLE
from config import REPEAT_INITIAL_DELAY_MS, REPEAT_INTERVAL_MS


class GlassButton(QPushButton):

    def __init__(self, text="", icon_path=None, parent=None):
        super().__init__(text, parent)

        self.setMinimumHeight(36)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet(GLASS_BUTTON_STYLE)

        if icon_path:
            icon_path = Path(icon_path)
            if icon_path.exists():
                self.setIcon(QIcon(str(icon_path)))
                self.setIconSize(QSize(20, 20))


class RepeatButton(GlassButton):

    def __init__(self, text="", icon_path=None, parent=None):
        super().__init__(text, icon_path, parent)

        self._initial_timer = QTimer(self)
        self._initial_timer.setSingleShot(True)
        self._initial_timer.timeout.connect(self._start_repeat)

        self._repeat_timer = QTimer(self)
        self._repeat_timer.timeout.connect(self.click)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            super().mousePressEvent(event)
            self._initial_timer.start(REPEAT_INITIAL_DELAY_MS)
        else:
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self._initial_timer.stop()
        self._repeat_timer.stop()
        super().mouseReleaseEvent(event)

    def _start_repeat(self):
        self._repeat_timer.start(REPEAT_INTERVAL_MS)