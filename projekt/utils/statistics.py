from typing import Optional, List
from matplotlib.figure import Figure
from collections import Counter
from matplotlib import pyplot as plt

from models.user import User  # zakładam, że masz klasę User i Movie w osobnych plikach
from models.movie import Movie

class Statistics:

    @staticmethod
    def plot_ratings_per_movie(user: User) -> Figure:
        watched: List[Movie] = [m for m in user.movies if m.status.lower() == "obejrzano" and m.rating is not None]
        titles: List[str] = [m.title for m in watched]
        ratings: List[float] = [float(m.rating) for m in watched]

        fig, ax = plt.subplots()
        if titles:
            ax.barh(titles, ratings, color="#4CAF50")
            ax.set_xlabel("Ocena")
            ax.set_title("Oceny obejrzanych filmów")
        else:
            ax.text(0.5, 0.5, "Brak ocenionych obejrzanych filmów", ha="center", va="center", transform=ax.transAxes)
            ax.axis("off")

        plt.close(fig)
        return fig

    @staticmethod
    def plot_movies_by_genre(user: User) -> Figure:
        genres: List[str] = [m.genre for m in user.movies if m.genre]
        count: Counter = Counter(genres)

        fig, ax = plt.subplots()
        if count:
            ax.pie(count.values(), labels=count.keys(), autopct="%1.1f%%", startangle=140)
            ax.set_title("Filmy wg gatunku")
        else:
            ax.text(0.5, 0.5, "Brak danych o gatunkach", ha="center", va="center", transform=ax.transAxes)
            ax.axis("off")
        return fig

    @staticmethod
    def plot_watched_vs_unwatched(user: User) -> Figure:
        watched: int = sum(1 for m in user.movies if m.status.lower() == "obejrzano")
        unwatched: int = sum(1 for m in user.movies if m.status.lower() != "obejrzano")

        fig, ax = plt.subplots()
        ax.bar(["Obejrzane", "Do obejrzenia"], [watched, unwatched], color=["#2196F3", "#FFC107"])
        ax.set_title("Status filmów")
        ax.set_ylabel("Liczba filmów")
        return fig

    @staticmethod
    def plot_top_rated_text(user: User) -> Figure:
        rated: List[Movie] = [m for m in user.movies if m.rating is not None]
        fig, ax = plt.subplots(figsize=(6, 3))

        if rated:
            top_movies = sorted(rated, key=lambda m: float(m.rating), reverse=True)[:3]
            lines = [
                f"{i + 1}. {m.title} ({m.year}) – {m.rating}/10"
                for i, m in enumerate(top_movies)
            ]
            msg = "Top 3 filmy:\n" + "\n".join(lines)
        else:
            msg = "Brak filmów z oceną"

        ax.text(0.5, 0.5, msg, ha="center", va="center", fontsize=12, wrap=True, transform=ax.transAxes)
        ax.axis("off")
        plt.tight_layout()
        plt.close(fig)
        return fig

    @staticmethod
    def get_top_rated_movie(user: User) -> Optional[Movie]:
        rated: List[Movie] = [m for m in user.movies if m.rating is not None]
        if not rated:
            return None
        return max(rated, key=lambda m: float(m.rating))

    @staticmethod
    def get_top_rated_movies_summary(user: User, top_n: int = 3) -> str:
        rated: List[Movie] = [m for m in user.movies if m.rating is not None]
        if not rated:
            return "Brak ocenionych filmów"

        top_movies = sorted(rated, key=lambda m: float(m.rating), reverse=True)[:top_n]

        lines = [f"{i + 1}. {m.title} ({m.year}) – {m.rating}/10" for i, m in enumerate(top_movies)]
        summary = "Top najwyżej oceniane filmy:\n" + "\n".join(lines)
        return summary






