from data.json_data_access import JSONDataAccess
from utils.password_utils import hash_password, verify_password
from models.user import User
from models.admin import Admin
from models.member import Member

class UserFactory:
    @staticmethod
    def create_user(username,password,role,specialization=None):
        if role=='admin':
            return Admin(username,password)
        elif role=='member':
            return Member(username,password,specialization)
        else:
            raise ValueError("Nieznana rola użytkownika")

class AuthController:
    def __init__(self):
        self.data_access = JSONDataAccess()

    def register_user(self, username, password, role, specialization=None):
        if self.data_access.get_user(username):
            raise ValueError("Użytkownik już istnieje")

        hashed_password = hash_password(password)
        user = UserFactory.create_user(username, hashed_password, role, specialization)

        user_dict = user.to_dict()

        self.data_access.add_user(user_dict)
        return user

    def login_user(self, username, password):
        user_dict = self.data_access.get_user(username)
        if not user_dict:
            raise ValueError("Użytkownik nie istnieje")

        if not verify_password(password, user_dict["password"]):
            raise ValueError("Nieprawidłowe hasło")

        role = user_dict["role"]
        if role == 'admin':
            return Admin(user_dict["username"], user_dict["password"])
        elif role == 'member':
            return Member(user_dict["username"], user_dict["password"], user_dict.get("specialization"))
        else:
            raise ValueError("Nieznana rola użytkownika")