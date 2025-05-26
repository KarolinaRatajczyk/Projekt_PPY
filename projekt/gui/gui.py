import json
from PySide6.QtWidgets import (
    QWidget, QListWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QTextEdit, QFormLayout, QMessageBox,
    QComboBox, QTabWidget, QScrollArea
)

from pathlib import Path

from managers.movieManager import MovieManager
from models.movie import Movie
from utils.statistics import Statistics
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class MainAppWindow(QWidget):
    def __init__(self, user, movie_manager: MovieManager, user_manager):
        super().__init__()
        self.user = user
        self.movie_manager = movie_manager
        self.user_manager = user_manager
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

        self.add_film_button = QPushButton("➕ Dodaj film ręcznie")
        self.add_film_button.clicked.connect(self.open_add_movie_dialog)
        right_layout.addWidget(self.add_film_button)

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

    def open_add_movie_dialog(self):
        from gui.gui_add_movie import AddMovieWindow

        dialog = AddMovieWindow(self)
        if dialog.exec():
            new_movie = dialog.get_movie()
            if new_movie:
                self.user.movies.append(new_movie)
                self.user_manager.save_users()
                self.load_user_movies()
                self.update_stats()

    # def add_movie(self):
    #     title = self.title_input.text().strip()
    #     director = self.director_input.text().strip()
    #     year = self.year_input.text().strip()
    #     genre = self.genre_input.text().strip()
    #     status = self.status_input.currentText()
    #     rating_text = self.rating_input.text().strip()
    #     description = self.description_input.toPlainText().strip()
    #
    #     if not title or not director:
    #         QMessageBox.warning(self, "Błąd", "Tytuł i reżyser są wymagane!")
    #         return
    #
    #     try:
    #         rating = float(rating_text) if rating_text else None
    #         if rating is not None and not (0 <= rating <= 10):
    #             raise ValueError()
    #     except ValueError:
    #         QMessageBox.warning(self, "Błąd", "Ocena musi być liczbą od 0 do 10")
    #         return
    #
    #     movie = Movie(title, director, year, genre, status, rating, description)
    #     self.user.movies.append(movie)
    #     self.load_user_movies()
    #     self.clear_form()
    #     QMessageBox.information(self, "Sukces", f"Dodano film '{title}'")
    #
    #     self.user_manager.save_users()
    #
    #     self.update_stats()

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

        base_dir = Path(__file__).resolve().parent.parent
        json_file = base_dir / "data" / "sample_movies.json"

        with json_file.open("r", encoding="utf-8") as f:
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

        self.user_manager.save_users()

        self.update_stats()

    def init_stats_tab(self):
        self.stats_tab_layout = QVBoxLayout()
        self.stats_tabs = QTabWidget()
        self.stats_tab.setLayout(self.stats_tab_layout)
        self.stats_tab_layout.addWidget(self.stats_tabs)

        self.ratings_widget = QWidget()
        self.ratings_layout = QVBoxLayout(self.ratings_widget)
        self.canvas_ratings = FigureCanvas(Statistics.plot_ratings_per_movie(self.user))
        self.ratings_layout.addWidget(self.canvas_ratings)
        self.stats_tabs.addTab(self.ratings_widget, "Oceny filmów")

        self.genre_widget = QWidget()
        self.genre_layout = QVBoxLayout(self.genre_widget)
        self.canvas_genre = FigureCanvas(Statistics.plot_movies_by_genre(self.user))
        self.genre_layout.addWidget(self.canvas_genre)
        self.stats_tabs.addTab(self.genre_widget, "Gatunki")

        self.avg_widget = QWidget()
        self.avg_layout = QVBoxLayout(self.avg_widget)
        self.canvas_avg = FigureCanvas(Statistics.plot_average_rating(self.user))
        self.avg_layout.addWidget(self.canvas_avg)
        self.stats_tabs.addTab(self.avg_widget, "Średnia")

        self.best_widget = QWidget()
        self.best_layout = QVBoxLayout(self.best_widget)
        self.canvas_best = FigureCanvas(Statistics.plot_top_rated_movie(self.user))
        self.best_layout.addWidget(self.canvas_best)
        self.stats_tabs.addTab(self.best_widget, "Najlepszy film")



    def update_stats(self):
        self.canvas_ratings.figure = Statistics.plot_ratings_per_movie(self.user)
        self.canvas_ratings.draw()

        self.canvas_genre.figure = Statistics.plot_movies_by_genre(self.user)
        self.canvas_genre.draw()

        self.canvas_avg.figure = Statistics.plot_average_rating(self.user)
        self.canvas_avg.draw()

        self.canvas_best.figure = Statistics.plot_top_rated_movie(self.user)
        self.canvas_best.draw()


        avg = Statistics.get_average_rating(self.user)
        top = Statistics.get_top_rated_movie(self.user)

        if avg is not None and top is not None:
            summary = f"Średnia ocena: {avg:.2f}   |   Najlepszy film: {top.title} ({top.rating}/10)"
        else:
            summary = "Brak wystarczających danych do podsumowania"


