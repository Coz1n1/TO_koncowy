import os
import json

class JSONDataAccess:
    _instance = None
    _file_path = 'data/data.json'

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(JSONDataAccess, cls).__new__(cls)
            cls._instance._load_data()
        return cls._instance
    
    def _load_data(self):
        if not os.path.exists(self._file_path):
            self.data = {"users": [], "boards": []}
            self._save_data()
        else:
            with open(self._file_path, 'r', encoding='utf-8') as file:
                self.data = json.load(file)

    def _save_data(self):
        os.makedirs(os.path.dirname(self._file_path), exist_ok=True)
        with open(self._file_path, 'w', encoding='utf-8') as file:
            json.dump(self.data, file, indent=4, ensure_ascii=False)

    def add_user(self, user_dict):
        self.data["users"].append(user_dict)
        self._save_data()

    def get_user(self, username):
        for user in self.data["users"]:
            if user["username"] == username:
                return user
        return None

    def get_all_users(self):
        return self.data.get("users", [])

    def get_all_boards(self):
        return self.data.get("boards", [])

    def get_board(self, board_id):
        for board in self.data["boards"]:
            if board["board_id"] == board_id:
                return board
        return None

    def add_board(self, board_dict):
        self.data["boards"].append(board_dict)
        self._save_data()

    def update_board(self, updated_board):
        for idx, board in enumerate(self.data["boards"]):
            if board["board_id"] == updated_board["board_id"]:
                self.data["boards"][idx] = updated_board
                self._save_data()
                return

    def add_task_to_board(self, board_id, task_dict):
        board = self.get_board(board_id)
        board["tasks"].append(task_dict)
        self._save_data()

    def update_task_in_board(self, board_id, updated_task):
        board = self.get_board(board_id)
        for idx, task in enumerate(board.get("tasks", [])):
            if task["task_id"] == updated_task["task_id"]:
                board["tasks"][idx] = updated_task
                self._save_data()
                return
    
    def delete_task(self, board_id, task_id):
        board = self.get_board(board_id)
        tasks = board.get('tasks', [])
        for task in tasks:
            if task['task_id'] == task_id:
                tasks.remove(task)
                self._save_data()
                return