from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)
from projekt.exceptions.exceptions import UserError, WrongStatus


class LoginWindow(QDialog):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager
        self.user = None
        self.setWindowTitle("Logowanie")

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Nazwa użytkownika")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Hasło")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        login_button = QPushButton("Zaloguj")
        login_button.clicked.connect(self.attempt_login)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Nazwa użytkownika:"))
        layout.addWidget(self.username_input)
        layout.addWidget(QLabel("Hasło:"))
        layout.addWidget(self.password_input)
        layout.addWidget(login_button)

        self.setLayout(layout)

    def attempt_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        try:
            user = self.manager.authenticate_user(username, password)
            self.user = user
            self.accept()
        except (UserError, WrongStatus) as e:
            QMessageBox.critical(self, "Błąd logowania", str(e))
