from matplotlib.figure import Figure

class Statistics:

    @staticmethod
    def plot_ratings_per_movie(user):
        fig = Figure(figsize=(6, 3))
        ax = fig.add_subplot(111)

        watched = [m.rating for m in user.movies if m.status.lower() == "watched" and m.rating is not None]
        labels = [m.title for m in user.movies if m.status.lower() == "watched" and m.rating is not None]

        if watched:
            ax.bar(labels, watched, color='skyblue')
            ax.set_title("Oceny obejrzanych filmów")
            ax.set_ylabel("Ocena")
            ax.set_ylim(0, 10)
            ax.set_xticks(range(len(labels)))
            ax.set_xticklabels(labels, rotation=45, ha='right')
        else:
            ax.text(0.5, 0.5, "Brak ocenionych filmów", ha='center', va='center')

        return fig

    @staticmethod
    def plot_movies_by_genre(user):
        fig = Figure(figsize=(5, 5))
        ax = fig.add_subplot(111)

        genres = {}
        for movie in user.movies:
            genre = movie.genre.strip().lower()
            if genre:
                genres[genre] = genres.get(genre, 0) + 1

        if genres:
            labels = list(genres.keys())
            sizes = list(genres.values())

            ax.pie(
                sizes,
                labels=labels,
                autopct="%1.1f%%",
                startangle=90,
                wedgeprops={'edgecolor': 'black'}
            )
            ax.set_title("Rozkład filmów według gatunku")
            ax.axis("equal")  # Koło zamiast elipsy
        else:
            ax.text(0.5, 0.5, "Brak danych o gatunkach", ha='center', va='center')

        return fig

    @staticmethod
    def plot_average_rating(user):
        fig = Figure(figsize=(4, 3))
        ax = fig.add_subplot(111)

        ratings = [m.rating for m in user.movies if m.rating is not None]
        if ratings:
            avg = sum(ratings) / len(ratings)
            ax.bar(["Średnia"], [avg], color='green')
            ax.set_title("Średnia ocena wszystkich filmów")
            ax.set_ylim(0, 10)
            ax.set_ylabel("Ocena")
        else:
            ax.text(0.5, 0.5, "Brak ocenionych filmów", ha='center', va='center')

        return fig

    @staticmethod
    def plot_top_rated_movie(user):
        fig = Figure(figsize=(5, 3))
        ax = fig.add_subplot(111)

        rated_movies = [m for m in user.movies if m.rating is not None]
        if rated_movies:
            top_movie = max(rated_movies, key=lambda m: m.rating)
            ax.bar([top_movie.title], [top_movie.rating], color='purple')
            ax.set_ylim(0, 10)
            ax.set_title("Najlepiej oceniany film")
            ax.set_ylabel("Ocena")
        else:
            ax.text(0.5, 0.5, "Brak ocenionych filmów", ha='center', va='center')

        return fig