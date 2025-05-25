import uuid
from datetime import date

from tomlkit import comment


class Movie:
    def __init__(self, title, director, year, genre, status, rating, description, watch_date=None):
        if not title:
            raise ValueError("Tytul jest wymagany")
        if not director:
            raise ValueError("Autor jest wymagany")

        if rating:
            try:
                rating = float(rating)
                if rating < 0 or rating > 10:
                    raise ValueError("Ocena musi byc od 0-10")
            except ValueError:
                raise ValueError("Ocena musi byc numerem")



        self.id = str(uuid.uuid4())
        self.title = title
        self.director = director
        self.year = year
        self.genre = genre
        self.status = status
        self.rating = float(rating)
        self.description = description
        self.watch_date = watch_date or (str(date.today()) if status == "obejrzany" else "")
        self.comments = []

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "director": self.director,
            "year": self.year,
            "genre": self.genre,
            "status": self.status,
            "rating": self.rating,
            "description": self.description,
            "watch_date": self.watch_date,}

    @classmethod
    def from_dict(cls, data):
            return cls(
                data["title"],
                data.get("director"),
                data.get("year", ""),   #jak nie ma takiej wartości to zwróci pusty string
                data.get("genre", ""),
                data.get("status", ""),
                data.get("rating", ""),
                data.gety("description", "")
            )