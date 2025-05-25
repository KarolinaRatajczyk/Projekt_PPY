import sys
from PySide6.QtWidgets import QApplication

from projekt.gui.gui import MainAppWindow
from projekt.gui.gui_login import LoginWindow
from projekt.managers.movieManager import MovieManager
from projekt.managers.userManager import UserManager

if __name__ == "__main__":
    app = QApplication(sys.argv)

    user_manager = UserManager("C:/Users/Mateusz/PycharmProjects/Projekt_PPY/projekt/data/users.json")
    movie_manager = MovieManager()  # zakładam, że masz to

    login_dialog = LoginWindow(user_manager)

    if login_dialog.exec():
        user = login_dialog.user
        main_window = MainAppWindow(user, movie_manager)
        main_window.show()
        sys.exit(app.exec())  # <- aplikacja działa dopóki okno jest otwarte
