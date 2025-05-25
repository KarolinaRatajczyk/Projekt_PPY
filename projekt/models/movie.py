import uuid
from datetime import date

class Movie:
    def __init__(self, title, director, year, genre, status, rating, description, watch_date=None):
        if not title:
            raise ValueError("Tytuł jest wymagany")
        if not director:
            raise ValueError("Reżyser jest wymagany")

        if rating:
            try:
                rating = float(rating)
                if rating < 0 or rating > 10:
                    raise ValueError("Ocena musi być w zakresie 0-10")
            except ValueError:
                raise ValueError("Ocena musi być liczbą")

        self.id = str(uuid.uuid4())
        self.title = title
        self.director = director
        self.year = year
        self.genre = genre
        self.status = status
        self.rating = rating
        self.description = description
        self.watch_date = watch_date or (str(date.today()) if status == "obejrzany" else "")
        self.comments = []

    def to_dict(self):
        """Zwraca słownikową reprezentację filmu."""
        return {
            "id": self.id,
            "title": self.title,
            "director": self.director,
            "year": self.year,
            "genre": self.genre,
            "status": self.status,
            "rating": self.rating,
            "description": self.description,
            "watch_date": self.watch_date,
            "comments": self.comments
        }

    @classmethod
    def from_dict(cls, data):
        """Tworzy obiekt filmu na podstawie słownika."""
        movie = cls(
            data["title"],
            data.get("director"),
            data.get("year", ""),
            data.get("genre", ""),
            data.get("status", ""),
            data.get("rating", ""),
            data.get("description", ""),
            data.get("watch_date", "")
        )
        movie.id = data["id"]
        movie.comments = data.get("comments", [])
        return movie

    def add_comment(self, user, comment):
        """Dodaje komentarz do filmu."""
        if not user or not comment:
            raise ValueError("Nazwa użytkownika i komentarz nie mogą być puste")
        self.comments.append({"user": user, "comment": comment})

    def __str__(self):
        return f"{self.title} ({self.year}) - {self.genre} - {self.status} - Ocena: {self.rating}/10"
