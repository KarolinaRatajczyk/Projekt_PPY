import json
from datetime import date
from typing import List, Optional, Tuple

from exceptions.exceptions import DuplicateMovieError, EmptyMovieListError, NotSuchAnId, WrongStatus
from models.movie import Movie


class MovieManager:
    def __init__(self) -> None:
        self.movies: List[Movie] = []

    def add_movie(self, movie: Movie) -> None:
        for m in self.movies:
            if m.title.lower() == movie.title.lower():
                raise DuplicateMovieError(f"Film '{movie.title}' już istnieje!")

        movie.status = "Do obejrzenia"
        movie.watch_date = None
        self.movies.append(movie)

    def get_movies(self) -> List[Movie]:
        if not self.movies:
            raise EmptyMovieListError("Lista filmow pusta")

        return self.movies

    def get_movie_by_id(self, id: str) -> Movie:
        for movie in self.movies:
            if movie.id == id:
                return movie
        raise NotSuchAnId(f"Brak filmu o id: {id}")

    def delete_movie(self, id: str) -> None:
        for movie in self.movies:
            if movie.id == id:
                self.movies.remove(movie)
                return
        raise NotSuchAnId(f"Nie można usunąć: film o ID {id} nie istnieje")

    def update_title(self, id: str, new_title: str) -> None:
        for movie in self.movies:
            if movie.id == id:
                movie.title = new_title
                return
        raise NotSuchAnId(f"Brak filmu o ID: {id} (próba aktualizacji tytułu)")

    def update_director(self, id: str, new_director: str) -> None:
        for movie in self.movies:
            if movie.id == id:
                movie.director = new_director
                return
        raise NotSuchAnId(f"Brak filmu o ID: {id} (próba aktualizacji reżysera)")

    def update_genre(self, id: str, new_genre: str) -> None:
        for movie in self.movies:
            if movie.id == id:
                movie.genre = new_genre
                return
        raise NotSuchAnId(f"Brak filmu o ID: {id} (próba aktualizacji gatunku)")

    def update_rating(self, id: str, new_rating: float) -> None:
        for movie in self.movies:
            if movie.id == id:
                movie.rating = new_rating
                return
        raise NotSuchAnId(f"Brak filmu o ID: {id} (próba aktualizacji oceny)")

    def update_watch_date(self, id: str, new_watch_date: str) -> None:
        for movie in self.movies:
            if movie.id == id:
                movie.watch_date = new_watch_date
                return
        raise NotSuchAnId(f"Brak filmu o ID: {id} (próba aktualizacji daty obejrzenia)")

    def update_description(self, id: str, new_description: str) -> None:
        for movie in self.movies:
            if movie.id == id:
                movie.description = new_description
                return
        raise NotSuchAnId(f"Brak filmu o ID: {id} (próba aktualizacji opisu)")

    def find_movie_by_title(self, title: str) -> Optional[Movie]:
        for movie in self.movies:
            if movie.title == title:
                return movie
        return None

    def find_movie_by_director(self, director: str) -> Optional[Movie]:
        for movie in self.movies:
            if movie.director == director:
                return movie
        return None

    def filter_movies_by_genre(self, genre: str) -> List[Movie]:
        movies: List[Movie] = []
        for movie in self.movies:
            if genre in movie.genre:
                movies.append(movie)
        return movies

    def add_comment_to_movie(self, title: str, user: str, comment: str) -> None:
        movie = self.find_movie_by_title(title)
        if not movie:
            raise NotSuchAnId("Nie znaleziono filmu o podanym tytule")
        movie.add_comment(user, comment)

    def sort_movies_by_rating(self) -> List[Movie]:
        return sorted(self.movies, key=lambda movie: movie.rating, reverse=True)

    def sort_movies_by_title(self) -> List[Movie]:
        return sorted(self.movies, key=lambda movie: movie.title)

    def get_watched_history(self) -> List[Tuple[str, Optional[str]]]:
        return [(m.title, m.watch_date) for m in self.movies if m.status == 'watched']

    def set_status(self, id: str, status: str) -> None:
        valid_statuses = ["Obejrzano", "Do obejrzenia"]

        if status not in valid_statuses:
            raise WrongStatus(f"Zły status '{status}'. Musi być 'Obejrzano' lub 'Do obejrzenia'")

        for movie in self.movies:
            if movie.id == id:
                if status == "Obejrzano":
                    today = date.today().isoformat()
                    movie.status = f"Obejrzano: {today}"
                    movie.watch_date = today
                else:
                    movie.status = "Do obejrzenia"
                    movie.watch_date = None
                return

        raise NotSuchAnId(f"Brak filmu o id: {id}")

    def display_all_movies(self) -> None:
        if not self.movies:
            print("Brak filmów w kolekcji")
            return
        for movie in self.movies:
            print(movie)
            if movie.comments:
                print("  Komentarze:")
                for c in movie.comments:
                    print(f"    {c['user']}: {c['comment']}")
            print()
