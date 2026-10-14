from PySide6.QtCore import (
    Qt,
    QTimer,
    QPropertyAnimation,
    QEasingCurve,
    QSize,
)

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QApplication
)

from config import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    WINDOW_MARGIN_RIGHT,
    WINDOW_MARGIN_TOP,
    IDLE_OPACITY,
    HOVER_OPACITY,
    HISTORY_ICON,
    SETTINGS_ICON,
    CLOSE_ICON,
    MINUS_ICON,
    PLUS_ICON,
    PIN_ICON, AUTOSAVE_DELAY_MS
)

from glass_button import GlassButton, RepeatButton
from history_widget import HistoryWidget
from settings_window import SettingsWindow
from glass_background import GlassBackground

from styles import (
    MAIN_STYLE,
    GLASS_BUTTON_STYLE,
    HISTORY_BUTTON_ACTIVE_STYLE,
    PIN_BUTTON_ACTIVE_STYLE,
    CLOSE_BUTTON_STYLE,
    ICON_BUTTON_STYLE,
)

from windows_effects import (
    configure_window,
    enable_blur,
)

class MainWindow(QWidget):

    def __init__(self, storage):

        super().__init__()

        self.storage = storage

        self.counter = storage.get_today_value()

        self.history_open = False

        self.is_pinned = self.storage.get_pinned()
        self.drag_position = None

        self._autosave_timer = QTimer(self)
        self._autosave_timer.setSingleShot(True)
        self._autosave_timer.timeout.connect(self._do_autosave)

        # ----------------------------------------------------
        # OPACITY ANIMATION
        # ----------------------------------------------------

        self.opacity_animation = QPropertyAnimation(self,b"windowOpacity")
        self.opacity_animation.setDuration(180)
        self.opacity_animation.setEasingCurve(QEasingCurve.Type.OutCubic)

        # ----------------------------------------------------
        # WINDOW
        # ----------------------------------------------------

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.Tool
            | Qt.WindowType.WindowStaysOnTopHint
        )

        self.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground
        )

        self.setAttribute(
            Qt.WidgetAttribute.WA_NoSystemBackground
        )

        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)

        self.setStyleSheet(MAIN_STYLE)

        # ----------------------------------------------------
        # POSITION
        # ----------------------------------------------------

        self.position_top_right()

        # ----------------------------------------------------
        # GLASS
        # ----------------------------------------------------

        self.background = GlassBackground(self)
        self.background.setGeometry(self.rect())

        # ----------------------------------------------------
        # CONTENT
        # ----------------------------------------------------

        self.content = QWidget(self.background)
        self.content.setGeometry(self.background.rect())

        self.build_ui()

        # ----------------------------------------------------
        # INITIAL OPACITY
        # ----------------------------------------------------

        self.setWindowOpacity(IDLE_OPACITY)

    # ========================================================
    # POSITION
    # ========================================================

    def position_window(self):
        saved = self.storage.get_window_position()
        if saved:
            self.move(saved[0], saved[1])
        else:
            self.position_top_right()

    def position_top_right(self):
        screen = self.screen()
        if not screen:
            return
        geometry = screen.availableGeometry()
        x = geometry.right() - self.width() - WINDOW_MARGIN_RIGHT
        y = geometry.top() + WINDOW_MARGIN_TOP
        self.move(x, y)

    # ========================================================
    # UI
    # ========================================================

    def build_ui(self):

        self.main_layout = QVBoxLayout(self.content)
        self.main_layout.setContentsMargins(13, 0, 13, 0)
        self.main_layout.setSpacing(0)

        # ====================================================
        # HEADER
        # ====================================================

        header = QHBoxLayout()
        header.setSpacing(5)

        title = QLabel("LiquidCounter")
        title.setStyleSheet("""
            QLabel {
                color: white;
                background: transparent;
                font-size: 14px;
                font-weight: 600;
            }
        """)

        header.addWidget(title)
        header.addStretch()

        # PIN
        self.pin_button = GlassButton("", PIN_ICON)
        self.pin_button.setFixedSize(26, 26)
        self.pin_button.setIconSize(QSize(16, 16))
        self.pin_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.pin_button.clicked.connect(self.toggle_pin)
        header.addWidget(self.pin_button)

        # CLOSE
        self.close_button = GlassButton("", CLOSE_ICON)
        self.close_button.setFixedSize(26, 26)
        self.close_button.setIconSize(QSize(16, 16))
        self.close_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.close_button.setStyleSheet(CLOSE_BUTTON_STYLE)
        self.close_button.clicked.connect(self.close)
        header.addWidget(self.close_button)

        self.main_layout.addLayout(header)

        self.update_pin_style()

        # ====================================================
        # COUNTER ROW
        # ====================================================

        row = QHBoxLayout()
        row.setSpacing(6)

        self.minus_button = RepeatButton("", MINUS_ICON)
        self.minus_button.setFixedSize(36, 36)

        self.plus_button = RepeatButton("", PLUS_ICON)
        self.plus_button.setFixedSize(36, 36)

        for button in (self.minus_button, self.plus_button):
            button.setFixedSize(36, 36)
            button.setCursor(
                Qt.CursorShape.PointingHandCursor
            )

        self.minus_button.clicked.connect(self.decrease)
        self.plus_button.clicked.connect(self.increase)

        self.counter_label = QLabel(str(self.counter))
        self.counter_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )
        self.counter_label.setStyleSheet("""
            QLabel {
                color: white;
                background: transparent;
                font-size: 30px;
                font-weight: 600;
            }
        """)

        self.history_button = GlassButton("", HISTORY_ICON)
        self.history_button.setFixedSize(36, 36)
        self.history_button.clicked.connect(self.toggle_history)

        self.settings_button = GlassButton("", SETTINGS_ICON)
        self.settings_button.setFixedSize(36, 36)
        self.settings_button.clicked.connect(self.open_settings)

        row.addWidget(self.minus_button)
        row.addWidget(self.counter_label, 1)
        row.addWidget(self.plus_button)
        row.addSpacing(2)
        row.addWidget(self.history_button)
        row.addWidget(self.settings_button)

        self.main_layout.addSpacing(0)
        self.main_layout.addLayout(row)

        # ====================================================
        # HISTORY PANEL
        # ====================================================

        self.history_widget = HistoryWidget(self.storage)
        self.history_widget.setParent(self.content)
        self.history_widget.hide()

    # ========================================================
    # COUNTER
    # ========================================================

    def increase(self):
        self.counter += 1
        self.update_counter()
        self._schedule_autosave()

    def decrease(self):
        if self.counter <= 0:
            return
        self.counter -= 1
        self.update_counter()
        self._schedule_autosave()

    def update_counter(self):
        self.counter_label.setText(str(self.counter))

    def _schedule_autosave(self):
        self._autosave_timer.start(AUTOSAVE_DELAY_MS)

    def _do_autosave(self):
        try:
            self.storage.save_today(self.counter)
            if self.history_open:
                self.history_widget.reload()
        except Exception as error:
            print("Autosave error:", error)


    # ========================================================
    # SETTINGS
    # ========================================================

    def open_settings(self):
        self.settings_window = SettingsWindow(self.storage)
        self.settings_window.show()
        self.settings_window.raise_()
        self.settings_window.activateWindow()

    # ========================================================
    # HISTORY
    # ========================================================

    def toggle_history(self):

        if self.history_open:
            self.close_history()
        else:
            self.open_history()

    def open_history(self):

        self.history_open = True

        self.history_widget.reload()

        if self.main_layout.indexOf(self.history_widget) == -1:
            self.main_layout.addWidget(self.history_widget)

        self.history_widget.show()

        target_height = self.history_widget.sizeHint().height()
        self.history_widget.setMaximumHeight(target_height)

        self.history_button.setStyleSheet(
            HISTORY_BUTTON_ACTIVE_STYLE
        )

        self.resize(
            WINDOW_WIDTH,
            WINDOW_HEIGHT + target_height
        )

    def close_history(self):

        self.history_open = False

        self.history_button.setStyleSheet(
            GLASS_BUTTON_STYLE
        )

        self.history_widget.hide()
        self.main_layout.removeWidget(self.history_widget)

        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)

    # ========================================================
    # HOVER OPACITY
    # ========================================================

    def enterEvent(self, event):
        self.animate_opacity(HOVER_OPACITY)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.animate_opacity(IDLE_OPACITY)
        super().leaveEvent(event)

    def animate_opacity(self, target):
        self.opacity_animation.stop()

        self.opacity_animation.setStartValue(
            self.windowOpacity()
        )
        self.opacity_animation.setEndValue(target)
        self.opacity_animation.start()

    def closeEvent(self, event):
        self._autosave_timer.stop()
        try:
            self.storage.save_today(self.counter)
        except Exception as error:
            print("Save on close error:", error)

        self.storage.save_window_position(self.x(), self.y())
        QApplication.quit()
        super().closeEvent(event)

    # ========================================================
    # RESIZE
    # ========================================================

    def resizeEvent(self, event):
        self.background.setGeometry(self.rect())
        self.content.setGeometry(self.background.rect())
        super().resizeEvent(event)

    # ========================================================
    # SHOW
    # ========================================================

    def showEvent(self, event):
        super().showEvent(event)

        if not getattr(self, "_positioned", False):
            self.position_window()
            self._positioned = True

        try:
            configure_window(int(self.winId()))
            enable_blur(int(self.winId()))
        except Exception as error:
            print("Windows effects error:", error)

    # ========================================================
    # PIN
    # ========================================================

    def toggle_pin(self):
        self.is_pinned = not self.is_pinned
        self.storage.save_pinned(self.is_pinned)
        self.update_pin_style()

    def update_pin_style(self):
        if self.is_pinned:
            self.pin_button.setStyleSheet(PIN_BUTTON_ACTIVE_STYLE)
        else:
            self.pin_button.setStyleSheet(ICON_BUTTON_STYLE)

    # ========================================================
    # MOUSE DRAG
    # ========================================================

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:

            child = self.childAt(event.position().toPoint())
            if isinstance(child, QPushButton):
                return

            if self.is_pinned:
                return

            self.drag_position = (
                    event.globalPosition().toPoint()
                    - self.frameGeometry().topLeft()
            )
            event.accept()

    def mouseMoveEvent(self, event):
        if (
                self.drag_position is not None
                and event.buttons() & Qt.MouseButton.LeftButton
        ):
            self.move(
                event.globalPosition().toPoint()
                - self.drag_position
            )
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if self.drag_position is not None:
                self.storage.save_window_position(
                    self.x(), self.y()
                )
            self.drag_position = None
            event.accept()