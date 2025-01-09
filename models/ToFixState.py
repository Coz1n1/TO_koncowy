from .ITaskState import TaskState

class ToFixState(TaskState):
    def move_to_next(self, task):
        return

    def move_to_previous(self, task):
        from .DoneState import DoneState
        task.state = DoneState()

    def get_status(self):
        return "To Fix"
