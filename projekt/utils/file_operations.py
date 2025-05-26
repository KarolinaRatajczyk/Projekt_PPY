import json
import csv
from typing import List, Optional, Union

from exceptions.exceptions import WrongFileLoading
from models.movie import Movie


class FileOperations:
    @staticmethod
    def save_to_json(movies: List[Movie], filename: str) -> None:
        try:
            movie_data = []
            for movie in movies:
                movie_data.append(movie.to_dict())

            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(movie_data, f, ensure_ascii=False, indent=2)

        except Exception as e:
            raise WrongFileLoading(f"Błąd podczas zapisywania do JSON: {e}")

    @staticmethod
    def load_from_json(filename: str) -> Union[List[dict], None]:
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data
        except FileNotFoundError:
            raise FileNotFoundError(f"Plik {filename} nie został znaleziony")
        except json.JSONDecodeError as e:
            raise WrongFileLoading(f"Nieprawidłowy format JSON: {e}")

    @staticmethod
    def export_to_csv(movies: List[Movie], filename: str) -> None:
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

    @staticmethod
    def export_to_txt(movies: List[Movie], filename: str) -> None:
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                for movie in movies:
                    f.write(f"Tytuł: {movie.title}\n")
                    f.write(f"Reżyser: {movie.director}\n")
                    f.write(f"Rok: {movie.year}\n")
                    f.write(f"Gatunek: {movie.genre}\n")
                    f.write(f"Status: {movie.status}\n")
                    f.write(f"Ocena: {movie.rating}\n")
                    f.write(f"Opis: {movie.description}\n")
                    f.write(f"Data obejrzenia: {movie.watch_date}\n")
                    f.write("-" * 40 + "\n")
        except Exception as e:
            raise WrongFileLoading(f"Błąd podczas eksportu do TXT: {e}")
