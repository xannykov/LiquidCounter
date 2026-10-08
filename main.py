import sys

from PySide6.QtWidgets import QApplication

from config import (
    APP_NAME,
    DATA_FILE,
)

from storage import Storage
from main_window import MainWindow


def main():

    app = QApplication(
        sys.argv
    )

    app.setApplicationName(
        APP_NAME
    )

    app.setQuitOnLastWindowClosed(
        True
    )

    # --------------------------------------------------------
    # STORAGE
    # --------------------------------------------------------

    storage = Storage(
        DATA_FILE
    )

    # --------------------------------------------------------
    # MAIN WINDOW
    # --------------------------------------------------------

    window = MainWindow(
        storage
    )

    window.show()

    sys.exit(
        app.exec()
    )


if __name__ == "__main__":
    main()