import uuid
from data.json_data_access import JSONDataAccess
from models.Board import Board
from models.Task import Task
from models.ToDoState import ToDoState
from models.DoneState import DoneState
from models.InProgressState import InProgressState
from models.ToDoState import ToDoState
from models.InProgressState import InProgressState
from models.DoneState import DoneState
from models.ToFixState import ToFixState

class BoardController:
    def __init__(self):
        self.data_access = JSONDataAccess()

    def create_board(self, name, creator_username):
        board_id = str(uuid.uuid4())
        board = Board(board_id=board_id, name=name, members=[creator_username])
        board_dict = board.to_dict()
        self.data_access.add_board(board_dict)
        return board

    def get_all_boards(self):
        boards_data = self.data_access.get_all_boards()
        boards = []
        for board_data in boards_data:
            board = Board(
                board_id=board_data["board_id"],
                name=board_data["name"],
                members=board_data["members"]
            )
            for task_data in board_data.get("tasks", []):
                task = Task(
                    title=task_data["title"],
                    description=task_data["description"],
                    assigned_users=task_data["assigned_users"],
                    task_id=task_data["task_id"]
                )

                if task_data["status"] == "To Do":
                    task.state = ToDoState()
                elif task_data["status"] == "In Progress":
                    task.state = InProgressState()
                elif task_data["status"] == "Done":
                    task.state = DoneState()
                elif task_data["status"] == "To Fix":
                    task.state = ToFixState()
                board.add_task(task)
            boards.append(board)
        return boards

    def add_member_to_board(self, board_id, username):
        board_data = self.data_access.get_board(board_id)
        if not board_data:
            raise ValueError("Tablica nie znaleziona")
        if username in board_data["members"]:
            raise ValueError("Użytkownik jest już członkiem tablicy")
        board_data["members"].append(username)
        self.data_access.update_board(board_data)
        return True

    def remove_member_from_board(self, board_id, username):
        board_data = self.data_access.get_board(board_id)
        if not board_data:
            raise ValueError("Tablica nie znaleziona")
        if username not in board_data["members"]:
            raise ValueError("Użytkownik nie jest członkiem tablicy")
        board_data["members"].remove(username)
        board_data["tasks"] = [task for task in board_data.get("tasks", []) if task["assigned_users"] != username]
        self.data_access.update_board(board_data)
        return True

    def create_task(self, board_id, title, description, assigned_users):
        board_data = self.data_access.get_board(board_id)
        if not board_data:
            raise ValueError("Tablica nie znaleziona")
        for user in assigned_users:
            if user not in board_data["members"]:
                raise ValueError(f"Przypisany użytkownik '{user}' nie jest członkiem tablicy")
        task = Task(title=title, description=description, assigned_users=assigned_users)
        task_dict = task.to_dict()
        self.data_access.add_task_to_board(board_id, task_dict)
        return task

    def move_task(self, board_id, task_id, direction):
        board_data = self.data_access.get_board(board_id)

        for task_data in board_data.get("tasks", []):
            if task_data["task_id"] == task_id:
                old_status = task_data["status"]
                if direction == "next":
                    if old_status == "To Do":
                        new_status = "In Progress"
                    elif old_status == "In Progress":
                        new_status = "Done"
                    elif old_status == "Done":
                        new_status = "To Fix"

                elif direction == "previous":
                    if old_status == "To Fix":
                        new_status = "Done"
                    elif old_status == "Done":
                        new_status = "In Progress"
                    elif old_status == "In Progress":
                        new_status = "To Do"

                task_data["status"] = new_status
                self.data_access.update_task_in_board(board_id, task_data)
                return
    
    def delete_task(self, board_id, task_id):
        self.data_access.delete_task(board_id, task_id)