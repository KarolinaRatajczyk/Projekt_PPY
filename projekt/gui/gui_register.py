from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QWidget, QLineEdit, QPushButton,
    QVBoxLayout, QLabel, QMessageBox
)
from exceptions.exceptions import UserAlreadyExists


class RegisterWindow(QWidget):
    registration_successful = Signal()

    def __init__(self, user_manager):
        super().__init__()
        self.setWindowTitle("Rejestracja")
        self.user_manager = user_manager

        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.register_button = QPushButton("Zarejestruj")

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Nazwa użytkownika:"))
        layout.addWidget(self.username_input)
        layout.addWidget(QLabel("Hasło:"))
        layout.addWidget(self.password_input)
        layout.addWidget(self.register_button)
        self.setLayout(layout)

        self.register_button.clicked.connect(self.register_user)

    def register_user(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Błąd", "Wszystkie pola są wymagane.")
            return

        try:
            self.user_manager.register_user(username, password)
            QMessageBox.information(self, "Sukces", "Użytkownik zarejestrowany!")
            self.registration_successful.emit()  # emitujemy sygnał do LoginWindow
            self.close()
        except UserAlreadyExists:
            QMessageBox.warning(self, "Błąd", "Użytkownik już istnieje.")
