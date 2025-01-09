from abc import ABC,abstractmethod

class User(ABC):
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role

    @abstractmethod
    def get_permissions(self):
        pass

    @abstractmethod
    def to_dict(self):
        pass