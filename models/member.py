from .user import User

class Member(User):
    def __init__(self, username, password, specialization):
        super().__init__(username, password, role='member')
        self.specialization = specialization

    def get_permissions(self):
        return ['assign_task','move_task']
    
    def to_dict(self):
        return {
            "username": self.username,
            "password": self.password,
            "role": self.role,
            "specialization": self.specialization
        }