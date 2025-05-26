from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox
)
from exceptions.exceptions import UserError, WrongStatus
from managers.userManager import UserManager
from models.user import User
from typing import Optional


class LoginWindow(QDialog):
    def __init__(self, user_manager: UserManager) -> None:
        super().__init__()
        self.user_manager = user_manager
        self.user: Optional[User] = None
        self.setWindowTitle("Logowanie")

        self.layout = QVBoxLayout(self)

        # Logowanie
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Nazwa użytkownika")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Hasło")
        self.password_input.setEchoMode(QLineEdit.Password)

        login_button = QPushButton("Zaloguj")
        login_button.clicked.connect(self.attempt_login)

        register_button = QPushButton("Zarejestruj")
        register_button.clicked.connect(self.toggle_register_area)

        self.layout.addWidget(QLabel("Nazwa użytkownika:"))
        self.layout.addWidget(self.username_input)
        self.layout.addWidget(QLabel("Hasło:"))
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(login_button)
        self.layout.addWidget(register_button)

        # === REJESTRACJA (ukryta na start) ===
        self.register_username = QLineEdit()
        self.register_username.setPlaceholderText("Nowa nazwa użytkownika")

        self.register_password = QLineEdit()
        self.register_password.setPlaceholderText("Nowe hasło")
        self.register_password.setEchoMode(QLineEdit.Password)

        self.register_button_submit = QPushButton("Zarejestruj konto")
        self.register_button_submit.clicked.connect(self.register_user)

        # Ukrywamy domyślnie
        self.register_username.hide()
        self.register_password.hide()
        self.register_button_submit.hide()

        self.layout.addWidget(self.register_username)
        self.layout.addWidget(self.register_password)
        self.layout.addWidget(self.register_button_submit)

    def toggle_register_area(self) -> None:
        if self.register_username.isVisible():
            self.register_username.hide()
            self.register_password.hide()
            self.register_button_submit.hide()
        else:
            self.register_username.show()
            self.register_password.show()
            self.register_button_submit.show()

    def attempt_login(self) -> None:
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        try:
            user = self.user_manager.authenticate_user(username, password)
            self.user = user
            self.accept()
        except (UserError, WrongStatus) as e:
            QMessageBox.critical(self, "Błąd logowania", str(e))

    def register_user(self) -> None:
        username = self.register_username.text().strip()
        password = self.register_password.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Błąd", "Wszystkie pola muszą być wypełnione.")
            return

        try:
            self.user_manager.register_user(username, password)
            self.register_username.clear()
            self.register_password.clear()
            self.toggle_register_area()

            self.username_input.setText(username)
            self.password_input.setFocus()

        except ValueError as e:
            QMessageBox.warning(self, "Błąd", str(e))
