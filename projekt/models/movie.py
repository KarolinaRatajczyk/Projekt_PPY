class Movie:
    def __init__(self, title, director, year, genre, status, rating, description):
        if not title:
            raise ValueError("Title is required")
        if not director:
            raise ValueError("Director is required")

        if rating:
            try:
                rating = float(rating)
                if rating < 0 or rating > 10:
                    raise ValueError("Rating must be between 0 and 10")
            except ValueError:
                raise ValueError("Rating must be a number")

        self.title = title
        self.director = director
        self.year = year
        self.genre = genre
        self.status = status
        self.rating = rating
        self.description = description

        def to_dict(self):
            return {
                "title": self.title,
                "director": self.director,
                "year": self.year,
                "genre": self.genre,
                "status": self.status,
                "rating": self.rating,
                "description": self.description,
            }

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