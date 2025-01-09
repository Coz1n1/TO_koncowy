from .ITaskState import TaskState

class ToDoState(TaskState):
    def move_to_next(self, task):
        from .InProgressState import InProgressState
        task.state = InProgressState()

    def move_to_previous(self, task):
        return

    def get_status(self):
        return "To Do"
