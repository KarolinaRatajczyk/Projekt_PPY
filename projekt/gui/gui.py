import json
from datetime import date

from PySide6.QtWidgets import (
    QWidget, QListWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QTextEdit, QMessageBox,
    QComboBox, QTabWidget, QScrollArea, QGroupBox
)

from pathlib import Path

from exceptions.exceptions import MovieNotSelectedError
from utils.file_operations import FileOperations
from managers.movieManager import MovieManager
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

        self.filtered_movies = self.user.movies.copy()

        self.user_tab = QWidget()
        self.init_user_tab()
        self.tabs.addTab(self.user_tab, "Moje filmy")

        self.history_tab = QWidget()
        self.init_history_tab()
        self.tabs.addTab(self.history_tab, "Historia")

        self.sample_tab = QWidget()
        self.init_sample_tab()
        self.tabs.addTab(self.sample_tab, "Dodaj z bazy filmów")

        self.stats_tab = QWidget()
        self.init_stats_tab()
        self.tabs.addTab(self.stats_tab, "Statystyki")


    def init_user_tab(self):
        main_layout = QHBoxLayout()
        self.user_tab.setLayout(main_layout)

        left_column = QVBoxLayout()

        self.search_input_user = QLineEdit()
        self.search_input_user.setPlaceholderText("Szukaj w mojej kolekcji...")
        self.search_input_user.textChanged.connect(self.search_user_movies)
        left_column.addWidget(self.search_input_user)


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
        self.details_label.setOpenExternalLinks(False)
        self.details_label.linkActivated.connect(self.toggle_movie_status)

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

        self.export_txt_button = QPushButton("📄 Eksportuj do TXT")
        self.export_txt_button.clicked.connect(self.export_movies_to_txt)
        self.export_txt_button.setStyleSheet("""
                    QPushButton {
                        background-color: #AB47BC;
                        color: white;
                        font-weight: bold;
                        border: none;
                        padding: 10px;
                        border-radius: 5px;
                        }
                        QPushButton:hover {
                        background-color: #9C27B0;
                    }""")
        right_layout.addWidget(self.export_txt_button)

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

    def init_history_tab(self) -> None:
        layout = QVBoxLayout()
        self.history_tab.setLayout(layout)

        title = QLabel("Lista obejrzanych filmów:")
        title.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                margin-bottom: 10px;
            }
        """)
        layout.addWidget(title)

        self.history_list = QListWidget()
        self.history_list.setStyleSheet("""
            QListWidget {
                background-color: #2c2c2c;
                font-size: 14px;
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            QListWidget::item {
                padding: 5px;
            }
        """)
        layout.addWidget(self.history_list)

        self.load_history()

    def load_history(self) -> None:
        self.history_list.clear()
        for movie in self.user.movies:
            if movie.status == "Obejrzano" and movie.watch_date:
                self.history_list.addItem(f"{movie.title} – {movie.watch_date}")

    def search_user_movies(self, text):
        text = text.strip().lower()
        self.filtered_movies = [movie for movie in self.user.movies if text in movie.title.lower()]
        self.update_movie_list_widget()

    def load_user_movies(self):
        self.filtered_movies = self.user.movies.copy()
        self.update_movie_list_widget()

    def export_movies_to_txt(self) -> None:
        try:
            filename = f"moje_filmy_{self.user.username}.txt"
            FileOperations.export_to_txt(self.user.movies, filename)
            QMessageBox.information(self, "Sukces", f"Filmy wyeksportowano do pliku: {filename}")
        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Nie udało się wyeksportować: {str(e)}")

    def show_movie_details(self, item):
        index = self.movie_list.row(item)
        if index < 0 or index >= len(self.filtered_movies):
            return
        movie = self.filtered_movies[index]

        if movie.status.lower() == "watched":
            pass

        text = (
            f"<h3 style='margin-bottom: 10px;'>{movie.title} ({movie.year})</h3>"
            f"<div style='font-size: 13px;'>"
            f"<b>Reżyser:</b> {movie.director}<br>"
            f"<b>Gatunek:</b> {movie.genre}<br>"
            # f"<b>Status:</b> {movie.status}<br>"
            f"<b>Status:</b> {movie.status} <a href='#toggle' style='color:#1976D2;'>[zmień]</a><br>"
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
        try:
            if index == -1:
                raise MovieNotSelectedError()
        except MovieNotSelectedError:
            QMessageBox.warning(self, "Błąd", "Wybierz film do edycji.")
            return

        movie = self.filtered_movies[index]
        from gui.gui_edit_movie import EditMovieWindow

        dialog = EditMovieWindow(self, movie)
        if dialog.exec():
            updated_movie = dialog.get_updated_movie()

            original_index = self.user.movies.index(movie)
            self.user.movies[original_index] = updated_movie

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


        comment_text = self.sample_comment_edit.toPlainText().strip()
        if comment_text:
            comment_entry = {
                "user": self.user.username,
                "comment": comment_text,
                "date": str(date.today())
            }
            movie_data.setdefault("comments", []).append(comment_entry)

            with self.sample_file.open("w", encoding="utf-8") as f:
                json.dump(self.sample_movies, f, indent=2, ensure_ascii=False)

        from models.movie import Movie

        movie = Movie(
            title=movie_data["title"],
            director=movie_data["director"],
            year=movie_data["year"],
            genre=movie_data["genre"],
            status="Do obejrzenia",
            rating=None,
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

        # Oceny obejrzanych
        self.ratings_widget = QWidget()
        self.ratings_layout = QVBoxLayout(self.ratings_widget)
        self.canvas_ratings = FigureCanvas(Statistics.plot_ratings_per_movie(self.user))
        self.ratings_layout.addWidget(self.canvas_ratings)
        self.stats_tabs.addTab(self.ratings_widget, "Oceny obejrzanych")

        # Gatunki
        self.genre_widget = QWidget()
        self.genre_layout = QVBoxLayout(self.genre_widget)
        self.canvas_genre = FigureCanvas(Statistics.plot_movies_by_genre(self.user))
        self.genre_layout.addWidget(self.canvas_genre)
        self.stats_tabs.addTab(self.genre_widget, "Gatunki")

        # Nowy: Status obejrzenia
        self.status_widget = QWidget()
        self.status_layout = QVBoxLayout(self.status_widget)
        self.canvas_status = FigureCanvas(Statistics.plot_watched_vs_unwatched(self.user))
        self.status_layout.addWidget(self.canvas_status)
        self.stats_tabs.addTab(self.status_widget, "Obejrzane vs. nie")

        # Tekst: Najlepszy film
        self.best_widget = QWidget()
        self.best_layout = QVBoxLayout(self.best_widget)
        self.canvas_best = FigureCanvas(Statistics.plot_top_rated_text(self.user))
        self.best_layout.addWidget(self.canvas_best)
        self.stats_tabs.addTab(self.best_widget, "Top 3 filmy")

    def update_stats(self):
        self.canvas_ratings.figure = Statistics.plot_ratings_per_movie(self.user)
        self.canvas_ratings.draw()

        self.canvas_genre.figure = Statistics.plot_movies_by_genre(self.user)
        self.canvas_genre.draw()

        self.canvas_status.figure = Statistics.plot_watched_vs_unwatched(self.user)
        self.canvas_status.draw()

        self.canvas_best.figure = Statistics.plot_top_rated_text(self.user)
        self.canvas_best.draw()

        self.load_history()

    def delete_selected_movie(self):
        index = self.movie_list.currentRow()
        try:
            if index == -1:
                raise MovieNotSelectedError()
        except MovieNotSelectedError:
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

        with self.sample_file.open("w", encoding="utf-8") as f:
            json.dump(self.sample_movies, f, indent=2, ensure_ascii=False)

        self.sample_comment_edit.clear()
        self.show_sample_movie_details(self.sample_list.item(index))
        QMessageBox.information(self, "Sukces", "Komentarz został dodany.")

    def sort_user_movies(self):
        current = self.sort_combo_user.currentText()

        if current == "Tytuł A-Z":
            self.filtered_movies.sort(key=lambda m: m.title.lower())
        elif current == "Tytuł Z-A":
            self.filtered_movies.sort(key=lambda m: m.title.lower(), reverse=True)
        elif current == "Rok (rosnąco)":
            self.filtered_movies.sort(key=lambda m: m.year)
        elif current == "Rok (malejąco)":
            self.filtered_movies.sort(key=lambda m: m.year, reverse=True)
        elif current == "Ocena (rosnąco)":
            self.filtered_movies.sort(key=lambda m: float(m.rating))
        elif current == "Ocena (malejąco)":
            self.filtered_movies.sort(key=lambda m: float(m.rating), reverse=True)

        self.update_movie_list_widget()

    def update_movie_list_widget(self):
        self.movie_list.clear()
        for movie in self.filtered_movies:
            self.movie_list.addItem(f"{movie.title} ({movie.year})")

    def toggle_movie_status(self, link: str) -> None:
        index = self.movie_list.currentRow()
        try:
            if index == -1:
                raise MovieNotSelectedError()
        except MovieNotSelectedError:
            QMessageBox.warning(self, "Błąd", "Najpierw wybierz film z listy.")
            return

        movie = self.user.movies[index]

        if movie.status == "Do obejrzenia":
            movie.status = "Obejrzano"
            movie.watch_date = date.today().isoformat()
        else:
            movie.status = "Do obejrzenia"
            movie.watch_date = ""

        self.user_manager.save_users()
        self.load_user_movies()
        self.show_movie_details(self.movie_list.item(index))
        self.update_stats()


