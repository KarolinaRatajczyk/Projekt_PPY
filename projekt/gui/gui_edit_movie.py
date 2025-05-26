from PySide6.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QComboBox, QTextEdit, QPushButton, \
    QMessageBox
from models.movie import Movie

class EditMovieWindow(QDialog):
    def __init__(self, parent, movie: Movie):
        super().__init__(parent)
        self.setWindowTitle("Edytuj film")
        self.original_id = movie.id

        layout = QVBoxLayout()
        form = QFormLayout()

        self.title_input = QLineEdit(movie.title)
        self.director_input = QLineEdit(movie.director)
        self.year_input = QLineEdit(str(movie.year))
        self.genre_input = QLineEdit(movie.genre)
        self.status_input = QComboBox()
        self.status_input.addItems(["obejrzany", "do obejrzenia"])
        self.status_input.setCurrentText(movie.status)
        self.rating_input = QLineEdit(str(movie.rating) if movie.rating is not None else "")
        self.description_input = QTextEdit(movie.description)

        form.addRow("Tytuł:", self.title_input)
        form.addRow("Reżyser:", self.director_input)
        form.addRow("Rok:", self.year_input)
        form.addRow("Gatunek:", self.genre_input)
        form.addRow("Status:", self.status_input)
        form.addRow("Ocena (0-10):", self.rating_input)
        form.addRow("Opis:", self.description_input)

        self.save_button = QPushButton("Zapisz zmiany")
        self.save_button.clicked.connect(self.validate_and_accept)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def validate_and_accept(self):
        title = self.title_input.text().strip()
        director = self.director_input.text().strip()
        if not title or not director:
            QMessageBox.warning(self, "Błąd", "Tytuł i reżyser są wymagane!")
            return

        rating_text = self.rating_input.text().strip()
        try:
            rating = float(rating_text) if rating_text else None
            if rating is not None and not (0 <= rating <= 10):
                raise ValueError()
        except ValueError:
            QMessageBox.warning(self, "Błąd", "Ocena musi być liczbą od 0 do 10")
            return

        self.accept()

    def get_updated_movie(self):
        movie = Movie(
            title=self.title_input.text().strip(),
            director=self.director_input.text().strip(),
            year=self.year_input.text().strip(),
            genre=self.genre_input.text().strip(),
            status=self.status_input.currentText(),
            rating=float(self.rating_input.text()) if self.rating_input.text().strip() else None,
            description=self.description_input.toPlainText().strip()
        )
        movie.id = self.original_id
        return movie
