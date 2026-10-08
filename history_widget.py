from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QScrollArea,
    QWidget,
)

from styles import (
    HISTORY_WIDGET_STYLE,
    HISTORY_TITLE_STYLE,
    HISTORY_ITEM_STYLE,
    HISTORY_ITEM_DATE_STYLE,
    HISTORY_ITEM_VALUE_STYLE,
    HISTORY_EMPTY_STYLE,
    HISTORY_SCROLL_STYLE,
    DELETE_BUTTON_STYLE,
)


MONTHS = [
    "января", "февраля", "марта", "апреля", "мая", "июня",
    "июля", "августа", "сентября", "октября", "ноября", "декабря",
]


def format_date_time(value):
    month = MONTHS[value.month - 1]
    return (
        f"{value.day} {month} "
        # f"{value.hour} часов "
        # f"{value.minute} минут"
    )


class HistoryItem(QFrame):

    delete_requested = Signal(object)

    def __init__(self, item, parent=None):
        super().__init__(parent)

        self.item = item

        self.setObjectName("historyItem")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet(HISTORY_ITEM_STYLE)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(7)

        date_label = QLabel(format_date_time(item["saved_at"]))
        date_label.setWordWrap(True)
        date_label.setStyleSheet(HISTORY_ITEM_DATE_STYLE)

        value_label = QLabel(str(item["value"]))
        value_label.setStyleSheet(HISTORY_ITEM_VALUE_STYLE)
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        delete_button = QPushButton("×")
        delete_button.setFixedSize(26, 26)
        delete_button.setCursor(Qt.CursorShape.PointingHandCursor)
        delete_button.setStyleSheet(DELETE_BUTTON_STYLE)
        delete_button.clicked.connect(
            lambda: self.delete_requested.emit(self.item)
        )

        layout.addWidget(date_label, 1)
        layout.addWidget(value_label)
        layout.addWidget(delete_button)


class HistoryWidget(QFrame):

    ITEM_HEIGHT = 30
    VISIBLE_ITEMS = 4

    def __init__(self, storage, parent=None):
        super().__init__(parent)

        self.storage = storage

        self.setObjectName("historyWidget")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet(HISTORY_WIDGET_STYLE)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(6, 10, 0, 0)
        self.layout.setSpacing(5)

        # ----------------------------------------------------
        # TITLE
        # ----------------------------------------------------

        title = QLabel("История")
        title.setStyleSheet(HISTORY_TITLE_STYLE)
        self.layout.addWidget(title)

        # ----------------------------------------------------
        # SCROLL AREA
        # ----------------------------------------------------

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        self.scroll_area.setStyleSheet(HISTORY_SCROLL_STYLE)

        self.items_widget = QWidget()
        self.items_widget.setStyleSheet("background: transparent;")

        self.items_container = QVBoxLayout(self.items_widget)
        self.items_container.setContentsMargins(0, 0, 6, 0)
        self.items_container.setSpacing(5)

        self.scroll_area.setWidget(self.items_widget)
        self.layout.addWidget(self.scroll_area)

        visible_height = (
            self.VISIBLE_ITEMS * self.ITEM_HEIGHT
            + (self.VISIBLE_ITEMS - 1) * 5
        )
        self.scroll_area.setFixedHeight(visible_height)

        self.reload()

    # ========================================================
    # RELOAD
    # ========================================================

    def reload(self):
        while self.items_container.count():
            item = self.items_container.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()

        history = self.storage.get_history()

        if not history:
            empty = QLabel("История пока пуста")
            empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty.setStyleSheet(HISTORY_EMPTY_STYLE)
            self.items_container.addWidget(empty)
            self.items_container.addStretch()
            return

        for item in history:
            widget = HistoryItem(item)
            widget.delete_requested.connect(self.delete_item)
            self.items_container.addWidget(widget)

        self.items_container.addStretch()

    # ========================================================
    # DELETE
    # ========================================================

    def delete_item(self, item):
        self.storage.delete_date(item["date"])
        self.reload()