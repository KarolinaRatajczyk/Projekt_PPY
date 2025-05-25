from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QListWidget, QPushButton,
    QHBoxLayout, QLineEdit, QTextEdit, QDialog, QMessageBox, QComboBox
)
from PySide6.QtCore import Qt
from projekt.models.movie import Movie
from projekt.exceptions.exceptions import NotSuchAnId
import json

PATH = "C/Users/Mateusz/PycharmProjects/Projekt_PPY/projekt/data/sample_movies.json"
class MainAppWindow(QMainWindow):
    def __init__(self, user, movie_manager):
        super().__init__()
        self.user = user
        self.manager = movie_manager

        # ⬇️ Wczytujemy filmy z JSON tylko tutaj
        self.load_movies_from_file()

        self.setWindowTitle(f"Panel Filmów - Witaj {self.user.username}")
        self.setGeometry(100, 100, 1000, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QHBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.movie_list = QListWidget()
        self.movie_list.itemClicked.connect(self.display_movie_details)
        self.layout.addWidget(self.movie_list)

        self.details_layout = QVBoxLayout()
        self.title_label = QLabel("Tytuł:")
        self.description_label = QLabel("Opis:")
        self.comments_label = QLabel("Komentarze:")
        self.comment_input = QLineEdit()
        self.comment_input.setPlaceholderText("Dodaj komentarz...")
        self.comment_button = QPushButton("Dodaj komentarz")
        self.comment_button.clicked.connect(self.add_comment)

        self.details_layout.addWidget(self.title_label)
        self.details_layout.addWidget(self.description_label)
        self.details_layout.addWidget(self.comments_label)
        self.details_layout.addWidget(self.comment_input)
        self.details_layout.addWidget(self.comment_button)

        self.add_button = QPushButton("Dodaj film")
        self.add_button.clicked.connect(self.show_add_movie_dialog)
        self.details_layout.addWidget(self.add_button)

        self.delete_button = QPushButton("Usuń film")
        self.delete_button.clicked.connect(self.delete_selected_movie)
        self.details_layout.addWidget(self.delete_button)

        self.layout.addLayout(self.details_layout)

        self.selected_movie = None
        self.refresh_movie_list()

    def load_movies_from_file(self):
        try:
            with open(PATH, "r", encoding="utf-8") as file:
                data = json.load(file)
                for movie_dict in data:
                    movie = Movie.from_dict(movie_dict)
                    self.manager.add_movie(movie)
        except Exception as e:
            QMessageBox.critical(self, "Błąd wczytywania", f"Nie udało się wczytać filmów:\n{str(e)}")

    def refresh_movie_list(self):
        self.movie_list.clear()
        try:
            for movie in self.manager.get_movies():
                self.movie_list.addItem(f"{movie.title} ({movie.status})")
        except:
            pass

    def display_movie_details(self, item):
        movie_title = item.text().split(" (")[0]
        movie = self.manager.find_movie_by_title(movie_title)
        if movie:
            self.selected_movie = movie
            self.title_label.setText(f"<b>{movie.title}</b> ({movie.year}) — {movie.genre}")
            self.description_label.setText(f"{movie.description}\nOcena: {movie.rating}/10")
            comments = "\n".join([f"{c['user']}: {c['comment']}" for c in movie.comments])
            self.comments_label.setText(f"<b>Komentarze:</b>\n{comments if comments else 'Brak komentarzy'}")

    def add_comment(self):
        if not self.selected_movie:
            return
        comment_text = self.comment_input.text()
        if comment_text:
            self.manager.add_comment_to_movie(self.selected_movie.title, self.user.username, comment_text)
            self.comment_input.clear()
            self.display_movie_details(self.movie_list.currentItem())

    def delete_selected_movie(self):
        if not self.selected_movie:
            return
        confirm = QMessageBox.question(self, "Potwierdź usunięcie",
                                       f"Czy na pewno chcesz usunąć film: {self.selected_movie.title}?",
                                       QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            try:
                self.manager.delete_movie(self.selected_movie.id)
                self.selected_movie = None
                self.refresh_movie_list()
                self.title_label.setText("")
                self.description_label.setText("")
                self.comments_label.setText("")
            except NotSuchAnId as e:
                QMessageBox.warning(self, "Błąd", str(e))

    def show_add_movie_dialog(self):
        dialog = AddMovieDialog(self.manager, self.user, self)
        if dialog.exec():
            self.refresh_movie_list()


class AddMovieDialog(QDialog):
    def __init__(self, movie_manager, user, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Dodaj nowy film")
        self.manager = movie_manager
        self.user = user

        layout = QVBoxLayout()
        self.title_input = QLineEdit()
        self.director_input = QLineEdit()
        self.year_input = QLineEdit()
        self.genre_input = QLineEdit()
        self.status_input = QComboBox()
        self.status_input.addItems(["obejrzany", "nieobejrzany"])
        self.rating_input = QLineEdit()
        self.description_input = QTextEdit()

        layout.addWidget(QLabel("Tytuł:"))
        layout.addWidget(self.title_input)
        layout.addWidget(QLabel("Reżyser:"))
        layout.addWidget(self.director_input)
        layout.addWidget(QLabel("Rok:"))
        layout.addWidget(self.year_input)
        layout.addWidget(QLabel("Gatunek:"))
        layout.addWidget(self.genre_input)
        layout.addWidget(QLabel("Status:"))
        layout.addWidget(self.status_input)
        layout.addWidget(QLabel("Ocena (0-10):"))
        layout.addWidget(self.rating_input)
        layout.addWidget(QLabel("Opis:"))
        layout.addWidget(self.description_input)

        add_button = QPushButton("Dodaj")
        add_button.clicked.connect(self.add_movie)
        layout.addWidget(add_button)

        self.setLayout(layout)

    def add_movie(self):
        try:
            movie = Movie(
                title=self.title_input.text(),
                director=self.director_input.text(),
                year=self.year_input.text(),
                genre=self.genre_input.text(),
                status=self.status_input.currentText(),
                rating=float(self.rating_input.text()),
                description=self.description_input.toPlainText()
            )
            self.manager.add_movie(movie)
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Błąd", str(e))
