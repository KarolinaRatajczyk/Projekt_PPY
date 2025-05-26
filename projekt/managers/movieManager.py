from datetime import date
from exceptions.exceptions import DuplicateMovieError, EmptyMovieListError, NotSuchAnId, WrongStatus


class MovieManager:

    def __init__(self):
        self.movies = []

    def add_movie(self, movie):
        for m in self.movies:
            if m.title.lower() == movie.title.lower() and m.user == movie.user:
                raise DuplicateMovieError(f"Film '{movie.title}' już istnieje u użytkownika '{movie.user}'!")

        movie.status = "Nieobejrzany"
        movie.watch_date = None
        movie.rating = None
        self.movies.append(movie)

    def get_movies(self):
        if not self.movies:
            raise EmptyMovieListError("Lista filmów pusta")
        return self.movies

    def get_movie_by_id(self, id):
        for movie in self.movies:
            if movie.id == id:
                return movie
        raise NotSuchAnId(f"Brak filmu o id: {id}")

    def delete_movie(self, id):
        for movie in self.movies:
            if movie.id == id:
                self.movies.remove(movie)
                return
        raise NotSuchAnId(f"Nie można usunąć: film o ID {id} nie istnieje")

    def update_title(self, id, new_title):
        for movie in self.movies:
            if movie.id == id:
                movie.title = new_title
                return
        raise NotSuchAnId(f"Brak filmu o ID: {id} (próba aktualizacji tytułu)")

    def update_director(self, id, new_director):
        for movie in self.movies:
            if movie.id == id:
                movie.director = new_director
                return
        raise NotSuchAnId(f"Brak filmu o ID: {id} (próba aktualizacji reżysera)")

    def update_genre(self, id, new_genre):
        for movie in self.movies:
            if movie.id == id:
                movie.genre = new_genre
                return
        raise NotSuchAnId(f"Brak filmu o ID: {id} (próba aktualizacji gatunku)")

    def update_description(self, id, new_description):
        for movie in self.movies:
            if movie.id == id:
                movie.description = new_description
                return
        raise NotSuchAnId(f"Brak filmu o ID: {id} (próba aktualizacji opisu)")

    def update_rating(self, id, new_rating):
        for movie in self.movies:
            if movie.id == id:
                movie.rating = new_rating
                return
        raise NotSuchAnId(f"Brak filmu o ID: {id} (próba aktualizacji oceny)")

    def update_watch_date(self, id, new_watch_date):
        for movie in self.movies:
            if movie.id == id:
                movie.watch_date = new_watch_date
                return
        raise NotSuchAnId(f"Brak filmu o ID: {id} (próba aktualizacji daty obejrzenia)")

    def find_movie_by_title(self, title):
        return [movie for movie in self.movies if movie.title.lower() == title.lower()]

    def find_movie_by_director(self, director):
        return [movie for movie in self.movies if movie.director.lower() == director.lower()]

    def filter_movies_by_genre(self, genre):
        return [movie for movie in self.movies if genre.lower() in movie.genre.lower()]

    def add_comment_to_movie(self, title, user, comment):
        for movie in self.movies:
            if movie.title.lower() == title.lower():
                movie.add_comment(user, comment)
                return
        raise NotSuchAnId("Nie znaleziono filmu o podanym tytule")

    def sort_movies_by_rating(self):
        return sorted(self.movies, key=lambda movie: (movie.rating is not None, movie.rating), reverse=True)

    def sort_movies_by_title(self):
        return sorted(self.movies, key=lambda movie: movie.title)

    def get_watched_history(self):
        return [(m.title, m.watch_date) for m in self.movies if m.status == "Obejrzany"]

    def set_status(self, id, status, rating=None):
        valid_statuses = ["Obejrzany", "Nieobejrzany"]

        if status not in valid_statuses:
            raise WrongStatus(f"Zły status '{status}'. Dozwolone: 'Obejrzany', 'Nieobejrzany'.")

        for movie in self.movies:
            if movie.id == id:
                movie.status = status
                if status == "Obejrzany":
                    movie.watch_date = date.today().isoformat()
                    if rating is None:
                        raise ValueError("Ocena musi być podana przy oznaczeniu filmu jako 'Obejrzany'.")
                    movie.rating = rating
                else:
                    movie.watch_date = None
                    movie.rating = None
                return

        raise NotSuchAnId(f"Brak filmu o id: {id}")

    def display_all_movies(self):
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
