from exceptions import WrongStatus, NotSuchAnId, EmptyMovieListError
from movie import Movie


class MovieManager:


    def __init__(self):
        self.movies = []  # -> inicjalizujemy pusty array

    def add_movie(self, movie):

        if not isinstance(movie, Movie):
            raise NotSuchAnId(f"Obiekt {movie} musi byc instancja movie")

        if existing_movie := self.find_movie_by_title(movie.title):
            raise NotSuchAnId(f"Movie {movie.title} already exists")

        self.movies.append(movie)
        print(f"Movie {movie.title} added")  ## na razie bez GUI bedziemy testowac na terminalu


    def get_movies(self):
        if not self.movies:
            raise EmptyMovieListError("Movie list is empty. Add some movies first.")

        return self.movies

    def get_movie_by_id(self, id):
        for movie in self.movies:
            if movie.id == id:
                return movie
        raise NotSuchAnId(f"No movie found with ID {id}")
    
    def delete_movie(self, id):
        for movie in self.movies:
            if movie.id == id:
                self.movies.remove(movie)
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

    def update_description(self, id, new_description):
        for movie in self.movies:
            if movie.id == id:
                movie.description = new_description
                return
        raise NotSuchAnId(f"Brak filmu o ID: {id} (próba aktualizacji opisu)")


    def find_movie_by_title(self, title):
        for movie in self.movies:
            if movie.title == title:
                return movie


    def find_movie_by_director(self, director):
        for movie in self.movies:
            if movie.director == director:
                return movie


    def filter_movies_by_genre(self, genre):
        movies = []
        for movie in self.movies:
            if genre in movie.genre:
                movies.append(movie)
        return movies


    def sort_movies_by_rating(self):
        return sorted(self.movies, key=lambda movie: movie.rating, reverse=True) ## DO WYTLUMACZENIA


    def sort_movies_by_title(self):
        return sorted(self.movies, key=lambda movie: movie.title)    ## DO WYTLUMACZENIA


    def get_watched_history(self):
        return [(m.title, m.watch_date) for m in self.movies if m.status == 'watched']

    def set_status(self, id, status):
        valid_statuses = ["watched", "unwatched"]

        if status not in valid_statuses:
            raise WrongStatus(f"Invalid status '{status}'. Must be 'watched' or 'unwatched'")

        for movie in self.movies:
            if movie.id == id:
                movie.status = status
                return

        raise NotSuchAnId(f"No movie found with ID {id}")
