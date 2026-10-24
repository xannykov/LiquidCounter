from PySide6.QtCore import Qt, QSize, QTimer
from PySide6.QtGui import QKeySequence
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QComboBox, QSlider, QCheckBox, QLineEdit,
    QPushButton, QGroupBox
)

from config import APP_VERSION, DEFAULT_SETTINGS, CLOSE_ICON
from glass_background import GlassBackground
from glass_button import GlassButton
from styles import (
    SETTINGS_WINDOW_STYLE, SETTINGS_HEADER_STYLE, SETTINGS_TITLE_STYLE,
    CLOSE_BUTTON_STYLE, SETTINGS_GROUP_STYLE, SETTINGS_LABEL_STYLE,
    SETTINGS_INPUT_STYLE, SETTINGS_CHECKBOX_STYLE, SETTINGS_SLIDER_STYLE,
    GLASS_BUTTON_STYLE, SETTINGS_VERSION_STYLE
)


class HotkeyEdit(QLineEdit):
    def __init__(self, text=""):
        super().__init__(text)
        self.setReadOnly(True)
        self.setPlaceholderText("Нажмите клавиши...")

        # Настройки для мигания
        self._blink_state = False
        self._blink_timer = QTimer(self)
        self._blink_timer.setInterval(400)
        self._blink_timer.timeout.connect(self._toggle_blink)

    def focusInEvent(self, event):
        super().focusInEvent(event)
        self.setPlaceholderText("Нажмите клавиши...")

        self.setProperty("active", True)
        self._blink_timer.start()

        self.style().unpolish(self)
        self.style().polish(self)

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        self._blink_timer.stop()

        self.setProperty("active", False)
        self.setProperty("blink", False)
        self.style().unpolish(self)
        self.style().polish(self)

    def _toggle_blink(self):
        self._blink_state = not self._blink_state
        self.setProperty("blink", self._blink_state)
        self.style().unpolish(self)
        self.style().polish(self)

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key.Key_Backspace, Qt.Key.Key_Delete):
            self.clear()
            return
        if event.key() in (Qt.Key.Key_Control, Qt.Key.Key_Shift, Qt.Key.Key_Alt, Qt.Key.Key_Meta):
            return

        sequence = QKeySequence(event.keyCombination()).toString()
        self.setText(sequence)

        self._blink_timer.stop()
        self.setProperty("active", False)
        self.setProperty("blink", False)
        self.style().unpolish(self)
        self.style().polish(self)
        self.clearFocus()


class SettingsWindow(QWidget):
    def __init__(self, storage, main_window, parent=None):
        super().__init__(parent)
        self.storage = storage
        self.main_window = main_window
        self.drag_position = None

        self.setWindowOpacity(1)

        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground)
        self.setFixedSize(300, 520)

        self.settings = {**DEFAULT_SETTINGS, **self.storage.get_settings()}

        # ----------------------------------------------------
        # GLASS BACKGROUND
        # ----------------------------------------------------
        self.background = GlassBackground(self, radius=23)
        self.background.setGeometry(self.rect())
        current_theme = self.settings.get("theme", "Темная")
        self.background.set_theme(
            "rusty" if current_theme == "Ржачная" else "dark")
            # "rusty" if current_theme == "Ржачная" else ("light" if current_theme == "Светлая" else "dark"))

        self.content = QWidget(self.background)
        self.content.setGeometry(self.background.rect())
        self.content.setObjectName("settingsWindow")
        self.apply_theme_styles(current_theme)

        layout = QVBoxLayout(self.content)
        layout.setContentsMargins(14, 1, 14, 14)
        layout.setSpacing(10)

        # ----------------------------------------------------
        # HEADER
        # ----------------------------------------------------
        header = QWidget()
        header.setObjectName("settingsHeader")
        header.setStyleSheet(SETTINGS_HEADER_STYLE)

        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(5)

        title = QLabel("Настройки")
        title.setStyleSheet(SETTINGS_TITLE_STYLE)
        header_layout.addWidget(title)
        header_layout.addStretch()

        close_button = GlassButton("", CLOSE_ICON)
        close_button.setFixedSize(26, 26)
        close_button.setIconSize(QSize(16, 16))
        close_button.setCursor(Qt.CursorShape.PointingHandCursor)
        close_button.setStyleSheet(CLOSE_BUTTON_STYLE)
        close_button.clicked.connect(self.close)
        header_layout.addWidget(close_button)

        layout.addWidget(header)

        # ----------------------------------------------------
        # HOTKEYS
        # ----------------------------------------------------
        hotkeys_group = QGroupBox("Бинды клавиш")
        hotkeys_group.setStyleSheet(SETTINGS_GROUP_STYLE)
        hotkeys_layout = QVBoxLayout(hotkeys_group)

        self.hotkey_increment = HotkeyEdit(self.settings["hotkeys"].get("increment", ""))
        self.hotkey_increment.setStyleSheet(SETTINGS_INPUT_STYLE)

        self.hotkey_decrement = HotkeyEdit(self.settings["hotkeys"].get("decrement", ""))
        self.hotkey_decrement.setStyleSheet(SETTINGS_INPUT_STYLE)

        label_inc = QLabel("Увеличить:")
        label_inc.setStyleSheet(SETTINGS_LABEL_STYLE)

        label_dec = QLabel("Уменьшить:")
        label_dec.setStyleSheet(SETTINGS_LABEL_STYLE)

        hotkeys_layout.addWidget(label_inc)
        hotkeys_layout.addWidget(self.hotkey_increment)
        hotkeys_layout.addWidget(label_dec)
        hotkeys_layout.addWidget(self.hotkey_decrement)

        layout.addWidget(hotkeys_group)

        # ----------------------------------------------------
        # BEHAVIOR
        # ----------------------------------------------------
        behavior_group = QGroupBox("Поведение")
        behavior_group.setStyleSheet(SETTINGS_GROUP_STYLE)
        behavior_layout = QVBoxLayout(behavior_group)

        self.autostart_checkbox = QCheckBox("Запускать при старте Windows")
        self.autostart_checkbox.setStyleSheet(SETTINGS_CHECKBOX_STYLE)
        self.autostart_checkbox.setChecked(self.settings.get("autostart", False))
        behavior_layout.addWidget(self.autostart_checkbox)

        layout.addWidget(behavior_group)

        # ----------------------------------------------------
        # APPEARANCE
        # ----------------------------------------------------
        appearance_group = QGroupBox("Внешний вид")
        appearance_group.setStyleSheet(SETTINGS_GROUP_STYLE)
        appearance_layout = QVBoxLayout(appearance_group)

        label_theme = QLabel("Тема:")
        label_theme.setStyleSheet(SETTINGS_LABEL_STYLE)
        appearance_layout.addWidget(label_theme)

        self.theme_combo = QComboBox()
        self.theme_combo.setStyleSheet(SETTINGS_INPUT_STYLE)
        self.theme_combo.addItems(["Темная", "Ржачная"])
        # self.theme_combo.addItems(["Темная", "Светлая", "Ржачная"])
        self.theme_combo.setCurrentText(self.settings.get("theme", "Темная"))
        self.theme_combo.currentTextChanged.connect(self._on_theme_preview)
        self.theme_combo.view().window().setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        appearance_layout.addWidget(self.theme_combo)

        label_opacity = QLabel("Прозрачность в покое:")
        label_opacity.setStyleSheet(SETTINGS_LABEL_STYLE)
        appearance_layout.addWidget(label_opacity)

        self.opacity_slider = QSlider(Qt.Orientation.Horizontal)
        self.opacity_slider.setStyleSheet(SETTINGS_SLIDER_STYLE)
        self.opacity_slider.setRange(10, 100)
        self.opacity_slider.setValue(int(self.settings.get("idle_opacity", 0.3) * 100))
        appearance_layout.addWidget(self.opacity_slider)

        layout.addWidget(appearance_group)

        # ----------------------------------------------------
        # VERSION & BUTTONS
        # ----------------------------------------------------
        version_label = QLabel(f"Версия: {APP_VERSION}")
        version_label.setStyleSheet(SETTINGS_VERSION_STYLE)
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(version_label)

        buttons = QHBoxLayout()
        buttons.addStretch()

        cancel_btn = QPushButton("Отмена")
        cancel_btn.setStyleSheet(GLASS_BUTTON_STYLE)
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.clicked.connect(self.close)

        save_btn = QPushButton("Сохранить")
        save_btn.setStyleSheet(GLASS_BUTTON_STYLE)
        save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        save_btn.clicked.connect(self.save_and_close)

        buttons.addWidget(cancel_btn)
        buttons.addWidget(save_btn)
        layout.addLayout(buttons)

    def _on_theme_preview(self, theme_name):
        self.apply_theme_styles(theme_name)
        if theme_name == "Ржачная":
            self.background.set_theme("rusty")
        # elif theme_name == "Светлая":
        #     self.background.set_theme("light")
        else:
            self.background.set_theme("dark")

    def apply_theme_styles(self, theme_name):
        # if theme_name == "Светлая":
        #     from styles import LIGHT_SETTINGS_WINDOW_STYLE, LIGHT_SETTINGS_GROUP_STYLE, LIGHT_SETTINGS_LABEL_STYLE, \
        #         LIGHT_SETTINGS_INPUT_STYLE
        #     self.content.setStyleSheet(LIGHT_SETTINGS_WINDOW_STYLE)
        # else:
        self.content.setStyleSheet(SETTINGS_WINDOW_STYLE)

    def save_and_close(self):
        self.settings["hotkeys"] = {
            "increment": self.hotkey_increment.text(),
            "decrement": self.hotkey_decrement.text(),
        }
        self.settings["autostart"] = self.autostart_checkbox.isChecked()
        self.settings["theme"] = self.theme_combo.currentText()
        self.settings["idle_opacity"] = self.opacity_slider.value() / 100.0

        self.storage.save_settings(self.settings)

        if self.main_window:
            self.main_window.load_settings()

        self.close()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self.drag_position is not None and event.buttons() & Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = None
            event.accept()