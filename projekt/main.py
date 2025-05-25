from PySide6.QtWidgets import QApplication
from projekt.gui.gui_login import LoginWindow
# from gui_main import MainWindow  # główne okno z listą filmów

app = QApplication([])

login = LoginWindow()
if login.exec() == LoginWindow.Accepted:
    username = login.username_input.text()
    # window = MainWindow(username)
    # window.show()
    # app.exec()
# dupa dupa