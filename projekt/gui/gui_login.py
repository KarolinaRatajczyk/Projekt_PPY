from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox
)
from exceptions.exceptions import UserError, WrongStatus
from gui.gui_register import RegisterWindow


class LoginWindow(QDialog):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager
        self.user = None
        self.register_window = None
        self.setWindowTitle("Logowanie")

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Nazwa użytkownika")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Hasło")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        login_button = QPushButton("Zaloguj")
        login_button.clicked.connect(self.attempt_login)

        register_button = QPushButton("Zarejestruj")
        register_button.clicked.connect(self.show_register_window)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Nazwa użytkownika:"))
        layout.addWidget(self.username_input)
        layout.addWidget(QLabel("Hasło:"))
        layout.addWidget(self.password_input)
        layout.addWidget(login_button)
        layout.addWidget(register_button)

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

    def show_register_window(self):
        if not self.register_window:
            self.register_window = RegisterWindow(self.manager)
            self.register_window.registration_successful.connect(self.on_registration_successful)
        self.register_window.show()

    def on_registration_successful(self):
        # Po pomyślnej rejestracji wpisz nazwę użytkownika w pole logowania
        self.username_input.setText(self.register_window.username_input.text())
        self.password_input.setFocus()
        QMessageBox.information(self, "Rejestracja zakończona", "Możesz się teraz zalogować.")
