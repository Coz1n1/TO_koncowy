from .ITaskState import TaskState
from .ToDoState import ToDoState

class InProgressState(TaskState):
    def move_to_next(self, task):
        from .DoneState import DoneState
        task.state = DoneState()

    def move_to_previous(self, task):
        task.state = ToDoState()

    def get_status(self):
        return "In Progress"
