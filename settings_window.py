from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QSlider,
    QCheckBox,
    QLineEdit,
    QPushButton,
    QGroupBox,
)

from config import (
    APP_VERSION,
    DEFAULT_SETTINGS,
    CLOSE_ICON
)

from glass_background import GlassBackground
from glass_button import GlassButton

from styles import (
    SETTINGS_WINDOW_STYLE,
    SETTINGS_HEADER_STYLE,
    SETTINGS_TITLE_STYLE,
    CLOSE_BUTTON_STYLE,
    SETTINGS_GROUP_STYLE,
    SETTINGS_LABEL_STYLE,
    SETTINGS_INPUT_STYLE,
    SETTINGS_CHECKBOX_STYLE,
    SETTINGS_SLIDER_STYLE,
    GLASS_BUTTON_STYLE,
    SETTINGS_VERSION_STYLE,
)


class SettingsWindow(QWidget):

    def __init__(self, storage, parent=None):
        super().__init__(parent)

        self.storage = storage
        self.drag_position = None

        self.setWindowFlags(
            Qt.WindowType.Window
            | Qt.WindowType.FramelessWindowHint
        )
        self.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground
        )
        self.setAttribute(
            Qt.WidgetAttribute.WA_NoSystemBackground
        )
        self.setFixedSize(285, 500)

        self.settings = {**DEFAULT_SETTINGS, **self.storage.get_settings()}

        # ----------------------------------------------------
        # GLASS BACKGROUND
        # ----------------------------------------------------

        self.background = GlassBackground(self, radius=23)
        self.background.setGeometry(self.rect())

        self.content = QWidget(self.background)
        self.content.setGeometry(self.background.rect())
        self.content.setObjectName("settingsWindow")
        self.content.setStyleSheet(SETTINGS_WINDOW_STYLE)

        layout = QVBoxLayout(self.content)
        layout.setContentsMargins(14, 10, 14, 14)
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

        self.hotkey_increment = QLineEdit(
            self.settings["hotkeys"].get("increment", "")
        )
        self.hotkey_increment.setStyleSheet(SETTINGS_INPUT_STYLE)

        self.hotkey_decrement = QLineEdit(
            self.settings["hotkeys"].get("decrement", "")
        )
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
        self.theme_combo.addItems(["Темная", "Светлая", "Ржачная"])
        self.theme_combo.setCurrentText(self.settings.get("theme", "Темная"))
        appearance_layout.addWidget(self.theme_combo)

        label_opacity = QLabel("Прозрачность:")
        label_opacity.setStyleSheet(SETTINGS_LABEL_STYLE)
        appearance_layout.addWidget(label_opacity)

        self.opacity_slider = QSlider(Qt.Orientation.Horizontal)
        self.opacity_slider.setStyleSheet(SETTINGS_SLIDER_STYLE)
        self.opacity_slider.setRange(10, 100)
        self.opacity_slider.setValue(
            int(self.settings.get("idle_opacity", 0.3) * 100)
        )
        appearance_layout.addWidget(self.opacity_slider)

        layout.addWidget(appearance_group)

        # ----------------------------------------------------
        # VERSION
        # ----------------------------------------------------

        version_label = QLabel(f"Версия: {APP_VERSION}")
        version_label.setStyleSheet(SETTINGS_VERSION_STYLE)
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(version_label)

        # ----------------------------------------------------
        # BUTTONS
        # ----------------------------------------------------

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

    # ========================================================
    # SAVE
    # ========================================================

    def save_and_close(self):
        self.settings["hotkeys"] = {
            "increment": self.hotkey_increment.text(),
            "decrement": self.hotkey_decrement.text(),
        }
        self.settings["autostart"] = self.autostart_checkbox.isChecked()
        self.settings["theme"] = self.theme_combo.currentText()
        self.settings["idle_opacity"] = self.opacity_slider.value() / 100.0

        self.storage.save_settings(self.settings)
        self.close()

    # ========================================================
    # DRAG
    # ========================================================

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
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
                event.globalPosition().toPoint() - self.drag_position
            )
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = None
            event.accept()