from .ITaskState import TaskState

class DoneState(TaskState):
    def move_to_next(self, task):
        from .ToFixState import ToFixState
        task.state = ToFixState()

    def move_to_previous(self, task):
        from .InProgressState import InProgressState
        task.state = InProgressState()

    def get_status(self):
        return "Done"
