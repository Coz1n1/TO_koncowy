from .user import User

class Admin(User):
    def __init__(self, username, password):
        super().__init__(username, password, role='admin')

    def get_permissions(self):
        return ['create_board','add_user','assign_task','remove_task']
    
    def to_dict(self):
        return {
            "username": self.username,
            "password": self.password,
            "role": self.role
        }