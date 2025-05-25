
import json
import os
from datetime import datetime

from projekt.exceptions.exceptions import UserError, WrongStatus
from projekt.models.user import User


class UserManager:
    def __init__(self, data_file="../data/users.json"):
        self.users = []
        self.current_user = None
        self.data_file = data_file
        self._ensure_data_directory()
        self.load_users()




    def _ensure_data_directory(self):
        ## tworzymy jasona jak go nie ma
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)

    def register_user(self, username, password, email=""):
        # tutaj tworzymy usera
        if not username.strip():
            raise ValueError("Nazwa nie moze byc pusta")



        # sprawdz czy uzytkownik juz istnieje
        if self.find_user_by_username(username):
            raise UserError(f"Uzytkownik {username} juz istnieje")

        user = User(username, password, email)
        self.users.append(user)
        self.save_users()
        print(f"Uzytkownik {username} zarejestrowany")
        return user

    def authenticate_user(self, username, password):


        ## tutaj przypisujemy usera do zalogowanego usera

        user = self.find_user_by_username(username)
        if not user:
            raise UserError(f"Uzytkownik {username} nie znaleziony")

        if not user.check_password(password):
            raise WrongStatus("Zle haslo")

        user.update_last_login()
        self.current_user = user
        self.save_users()
        print(f"Zalogowano, pomyslnie\n")
        print(f"Witaj {username}")
        return user

    def logout(self):
        ## wylogowywanie

        if self.current_user:
            print(f"Wylogowano '{self.current_user.username}'")
            self.current_user = None
        else:
            raise UserError("Brak zalogowanych uzytkownikow")

    def find_user_by_username(self, username):
        #wiadomo znajdujemy po nazwie

        for user in self.users:
            if user.username.lower() == username.lower():
                return user
        return None

    def find_user_by_id(self, user_id):
        # znajdujemy po id

        for user in self.users:
            if user.id == user_id:
                return user
        raise UserError(f"Uzytkownik {user_id} nie znaleziony")

    def get_all_users(self):
        ## dostajemy spis wszystkich



        if not self.users:
            raise UserError("Brak uzytkownikow")
        return self.users





    def delete_user(self, username):

        ## sama nazwa wiadomo co wiadomo kogo


        user = self.find_user_by_username(username)
        if not user:
            raise UserError(f"Uzytkownik {user} nie znaleziony")

        if self.current_user and self.current_user.id == user.id:
            self.current_user = None

        self.users.remove(user)
        self.save_users()
        print(f"Uzytkownik {username} pomyślnie usuniety")

    def change_password(self, username, old_password, new_password):
        # zmien haslo


        user = self.find_user_by_username(username)
        if not user:
            raise UserError(f"Uzytkownik {user} nie znaleziony")

        if not user.check_password(old_password):
            raise UserError(f"Zle haslo")
            # tu damy okienko gui

        user.password_hash = user._hash_password(new_password)
        self.save_users()
        print(f"Haslo zmienione dla uzytkownika {username}\n")
        print(f"Nowe haslo {new_password}")

    def is_logged_in(self):
        ## sprawdz czy zalogowany
        return self.current_user is not None

    def save_users(self):
        try:
            user_data = []
            for user in self.users:
                data = user.to_dict()
                # Zamień datetime na string jeśli istnieją
                if isinstance(data.get("created_at"), datetime):
                    data["created_at"] = data["created_at"].strftime("%Y-%m-%d %H:%M:%S")
                if isinstance(data.get("last_login"), datetime):
                    data["last_login"] = data["last_login"].strftime("%Y-%m-%d %H:%M:%S")
                user_data.append(data)

            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(user_data, f, ensure_ascii=False, indent=2)

        except Exception as e:
            print(f"Nie udalo sie zapisac: {e}")

    def load_users(self):

        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    user_data = json.load(f)
                    self.users = [User.from_dict(data) for data in user_data]
                    print(f"Wpisano {len(self.users)} uzytkownikow")
            else:
                print("Nie znaleziono user.data")
        except Exception as e:
            print(f"error")
            self.users = []