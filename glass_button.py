from pathlib import Path

from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QPushButton

from styles import GLASS_BUTTON_STYLE

class GlassButton(QPushButton):

    def __init__(self,text="",icon_path=None,parent=None):

        super().__init__(text,parent)

        self.setMinimumHeight(36)

        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self.setStyleSheet(GLASS_BUTTON_STYLE)

        if icon_path:

            icon_path = Path(icon_path)

            if icon_path.exists():

                self.setIcon(QIcon(str(icon_path)))

                self.setIconSize(QSize(20,20))