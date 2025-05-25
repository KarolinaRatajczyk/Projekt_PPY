import uuid
from datetime import datetime

from projekt.models.movie import Movie


class User:
    def __init__(self, username, password, email=""):

        if not username:
            raise ValueError("Nazwa uzytkownika wymagana")
        if not password:
            raise ValueError("Haslo wymagane")
        if len(password) < 4:
            raise ValueError("Haslo min. 4 znaki")


        self.id = str(uuid.uuid4())
        self.username = username
        self.password = password
        self.email = email
        self.created_at = datetime.now()
        self.last_login = self.created_at
        self.movies = []



    def check_password(self, password):
        # sprawdzamy czy sie zgadza
        return self.password == password

    def update_last_login(self):
        ## last logowanie
        self.last_login = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "email": self.email,
            "created_at": str(self.created_at),
            "last_login": self.last_login,
            "movies": [movie.to_dict() for movie in self.movies]
        }

    @classmethod
    def from_dict(cls, data):
        user = cls.__new__(cls)
        user.id = data["id"]
        user.username = data["username"]
        user.password = data["password"]  # poprawka: `password_hash` nie istnieje
        user.email = data.get("email", "")
        user.created_at = data.get("created_at", "")
        user.last_login = data.get("last_login")
        user.movies = [Movie.from_dict(m) for m in data.get("movies", [])]
        return user