import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication

from gui.gui import MainAppWindow
from gui.gui_login import LoginWindow
from managers.movieManager import MovieManager
from managers.userManager import UserManager

if __name__ == "__main__":
    app = QApplication(sys.argv)

    BASE_DIR = Path(__file__).resolve().parent
    DATA_PATH = BASE_DIR / "data" / "users.json"

    user_manager = UserManager(DATA_PATH)
    movie_manager = MovieManager()

    login_dialog = LoginWindow(user_manager)

    if login_dialog.exec():
        user = login_dialog.user

        main_window = MainAppWindow(user, movie_manager)
        main_window.show()
        sys.exit(app.exec())  # <- aplikacja działa dopóki okno jest otwarte
