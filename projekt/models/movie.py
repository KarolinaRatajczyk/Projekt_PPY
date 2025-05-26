import uuid
from datetime import date
from typing import List, Dict, Any, Optional, Union

from exceptions.exceptions import InvalidRatingError


class Movie:
    def __init__(
        self,
        title: str,
        director: str,
        year: Union[int, str],
        genre: str,
        status: str,
        rating: Optional[float],
        description: str,
        watch_date: Optional[str] = None
    ) -> None:
        if not title:
            raise ValueError("Tytuł jest wymagany")
        if not director:
            raise ValueError("Reżyser jest wymagany")

        if rating:
            try:
                rating = float(rating)
                if rating < 0 or rating > 10:
                    raise InvalidRatingError("Ocena musi być w zakresie 0-10")
            except ValueError:
                raise ValueError("Ocena musi być liczbą")

        self.id: str = str(uuid.uuid4())
        self.title: str = title
        self.director: str = director
        self.year: Union[int, str] = year
        self.genre: str = genre
        self.status: str = status
        self.rating: Optional[float] = rating
        self.description: str = description
        self.watch_date: str = watch_date or (str(date.today()) if status == "obejrzany" else "")
        self.comments: List[Dict[str, str]] = []

    def to_dict(self) -> Dict[str, Any]:
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
    def from_dict(cls, data: Dict[str, Any]) -> "Movie":
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

    def add_comment(self, user: str, comment: str) -> None:
        if not user or not comment:
            raise ValueError("Nazwa użytkownika i komentarz nie mogą być puste")
        self.comments.append({"user": user, "comment": comment})

    def __str__(self) -> str:
        return f"{self.title} ({self.year}) - {self.genre} - {self.status} - Ocena: {self.rating}/10"
