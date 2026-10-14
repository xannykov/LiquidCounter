from PySide6.QtCore import Qt
from PySide6.QtGui import (
    QPainter,
    QPainterPath,
    QColor,
    QLinearGradient,
)
from PySide6.QtWidgets import QFrame


class GlassBackground(QFrame):

    def __init__(self, parent=None, radius=23):
        super().__init__(parent)

        self._radius = radius

        self.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground
        )

        self.setStyleSheet(
            "background: transparent;"
            "border: none;"
        )

    def paintEvent(self, event):

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect().adjusted(1, 1, -1, -1)

        path = QPainterPath()
        path.addRoundedRect(rect, self._radius, self._radius)

        gradient = QLinearGradient(
            0, 0,
            self.width(), self.height()
        )
        gradient.setColorAt(0.0, QColor(255, 255, 255, 20))
        gradient.setColorAt(0.5, QColor(255, 255, 255, 5))
        gradient.setColorAt(1.0, QColor(255, 255, 255, 20))
        painter.fillPath(path, gradient)

        glow = QLinearGradient(
            0, 0,
            self.width(), self.height()
        )
        glow.setColorAt(0.0, QColor(130, 160, 255, 70))
        glow.setColorAt(0.5, QColor(130, 160, 255, 45))
        glow.setColorAt(0.1, QColor(130, 160, 255, 70))
        painter.fillPath(path, glow)

        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(QColor(255, 255, 255, 75))
        painter.drawPath(path)