# models/board.py

from models.Task import Task

class Board:
    def __init__(self, board_id, name, members=None):
        self.board_id = board_id
        self.name = name
        self.members = members if members else []
        self.tasks = []

    def add_member(self, username):
        if username not in self.members:
            self.members.append(username)

    def remove_member(self, username):
        if username in self.members:
            self.members.remove(username)
            self.tasks = [task for task in self.tasks if task.assigned_users != username]

    def add_task(self, task):
        self.tasks.append(task)

    def remove_task(self, task_id):
        for task in self.tasks:
            if task.task_id == task_id:
                self.tasks.remove(task)
                return
        raise ValueError("Zadanie nie istnieje.")

    def get_task(self, task_id):
        for task in self.tasks:
            if task.task_id == task_id:
                return task
        return None

    def to_dict(self):
        return {
            "board_id": self.board_id,
            "name": self.name,
            "members": self.members,
            "tasks": [task.to_dict() for task in self.tasks]
        }