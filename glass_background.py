from PySide6.QtCore import Qt, QTimer
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
        self.theme = "dark"
        self.rainbow_hue = 0

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet("background: transparent; border: none;")

        self.rainbow_timer = QTimer(self)
        self.rainbow_timer.timeout.connect(self._animate_rainbow)

    def set_theme(self, theme_name):
        self.theme = theme_name
        if theme_name == "rusty":
            self.rainbow_timer.start(50)
        else:
            self.rainbow_timer.stop()
        self.update()

    def _animate_rainbow(self):
        self.rainbow_hue = (self.rainbow_hue + 2) % 360
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect().adjusted(1, 1, -1, -1)
        path = QPainterPath()
        path.addRoundedRect(rect, self._radius, self._radius)

        gradient = QLinearGradient(0, 0, self.width(), self.height())
        glow = QLinearGradient(0, 0, self.width(), self.height())

        if self.theme == "rusty":
            c1 = QColor.fromHsv(self.rainbow_hue, 200, 255, 80)
            c2 = QColor.fromHsv((self.rainbow_hue + 120) % 360, 200, 255, 40)
            c3 = QColor.fromHsv((self.rainbow_hue + 240) % 360, 200, 255, 80)
            gradient.setColorAt(0.0, c1)
            gradient.setColorAt(0.5, c2)
            gradient.setColorAt(1.0, c3)
            painter.fillPath(path, gradient)

            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.setPen(QColor.fromHsv(self.rainbow_hue, 150, 255, 150))
            painter.drawPath(path)

        # elif self.theme == "light":
        #     gradient.setColorAt(0.0, QColor(255, 255, 255, 180))
        #     gradient.setColorAt(0.5, QColor(255, 255, 255, 120))
        #     gradient.setColorAt(1.0, QColor(255, 255, 255, 180))
        #     painter.fillPath(path, gradient)
        #
        #     glow.setColorAt(0.0, QColor(118, 222, 197, 100))
        #     glow.setColorAt(0.5, QColor(118, 222, 197, 100))
        #     glow.setColorAt(1.0, QColor(118, 222, 197, 100))
        #     painter.fillPath(path, glow)
        #
        #     painter.setBrush(Qt.BrushStyle.NoBrush)
        #     painter.setPen(QColor(0, 0, 0, 30))
        #     painter.drawPath(path)

        else:
            gradient.setColorAt(0.0, QColor(255, 255, 255, 20))
            gradient.setColorAt(0.5, QColor(255, 255, 255, 5))
            gradient.setColorAt(1.0, QColor(255, 255, 255, 20))
            painter.fillPath(path, gradient)

            glow.setColorAt(0.0, QColor(130, 160, 255, 70))
            glow.setColorAt(0.5, QColor(130, 160, 255, 45))
            glow.setColorAt(1.0, QColor(130, 160, 255, 70))
            painter.fillPath(path, glow)

            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.setPen(QColor(255, 255, 255, 75))
            painter.drawPath(path)