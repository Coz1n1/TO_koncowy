import uuid
from .ITaskState import TaskState
from .ToDoState import ToDoState
from utils.observable import Observable

class Task(Observable):
    def __init__(self, title, description, assigned_users, task_id=None):
        super().__init__()
        self.task_id = task_id if task_id else str(uuid.uuid4())
        self.title = title
        self.description = description
        self.assigned_users = assigned_users
        self.state: TaskState = ToDoState()

    def move_next(self):
        self.notify_observers(f"Task Moved")
        self.state.move_to_next(self)

    def move_previous(self):
        self.notify_observers(f"Task Moved")
        self.state.move_to_previous(self)

    def get_status(self):
        return self.state.get_status()

    def to_dict(self):
        return {
            "task_id": self.task_id,
            "title": self.title,
            "description": self.description,
            "assigned_users": self.assigned_users,
            "status": self.get_status()
        }
    
    def get_color(self):
        status_colors = {
            'To Do': '#007bff',
            'In Progress': '#ffc107',
            'Done': '#28a745',
            'To Fix': '#dc3545'
        }
        return status_colors.get(self.get_status(), '#6c757d')