from PySide6.QtWidgets import QDialog, QLineEdit, QPushButton, QVBoxLayout, QLabel, QMessageBox

class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Logowanie")
        self.setFixedSize(300, 150)

        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton("Zaloguj")
        self.login_button.clicked.connect(self.attempt_login)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Nazwa użytkownika:"))
        layout.addWidget(self.username_input)
        layout.addWidget(QLabel("Hasło:"))
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        self.setLayout(layout)

    def attempt_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if self.manager.authenticate_user(username, password):
            self.accept()  # zamyka okno z wynikiem „sukces”
        else:
            QMessageBox.warning(self, "Błąd", "Niepoprawne dane")
