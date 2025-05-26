import json
from PySide6.QtWidgets import (
    QWidget, QListWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QTextEdit, QFormLayout, QMessageBox,
    QComboBox, QTabWidget
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from projekt.models.movie import Movie
from projekt.managers.movieManager import MovieManager


class MainAppWindow(QWidget):
    def __init__(self, user, movie_manager: MovieManager):
        super().__init__()
        self.user = user
        self.movie_manager = movie_manager
        self.setWindowTitle(f"Witaj, {self.user.username}!")
        self.resize(800, 500)

        self.tabs = QTabWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        self.setLayout(layout)

        # --- TAB 1: Lista filmów użytkownika
        self.user_tab = QWidget()
        self.init_user_tab()
        self.tabs.addTab(self.user_tab, "Moje filmy")

        # --- TAB 2: Dodaj z listy dostępnych
        self.sample_tab = QWidget()
        self.init_sample_tab()
        self.tabs.addTab(self.sample_tab, "Dodaj z bazy filmów")

        # --- TAB 3: Statystyki
        self.stats_tab = QWidget()
        self.init_stats_tab()
        self.tabs.addTab(self.stats_tab, "Statystyki")

    # === Moje filmy ===
    def init_user_tab(self):
        layout = QHBoxLayout()
        self.user_tab.setLayout(layout)

        self.movie_list = QListWidget()
        self.movie_list.itemClicked.connect(self.show_movie_details)
        layout.addWidget(self.movie_list, 1)

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

        layout.addLayout(right_layout, 2)
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
            f"Data obejrzenia: {getattr(movie, 'watch_date', 'Brak')}"
        )
        self.details_label.setText(text)
        self.update_stats()

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

        movie = Movie(title, director, year, genre, status, rating, description)
        self.user.movies.append(movie)
        self.load_user_movies()
        self.clear_form()
        QMessageBox.information(self, "Sukces", f"Dodano film '{title}'")
        self.update_stats()

    def clear_form(self):
        self.title_input.clear()
        self.director_input.clear()
        self.year_input.clear()
        self.genre_input.clear()
        self.rating_input.clear()
        self.description_input.clear()
        self.status_input.setCurrentIndex(0)

    # === Lista gotowych filmów ===
    def init_sample_tab(self):
        layout = QVBoxLayout()
        self.sample_tab.setLayout(layout)

        self.sample_list = QListWidget()
        layout.addWidget(self.sample_list)
        self.sample_comment = QTextEdit()
        self.sample_comment.setPlaceholderText("Dodaj komentarz (opcjonalnie)")
        layout.addWidget(self.sample_comment)

        self.add_sample_button = QPushButton("Dodaj wybrany film do moich")
        self.add_sample_button.clicked.connect(self.add_selected_sample)
        layout.addWidget(self.add_sample_button)

        with open("C:/Users/gorka/PycharmProjects/Projekt_PPY/projekt/data/sample_movies.json", "r", encoding="utf-8") as f:
            self.sample_movies = json.load(f)

        for m in self.sample_movies:
            self.sample_list.addItem(f"{m['title']} ({m['year']})")

    def add_selected_sample(self):
        index = self.sample_list.currentRow()
        if index == -1:
            QMessageBox.warning(self, "Błąd", "Wybierz film z listy!")
            return

        movie_data = self.sample_movies[index]
        movie = Movie(
            title=movie_data["title"],
            director=movie_data["director"],
            year=movie_data["year"],
            genre=movie_data["genre"],
            status=movie_data["status"],
            rating=movie_data["rating"],
            description=self.sample_comment.toPlainText() or movie_data["description"]
        )
        setattr(movie, "watch_date", movie_data.get("watched_date"))

        self.user.movies.append(movie)
        self.load_user_movies()
        self.sample_comment.clear()
        QMessageBox.information(self, "Dodano", f"Film '{movie.title}' został dodany.")
        self.update_stats()

    # === Statystyki matplotlib ===
    def init_stats_tab(self):
        layout = QVBoxLayout()
        self.stats_tab.setLayout(layout)

        self.canvas = FigureCanvas(Figure(figsize=(5, 3)))
        layout.addWidget(self.canvas)
        self.update_stats()

    def update_stats(self):
        self.canvas.figure.clf()
        ax = self.canvas.figure.add_subplot(111)
        watched = [m.rating for m in self.user.movies if m.status.lower() == "watched" and m.rating is not None]
        labels = [m.title for m in self.user.movies if m.status.lower() == "watched" and m.rating is not None]

        if watched:
            ax.bar(labels, watched, color='skyblue')
            ax.set_title("Oceny obejrzanych filmów")
            ax.set_ylabel("Ocena")
            ax.set_ylim(0, 10)
            ax.set_xticklabels(labels, rotation=45, ha='right')
        else:
            ax.text(0.5, 0.5, "Brak danych do wyświetlenia", ha='center', va='center')

        self.canvas.draw()
