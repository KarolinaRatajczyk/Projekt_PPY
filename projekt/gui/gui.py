import json
from PySide6.QtWidgets import (
    QWidget, QListWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QTextEdit, QFormLayout, QMessageBox,
    QComboBox, QTabWidget, QScrollArea, QGroupBox
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
        self.movie_list.setStyleSheet("""
        QListWidget {
            font-size: 13px;
            padding: 5px;
        }
        """)

        layout.addWidget(self.movie_list, 1)

        right_layout = QVBoxLayout()
        self.details_box = QGroupBox("Sczegóły filmu")
        self.details_box.setStyleSheet("""
                QGroupBox {
                    font-weight: bold;
                    border: 1px solid #ccc;
                    border-radius: 5px;
                    margin-top: 10px;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 3px 0 3px;
                }
        """)

        self.details_label = QLabel("Wybierz film z listy")
        self.details_label.setWordWrap(True)

        details_layout = QVBoxLayout()
        details_layout.addWidget(self.details_label)
        self.details_box.setLayout(details_layout)
        right_layout.addWidget(self.details_box)


        self.add_film_button = QPushButton("➕ Dodaj film ręcznie")
        self.add_film_button.clicked.connect(self.open_add_movie_dialog)
        self.add_film_button.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    font-weight: bold;
                    border: none;
                    padding: 10px;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
        """)
        right_layout.addWidget(self.add_film_button)


        self.delete_film_button = QPushButton("🗑️ Usuń film")
        self.delete_film_button.setStyleSheet("""
            QPushButton {
                background-color: #e53935;
                color: white;
                font-weight: bold;
                border: none;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #c62828;
            }
        """)
        self.delete_film_button.clicked.connect(self.delete_selected_movie)
        right_layout.addWidget(self.delete_film_button)

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


    def delete_selected_movie(self):
        index = self.movie_list.currentRow()
        if index == -1:
            QMessageBox.warning(self, "Błąd", "Nie wybrano żadnego filmu do usunięcia.")
            return

        confirm = QMessageBox.question(
            self,
            "Potwierdź usunięcie",
            "Czy na pewno chcesz usunąć ten film?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirm == QMessageBox.StandardButton.Yes:
            movie = self.user.movies[index]
            del self.user.movies[index]
            self.user_manager.save_users()
            self.load_user_movies()
            self.details_label.setText("Wybierz film z listy")
            self.update_stats()


