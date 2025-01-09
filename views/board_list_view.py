import tkinter as tk
from tkinter import simpledialog, messagebox
from controllers.board_controller import BoardController
from views.board_view_detail import BoardViewDetail
from utils.task_observer import TaskObserver
import random

class BoardListView:
    def __init__(self, master, user):
        self.master = master
        self.user = user
        self.controller = BoardController()
        self.master.title("DoThings")
        self.master.geometry("1000x700")

        self.label_welcome = tk.Label(master, text=f"Witaj, {self.user.username}!", font=("Arial", 16))
        self.label_welcome.pack(pady=10)

        self.frame_boards = tk.Frame(master)
        self.frame_boards.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.frame_boards, bg="#f0f0f0")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.frame_boards, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.inner_frame = tk.Frame(self.canvas, bg="#f0f0f0")
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        self.button_frame = tk.Frame(master)
        self.button_frame.pack(pady=10)

        if self.user.role == 'admin':
            self.button_create_board = tk.Button(self.button_frame, text="Utwórz Nową Tablicę", command=self.create_board, width=20)
            self.button_create_board.pack(side=tk.LEFT, padx=5)

        self.boards = []
        self.board_buttons = []
        self.load_boards()

    def load_boards(self):
        for btn in self.board_buttons:
            btn.destroy()
        self.board_buttons.clear()

        boards = self.controller.get_all_boards()
        self.boards = []
        for board in boards:
            if self.user.role == 'admin' or self.user.username in board.members:
                self.boards.append(board)

        for board in self.boards:
            btn = tk.Button(self.inner_frame,text=board.name,bg=self.get_random_color(),fg="white",font=("Arial", 12, "bold"),width=20,height=5,wraplength=150,command=lambda b=board: self.open_board(b))
            self.board_buttons.append(btn)

        self.arrange_boards()

    def arrange_boards(self):
        for btn in self.board_buttons:
            btn.grid_forget()

        frame_width = self.canvas.winfo_width()
        if frame_width == 1:
            frame_width = self.master.winfo_width()

        btn_width = 180
        num_cols = max(1, frame_width // btn_width)

        for index, btn in enumerate(self.board_buttons):
            row = index // num_cols
            col = index % num_cols
            btn.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

        for col in range(num_cols):
            self.inner_frame.grid_columnconfigure(col, weight=1)

    def get_random_color(self):
        return "#{:06x}".format(random.randint(0, 0xFFFFFF))

    def create_board(self):
        board_name = simpledialog.askstring("Nowa Tablica", "Podaj nazwę nowej tablicy:")
        if board_name:
            try:
                board = self.controller.create_board(board_name, self.user.username)
                messagebox.showinfo("Sukces", f"Utworzono tablicę: '{board.name}'")
                self.load_boards()
            except Exception as e:
                messagebox.showerror("Błąd", str(e))

    def open_board(self, board):
        self.master.destroy()
        root = tk.Tk()
        root.geometry("1000x700")
        app = BoardViewDetail(root, self.user, board)
        root.mainloop()