import uuid
from datetime import datetime
from typing import List, Dict, Any

from models.movie import Movie

class User:
    def __init__(self, username: str, password: str, email: str = "") -> None:
        if not username:
            raise ValueError("Nazwa uzytkownika wymagana")
        if not password:
            raise ValueError("Haslo wymagane")
        if len(password) < 4:
            raise ValueError("Haslo min. 4 znaki")

        self.id: str = str(uuid.uuid4())
        self.username: str = username
        self.password: str = password
        self.email: str = email
        self.created_at: datetime = datetime.now()
        self.last_login: str = self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        self.movies: List[Movie] = []

    def check_password(self, password: str) -> bool:
        return self.password == password

    def update_last_login(self) -> None:
        self.last_login = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self) -> Dict[str, Any]:
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
    def from_dict(cls, data: Dict[str, Any]) -> "User":
        user = cls.__new__(cls)
        user.id = data["id"]
        user.username = data["username"]
        user.password = data["password"]
        user.email = data.get("email", "")
        user.created_at = data.get("created_at", "")
        user.last_login = data.get("last_login")
        user.movies = [Movie.from_dict(m) for m in data.get("movies", [])]
        return user
