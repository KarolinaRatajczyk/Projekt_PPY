import json
import csv

from exceptions.exceptions import WrongFileLoading


class FileOperations:
    @staticmethod
    def save_to_json(movies, filename):
        try:
            movie_data = []
            for movie in movies:
                movie_data.append(movie.to_dict())

            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(movie_data, f, ensure_ascii=False, indent=2)

        except Exception as e:
            raise WrongFileLoading(f"Błąd podczas zapisywania do JSON: {e}")

    @staticmethod
    def load_from_json(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data
        except FileNotFoundError:
            raise FileNotFoundError(f"Plik {filename} nie został znaleziony")
        except json.JSONDecodeError as e:
            raise WrongFileLoading(f"Nieprawidłowy format JSON: {e}")

    @staticmethod
    def export_to_csv(movies, filename):
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Tytuł', 'Reżyser', 'Rok', 'Gatunek', 'Status', 'Ocena', 'Opis'])

                for movie in movies:
                    writer.writerow([
                        movie.title,
                        movie.director,
                        movie.year,
                        movie.genre,
                        movie.status,
                        movie.rating,
                        movie.description
                    ])

        except Exception as e:
            raise WrongFileLoading(f"Błąd podczas eksportu do CSV: {e}")