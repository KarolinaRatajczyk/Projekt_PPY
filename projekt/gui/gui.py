import json
from datetime import date

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
        main_layout = QHBoxLayout()
        self.user_tab.setLayout(main_layout)

        left_column = QVBoxLayout()

        self.search_input_user = QLineEdit()
        self.search_input_user.setPlaceholderText("Szukaj w mojej kolekcji...")
        self.search_input_user.textChanged.connect(self.search_user_movies)
        left_column.addWidget(self.search_input_user)


        # ZMIENIONE SORTOWANIE
        self.sort_combo_user = QComboBox()
        self.sort_combo_user.addItems(
            ["Sortuj wg: Tytuł A-Z", "Tytuł Z-A", "Rok (rosnąco)", "Rok (malejąco)", "Ocena (rosnąco)",
             "Ocena (malejąco)"])
        self.sort_combo_user.currentIndexChanged.connect(self.sort_user_movies)
        left_column.addWidget(self.sort_combo_user)
        # --------------------

        self.movie_list = QListWidget()
        self.movie_list.itemClicked.connect(self.show_movie_details)
        self.movie_list.setStyleSheet("""
            QListWidget {
                font-size: 13px;
                padding: 5px;
            }
        """)

        left_column.addWidget(self.movie_list)

        main_layout.addLayout(left_column, 1)

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



        self.edit_film_button = QPushButton("✏️ Edytuj film")
        self.edit_film_button.clicked.connect(self.open_edit_movie_dialog)
        self.edit_film_button.setStyleSheet("""
            QPushButton {
                background-color: #1976D2;;
                color: white;
                font-weight: bold;
                border: none;
                padding: 10px;
                border-radius: 5px;
                }
                QPushButton:hover {
                background-color: #1565C0;
            }""")
        right_layout.addWidget(self.edit_film_button)


        self.delete_film_button = QPushButton("🗑️ Usuń film")
        self.delete_film_button.clicked.connect(self.delete_selected_movie)
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
        right_layout.addWidget(self.delete_film_button)

        main_layout.addLayout(right_layout, 2)
        self.load_user_movies()

    def search_user_movies(self, text):
        text = text.strip().lower()
        self.movie_list.clear()

        for movie in self.user.movies:
            if text in movie.title.lower():
                self.movie_list.addItem(f"{movie.title} ({movie.year})")

    def load_user_movies(self):
        self.movie_list.clear()
        for movie in self.user.movies:
            self.movie_list.addItem(f"{movie.title} ({movie.year})")

    def show_movie_details(self, item):
        index = self.movie_list.row(item)
        movie = self.user.movies[index]

        # ✅ Zmieniono: movie['status'] → movie.status
        if movie.status.lower() == "watched":
            pass  # jeśli chcesz coś dodać, możesz tutaj

        text = (
            f"<h3 style='margin-bottom: 10px;'>{movie.title} ({movie.year})</h3>"
            f"<div style='font-size: 13px;'>"
            f"<b>Reżyser:</b> {movie.director}<br>"
            f"<b>Gatunek:</b> {movie.genre}<br>"
            f"<b>Status:</b> {movie.status}<br>"
            f"<b>Ocena:</b> {movie.rating}<br>"
            f"<b>Opis:</b> {movie.description}<br>"
            f"<b>Data obejrzenia:</b> {getattr(movie, 'watch_date', 'Brak')}"
            f"</div>"
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

    def open_edit_movie_dialog(self):
        index = self.movie_list.currentRow()
        if index == -1:
            QMessageBox.warning(self, "Błąd", "Wybierz film do edycji.")
            return

        from gui.gui_edit_movie import EditMovieWindow

        movie = self.user.movies[index]
        dialog = EditMovieWindow(self, movie)
        if dialog.exec():
            updated_movie = dialog.get_updated_movie()
            self.user.movies[index] = updated_movie
            self.user_manager.save_users()
            self.load_user_movies()
            self.update_stats()


    def init_sample_tab(self):
        main_layout = QVBoxLayout()
        self.sample_tab.setLayout(main_layout)

        self.search_input_sample = QLineEdit()
        self.search_input_sample.setPlaceholderText("Szukaj w bazie filmów...")
        self.search_input_sample.textChanged.connect(self.search_sample_movies)
        main_layout.addWidget(self.search_input_sample)

        content_layout = QHBoxLayout()
        main_layout.addLayout(content_layout)

        self.sample_list = QListWidget()
        self.sample_list.itemClicked.connect(self.show_sample_movie_details)
        content_layout.addWidget(self.sample_list, 1)

        right_panel = QVBoxLayout()

        self.sample_details_label = QLabel("Wybierz film z listy, by zobaczyć szczegóły.")
        self.sample_details_label.setWordWrap(True)
        right_panel.addWidget(self.sample_details_label)

        self.sample_comment_edit = QTextEdit()
        self.add_comment_button = QPushButton("💬 Dodaj komentarz")
        self.add_comment_button.clicked.connect(self.add_sample_comment)
        right_panel.addWidget(self.add_comment_button)

        # self.sample_comment_edit.setPlaceholderText("Dodaj komentarz (opcjonalnie)")
        right_panel.addWidget(self.sample_comment_edit)



        self.add_sample_button = QPushButton("Dodaj wybrany film do moich")
        self.add_sample_button.clicked.connect(self.add_selected_sample)
        right_panel.addWidget(self.add_sample_button)

        content_layout.addLayout(right_panel, 2)

        base_dir = Path(__file__).resolve().parent.parent
        self.sample_file = base_dir / "data" / "sample_movies.json"

        with self.sample_file.open("r", encoding="utf-8") as f:
            self.sample_movies = json.load(f)

        for movie in self.sample_movies:
            self.sample_list.addItem(f"{movie['title']} ({movie['year']})")

    def show_sample_movie_details(self, item):
        index = self.sample_list.row(item)
        movie = self.sample_movies[index]

        text = (
            f"<h3>{movie['title']} ({movie['year']})</h3>"
            f"<b>Reżyser:</b> {movie['director']}<br>"
            f"<b>Gatunek:</b> {movie['genre']}<br>"
            f"<b>Ocena:</b> {movie['rating']}<br>"
            f"<b>Opis:</b> {movie['description']}<br>"
            f"<b>Data obejrzenia:</b> {movie.get('watch_date', 'Brak')}<br><br>"
            f"<b>Komentarze użytkowników:</b><br>"
        )

        comments = movie.get("comments", [])
        if comments:
            text += "<ul style='padding-left: 15px;'>"
            for c in comments:
                user = c.get("user", "Nieznany")
                date = c.get("date", "Brak daty")
                comment = c.get("comment", "")
                text += f"<li><b>{user}</b> ({date}): {comment}</li>"
            text += "</ul>"
        else:
            text += "<i>Brak komentarzy.</i>"

        self.sample_details_label.setText(text)

    def search_sample_movies(self, text):
        text = text.strip().lower()
        self.sample_list.clear()

        for movie in self.sample_movies:
            if text in movie["title"].lower():
                self.sample_list.addItem(f"{movie['title']} ({movie['year']})")

    def add_selected_sample(self):
        index = self.sample_list.currentRow()
        if index == -1:
            QMessageBox.warning(self, "Błąd", "Wybierz film z listy!")
            return

        movie_data = self.sample_movies[index]

        if any(m.title == movie_data["title"] and m.year == movie_data["year"] for m in self.user.movies):
            QMessageBox.information(self, "Uwaga", "Ten film już znajduje się na Twojej liście!")
            return


        # Dodaj komentarz użytkownika do JSON-a
        comment_text = self.sample_comment_edit.toPlainText().strip()
        if comment_text:
            comment_entry = {
                "user": self.user.username,
                "comment": comment_text,
                "date": str(date.today())
            }
            movie_data.setdefault("comments", []).append(comment_entry)

            # Zapisz komentarz do pliku JSON
            with self.sample_file.open("w", encoding="utf-8") as f:
                json.dump(self.sample_movies, f, indent=2, ensure_ascii=False)

        # Dodaj film do listy użytkownika
        from models.movie import Movie

        movie = Movie(
            title=movie_data["title"],
            director=movie_data["director"],
            year=movie_data["year"],
            genre=movie_data["genre"],
            status=movie_data["status"],
            rating=movie_data["rating"],
            description=movie_data["description"],
            watch_date=movie_data.get("watch_date")
        )
        movie.comments = movie_data.get("comments", [])

        self.user.movies.append(movie)
        self.user_manager.save_users()
        self.load_user_movies()

        QMessageBox.information(self, "Dodano", f"Film '{movie.title}' został dodany do Twojej listy.")
        self.sample_comment_edit.clear()

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

    def add_sample_comment(self):
        index = self.sample_list.currentRow()
        if index == -1:
            QMessageBox.warning(self, "Błąd", "Wybierz film, do którego chcesz dodać komentarz.")
            return

        comment_text = self.sample_comment_edit.toPlainText().strip()
        if not comment_text:
            QMessageBox.warning(self, "Błąd", "Komentarz nie może być pusty.")
            return

        movie_data = self.sample_movies[index]
        comment_entry = {
            "user": self.user.username,
            "comment": comment_text,
            "date": str(date.today())
        }

        movie_data.setdefault("comments", []).append(comment_entry)

        # Zapisz do pliku
        with self.sample_file.open("w", encoding="utf-8") as f:
            json.dump(self.sample_movies, f, indent=2, ensure_ascii=False)

        # Wyczyszczenie pola i odświeżenie widoku
        self.sample_comment_edit.clear()
        self.show_sample_movie_details(self.sample_list.item(index))
        QMessageBox.information(self, "Sukces", "Komentarz został dodany.")

    def sort_user_movies(self):
        current = self.sort_combo_user.currentText()

        if current == "Tytuł A-Z":
            sorted_movies = sorted(self.user.movies, key=lambda m: m.title.lower())
        elif current == "Tytuł Z-A":
            sorted_movies = sorted(self.user.movies, key=lambda m: m.title.lower(), reverse=True)
        elif current == "Rok (rosnąco)":
            sorted_movies = sorted(self.user.movies, key=lambda m: m.year)
        elif current == "Rok (malejąco)":
            sorted_movies = sorted(self.user.movies, key=lambda m: m.year, reverse=True)
        elif current == "Ocena (rosnąco)":
            sorted_movies = sorted(self.user.movies, key=lambda m: float(m.rating))
        elif current == "Ocena (malejąco)":
            sorted_movies = sorted(self.user.movies, key=lambda m: float(m.rating), reverse=True)

        else:
            sorted_movies = self.user.movies

        self.movie_list.clear()
        for movie in sorted_movies:
            self.movie_list.addItem(f"{movie.title} ({movie.year})")
