from matplotlib.figure import Figure

class Statistics:

    @staticmethod
    def plot_ratings_per_movie(user):
        fig = Figure(figsize=(6, 4))
        ax = fig.add_subplot(111)

        movies = []
        for m in user.movies:
            if m.status.lower() in ("watched", "obejrzany") and m.rating is not None:
                movies.append(m)

        ratings = []
        labels = []
        for m in movies:
            ratings.append(m.rating)
            labels.append(m.title)

        if ratings:
            bars = ax.bar(labels, ratings, color='skyblue')
            ax.set_title("Oceny obejrzanych filmów")
            ax.set_ylabel("Ocena")
            ax.set_ylim(0, 10)
            ax.set_xticks(range(len(labels)))
            ax.set_xticklabels(labels, rotation=45, ha='right')

            for i in range(len(bars)):
                bar = bars[i]
                rating = ratings[i]
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.2,
                        str(round(rating, 1)), ha='center', fontsize=8)
        else:
            ax.text(0.5, 0.5, "Brak ocenionych filmów", ha='center', va='center')

        fig.tight_layout()
        return fig

    @staticmethod
    def plot_movies_by_genre(user):
        fig = Figure(figsize=(5, 5))
        ax = fig.add_subplot(111)

        genres = {}
        for movie in user.movies:
            genre = movie.genre.strip().capitalize()
            if genre != "":
                if genre in genres:
                    genres[genre] += 1
                else:
                    genres[genre] = 1

        if len(genres) > 0:
            labels = []
            sizes = []
            for key in genres:
                labels.append(key)
                sizes.append(genres[key])

            ax.pie(
                sizes,
                labels=labels,
                autopct="%1.1f%%",
                startangle=90,
                wedgeprops={'edgecolor': 'white'},
                textprops={'fontsize': 9}
            )
            ax.set_title("Rozkład filmów według gatunku")
            ax.axis("equal")
        else:
            ax.text(0.5, 0.5, "Brak danych o gatunkach", ha='center', va='center')

        fig.tight_layout()
        return fig

    @staticmethod
    def plot_average_rating(user):
        fig = Figure(figsize=(4, 3))
        ax = fig.add_subplot(111)

        ratings = []
        for m in user.movies:
            if m.rating is not None:
                ratings.append(m.rating)

        if len(ratings) > 0:
            suma = 0
            for r in ratings:
                suma += r
            avg = suma / len(ratings)

            bar = ax.bar(["Średnia"], [avg], color='green')
            ax.set_title("Średnia ocena filmów")
            ax.set_ylim(0, 10)
            ax.set_ylabel("Ocena")

            ax.bar_label(bar, fmt="%.2f", padding=5, fontsize=10)
        else:
            ax.text(0.5, 0.5, "Brak ocenionych filmów", ha='center', va='center')

        fig.tight_layout()
        return fig

    @staticmethod
    def plot_top_rated_movie(user):
        fig = Figure(figsize=(5, 3))
        ax = fig.add_subplot(111)

        rated_movies = []
        for m in user.movies:
            if m.rating is not None:
                rated_movies.append(m)

        if len(rated_movies) > 0:
            top_movie = rated_movies[0]
            for m in rated_movies:
                if m.rating > top_movie.rating:
                    top_movie = m

            bar = ax.bar([top_movie.title], [top_movie.rating], color='purple')
            ax.set_ylim(0, 10)
            ax.set_title("Najlepiej oceniany film")
            ax.set_ylabel("Ocena")

            ax.bar_label(bar, fmt="%.1f", padding=5, fontsize=10)
            ax.set_xticklabels([top_movie.title], rotation=15, ha='center', fontsize=9)
        else:
            ax.text(0.5, 0.5, "Brak ocenionych filmów", ha='center', va='center')

        fig.tight_layout()
        return fig

    @staticmethod
    def get_average_rating(user):
        ratings = []
        for m in user.movies:
            if m.rating is not None:
                ratings.append(m.rating)

        if len(ratings) > 0:
            suma = 0
            for r in ratings:
                suma += r
            return suma / len(ratings)
        return None

    @staticmethod
    def get_top_rated_movie(user):
        rated_movies = []
        for m in user.movies:
            if m.rating is not None:
                rated_movies.append(m)

        if len(rated_movies) == 0:
            return None

        top_movie = rated_movies[0]
        for m in rated_movies:
            if m.rating > top_movie.rating:
                top_movie = m

        return top_movie
