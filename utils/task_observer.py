from utils.observable import Observer

class TaskObserver(Observer):
    def __init__(self, board_view_detail=None):
        self.board_view_detail = board_view_detail

    def update(self, message):
        print(f"{message}")
        if self.board_view_detail:
            self.board_view_detail.populate_tasks()
