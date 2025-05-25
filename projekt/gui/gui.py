from PySide6.QtWidgets import (
    QWidget, QListWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QTextEdit, QFormLayout, QMessageBox, QComboBox
)
from projekt.models.movie import Movie
from projekt.managers.movieManager import MovieManager

class MainAppWindow(QWidget):
    def __init__(self, user, movie_manager: MovieManager):
        super().__init__()
        self.user = user
        self.movie_manager = movie_manager
        self.setWindowTitle(f"Witaj, {self.user.username}!")
        self.resize(600, 400)

        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

        self.movie_list = QListWidget()
        self.movie_list.itemClicked.connect(self.show_movie_details)
        main_layout.addWidget(self.movie_list, 1)

        right_layout = QVBoxLayout()
        self.details_label = QLabel("Wybierz film z listy")
        self.details_label.setWordWrap(True)
        right_layout.addWidget(self.details_label, 2)

        form_layout = QFormLayout()
        self.title_input = QLineEdit()
        self.director_input = QLineEdit()
        self.year_input = QLineEdit()
        self.genre_input = QLineEdit()
        self.status_input = QComboBox()
        self.status_input.addItems(["obejrzany", "do obejrzenia"])
        self.rating_input = QLineEdit()
        self.description_input = QTextEdit()

        form_layout.addRow("Tytuł:", self.title_input)
        form_layout.addRow("Reżyser:", self.director_input)
        form_layout.addRow("Rok:", self.year_input)
        form_layout.addRow("Gatunek:", self.genre_input)
        form_layout.addRow("Status:", self.status_input)
        form_layout.addRow("Ocena (0-10):", self.rating_input)
        form_layout.addRow("Opis:", self.description_input)

        right_layout.addLayout(form_layout)

        self.add_button = QPushButton("Dodaj film")
        self.add_button.clicked.connect(self.add_movie)
        right_layout.addWidget(self.add_button)

        main_layout.addLayout(right_layout, 2)

        self.load_user_movies()

    def load_user_movies(self):
        self.movie_list.clear()
        for movie in self.user.movies:
            self.movie_list.addItem(f"{movie.title} ({movie.year})")

    def show_movie_details(self, item):
        index = self.movie_list.row(item)
        movie = self.user.movies[index]
        text = (
            f"<b>{movie.title} ({movie.year})</b><br>"
            f"Reżyser: {movie.director}<br>"
            f"Gatunek: {movie.genre}<br>"
            f"Status: {movie.status}<br>"
            f"Ocena: {movie.rating}<br>"
            f"Opis: {movie.description}<br>"
            f"Data obejrzenia: {movie.watch_date if hasattr(movie, 'watch_date') else 'Brak'}"
        )
        self.details_label.setText(text)

    def add_movie(self):
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

        new_movie = Movie(title, director, year, genre, status, rating, description)
        self.user.movies.append(new_movie)
        self.load_user_movies()

        self.title_input.clear()
        self.director_input.clear()
        self.year_input.clear()
        self.genre_input.clear()
        self.rating_input.clear()
        self.description_input.clear()
        self.status_input.setCurrentIndex(0)

        QMessageBox.information(self, "Sukces", f"Dodano film '{title}'")
