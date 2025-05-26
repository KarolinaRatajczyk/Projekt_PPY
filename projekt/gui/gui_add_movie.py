from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, QComboBox,
    QTextEdit, QPushButton, QMessageBox, QListWidget
)
from models.movie import Movie
from typing import List, Optional


class AddMovieWindow(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.movie: Optional[Movie] = None
        self.comments: List[str] = []

        self.setWindowTitle("Dodaj nowy film")

        layout = QVBoxLayout()
        form = QFormLayout()

        self.title_input = QLineEdit()
        self.director_input = QLineEdit()
        self.year_input = QLineEdit()
        self.genre_input = QLineEdit()
        self.status_input = QComboBox()
        self.status_input.addItems(["obejrzany", "do obejrzenia"])
        self.rating_input = QLineEdit()
        self.description_input = QTextEdit()

        form.addRow("Tytuł:", self.title_input)
        form.addRow("Reżyser:", self.director_input)
        form.addRow("Rok:", self.year_input)
        form.addRow("Gatunek:", self.genre_input)
        form.addRow("Status:", self.status_input)
        form.addRow("Ocena (0-10):", self.rating_input)
        form.addRow("Opis:", self.description_input)

        layout.addLayout(form)

        self.comment_input = QTextEdit()
        self.comment_input.setPlaceholderText("Dodaj komentarz...")
        self.add_comment_button = QPushButton("Dodaj komentarz")
        self.comment_list = QListWidget()

        self.add_comment_button.clicked.connect(self.add_comment)

        layout.addWidget(self.comment_input)
        layout.addWidget(self.add_comment_button)
        layout.addWidget(self.comment_list)

        self.add_button = QPushButton("Dodaj film")
        self.add_button.clicked.connect(self.accept_dialog)
        layout.addWidget(self.add_button)

        self.setLayout(layout)

    def add_comment(self) -> None:
        comment = self.comment_input.toPlainText().strip()
        if comment:
            self.comments.append(comment)
            self.comment_list.addItem(comment)
            self.comment_input.clear()
        else:
            QMessageBox.warning(self, "Błąd", "Komentarz nie może być pusty!")

    def accept_dialog(self) -> None:
        title = self.title_input.text().strip()
        director = self.director_input.text().strip()
        year = self.year_input.text().strip()
        genre = self.genre_input.text().strip()
        status = self.status_input.currentText()
        rating_text = self.rating_input.text().strip()
        description = self.description_input.toPlainText().strip()

        if not title or not director:
            QMessageBox.warning(self, "Błąd", "Tytuł i reżyser są wymagane!")
            return

        try:
            rating = float(rating_text) if rating_text else None
            if rating is not None and not (0 <= rating <= 10):
                raise ValueError()
        except ValueError:
            QMessageBox.warning(self, "Błąd", "Ocena musi być liczbą od 0 do 10")
            return

        self.movie = Movie(title, director, year, genre, status, rating, description)
        self.accept()

    def get_movie(self) -> Optional[Movie]:
        return self.movie

    def get_comments(self) -> List[str]:
        return self.comments
