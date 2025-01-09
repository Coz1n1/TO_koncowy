import tkinter as tk
from tkinter import simpledialog, messagebox
from controllers.board_controller import BoardController
from models.Task import Task
from tkinter import ttk 
from utils.task_observer import TaskObserver

class BoardViewDetail:
    def __init__(self, master, user, board):
        self.master = master
        self.user = user
        self.board = board
        self.controller = BoardController()
        self.master.title(f"Tablica: {self.board.name}")
        self.master.geometry("1200x800")
        self.task_observer = TaskObserver(board_view_detail=self)

        for task in self.board.tasks:
            task.register_observer(self.task_observer)

        self.init_gui()

    def init_gui(self):
        self.label_board = tk.Label(self.master, text=f"Tablica: {self.board.name}\tZalogowany jako: {self.user.username}")
        self.label_board.pack(pady=10)

        self.frame_members = tk.Frame(self.master)
        self.frame_members.pack(pady=5)

        self.label_members = tk.Label(self.frame_members, text="Członkowie Tablicy:")
        self.label_members.pack(side=tk.LEFT, padx=5)

        self.selected_member = tk.StringVar()
        self.combobox_members = ttk.Combobox(self.frame_members,textvariable=self.selected_member,state="readonly",font=("Arial", 12),width=30)
        self.combobox_members.pack(side=tk.LEFT, padx=5)
        self.populate_members_combobox()

        if self.user.role == 'admin':
            self.button_add_member = tk.Button(self.frame_members,text="Dodaj Członka",command=self.add_member,bg="#28a745",fg="white")
            self.button_add_member.pack(side=tk.LEFT, padx=5)
            self.button_remove_member = tk.Button(self.frame_members,text="Usuń Członka",command=self.remove_member,bg="#dc3545",fg="white")
            self.button_remove_member.pack(side=tk.LEFT, padx=5)

        self.frame_columns = tk.Frame(self.master)
        self.frame_columns.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.columns = [
            {'name': 'To Do', 'color': '#007bff'},
            {'name': 'In Progress', 'color': '#ffc107'},
            {'name': 'Done', 'color': '#28a745'},
            {'name': 'To Fix', 'color': '#dc3545'}
        ]
        self.column_frames = {}

        for idx, column in enumerate(self.columns):
            frame = tk.Frame(self.frame_columns, bd=2, relief=tk.RIDGE, bg=column['color'])
            frame.grid(row=0, column=idx, padx=5, sticky="nsew")
            self.frame_columns.grid_columnconfigure(idx, weight=1)

            label = tk.Label(frame,text=column['name'],font=("Arial", 14, "bold"),bg=column['color'],fg="white")
            label.pack(pady=5)

            tasks_frame = tk.Frame(frame, bg=column['color'])
            tasks_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

            scrollbar = tk.Scrollbar(tasks_frame, orient="vertical")
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            canvas = tk.Canvas(tasks_frame,bg=column['color'],yscrollcommand=scrollbar.set,highlightthickness=0)
            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.config(command=canvas.yview)

            inner_tasks_frame = tk.Frame(canvas, bg=column['color'])
            canvas.create_window((0, 0), window=inner_tasks_frame, anchor='nw')

            inner_tasks_frame.bind("<Configure>", lambda event, canvas=canvas: canvas.configure(scrollregion=canvas.bbox("all")))
            canvas.bind("<Configure>", lambda event, frame=inner_tasks_frame: frame.config(width=event.width))

            self.column_frames[column['name']] = inner_tasks_frame

        if self.user.role == 'admin':
            self.button_add_task = tk.Button(self.master,text="Dodaj Zadanie",command=self.open_add_task_form,bg="#28a745",fg="white")
            self.button_add_task.pack(pady=5)

        self.button_refresh = tk.Button(self.master,text="Odśwież",command=self.refresh,bg="#17a2b8",fg="white")
        self.button_refresh.pack(pady=5)

        if self.user.role == 'admin':
            self.button_delete_done = tk.Button(self.master,text="Zalicz zadania",command=self.delete_all_done_tasks,bg="#008000",fg="white")
            self.button_delete_done.pack(pady=5)

        self.populate_tasks()

    def populate_members_combobox(self):
        members = self.board.members.copy()
        self.combobox_members['values'] = members

    def populate_members(self):
        self.populate_members_combobox()

    def add_member(self):
        all_users = self.controller.data_access.get_all_users()
        if all_users is None:
            messagebox.showerror("Błąd", "Nie udało się pobrać listy użytkowników.", parent=self.master)
            return

        available_users = [user['username'] for user in all_users if user['username'] not in self.board.members]

        if not available_users:
            messagebox.showinfo("Informacja", "Nie ma dostępnych użytkowników do dodania.", parent=self.master)
            return

        dialog = tk.Toplevel(self.master)
        dialog.title("Dodaj Członka")
        dialog.geometry("300x400")
        dialog.grab_set()

        label = tk.Label(dialog, text="Wybierz użytkownika do dodania:", font=("Arial", 12))
        label.pack(pady=10)

        listbox = tk.Listbox(dialog, selectmode=tk.SINGLE, font=("Arial", 12))
        listbox.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        for user in available_users:
            listbox.insert(tk.END, user)

        def add_selected_member():
            selected_indices = listbox.curselection()
            if not selected_indices:
                messagebox.showwarning("Uwaga", "Proszę wybrać użytkownika do dodania.", parent=dialog)
                return
            selected_username = listbox.get(selected_indices[0])
            self.controller.add_member_to_board(self.board.board_id, selected_username)
            self.board.add_member(selected_username)
            self.populate_members()
            dialog.destroy()

        btn_add = tk.Button(dialog, text="Dodaj", command=add_selected_member, font=("Arial", 12), bg="#28a745", fg="white")
        btn_add.pack(pady=10)

        btn_cancel = tk.Button(dialog, text="Anuluj", command=dialog.destroy, font=("Arial", 12), bg="#dc3545", fg="white")
        btn_cancel.pack(pady=5)

    def remove_member(self):
        selected_member = self.selected_member.get()
        if not selected_member:
            messagebox.showwarning("Uwaga", "Proszę wybrać członka do usunięcia.", parent=self.master)
            return
        if selected_member == self.user.username and self.user.role == 'admin':
            messagebox.showerror("Błąd", "Nie możesz usunąć siebie z tablicy.", parent=self.master)
            return
        confirm = messagebox.askyesno("Potwierdzenie",f"Czy na pewno chcesz usunąć '{selected_member}' z tablicy?",parent=self.master)
        if not confirm:
            return
        
        self.controller.remove_member_from_board(self.board.board_id, selected_member)
        self.board.remove_member(selected_member)
        self.populate_members()
        self.populate_tasks()

    def delete_all_done_tasks(self):
        done_tasks = [task for task in self.board.tasks if task.get_status() == 'Done']
        if not done_tasks:
            messagebox.showinfo("Informacja", "Nie ma zrobionych zadań.", parent=self.master)
            return

        for task in done_tasks:
            self.controller.delete_task(self.board.board_id, task.task_id)
            self.board.remove_task(task.task_id)

        self.populate_tasks()
        messagebox.showinfo("Sukces", "Wyczyszczono zadania", parent=self.master)

    def populate_tasks(self):
        for column in self.columns:
            frame = self.column_frames[column['name']]
            for widget in frame.winfo_children():
                widget.destroy()

        for task in self.board.tasks:
            if not isinstance(task, Task):
                print(f"Zadanie nie jest instancją Task: {task}")
                continue
            column_name = task.get_status()
            if column_name not in self.column_frames:
                continue
            frame = self.column_frames[column_name]

            task_frame = tk.Frame(frame,bg=task.get_color(),bd=1,relief=tk.RIDGE,padx=5,pady=5)
            task_frame.pack(fill=tk.X, padx=5, pady=5)

            label_title = tk.Label(task_frame,text=f"{task.title}",font=("Arial", 12, "bold"),bg=task.get_color(),fg="white")
            label_title.pack(anchor='w')

            label_description = tk.Label(task_frame,text=task.description,font=("Arial", 10),wraplength=200,justify="left",bg=task.get_color(),fg="white")
            label_description.pack(anchor='w')

            assigned_users_str = ", ".join(task.assigned_users)
            label_users = tk.Label(task_frame,text=f"Przypisani: {assigned_users_str}",font=("Arial", 10, "italic"),bg=task.get_color(),fg="white")
            label_users.pack(anchor='w')

            if self.user.role == 'admin' or self.user.username in task.assigned_users:
                btn_move = tk.Button(task_frame,text="Przesuń Zadanie",command=lambda t=task: self.move_task_dialog(t),font=("Arial", 10),bg="#17a2b8",fg="white")
                btn_move.pack(anchor='e', pady=5)

    def open_add_task_form(self):
        add_task_window = tk.Toplevel(self.master)
        add_task_window.title("Dodaj Nowe Zadanie")
        add_task_window.geometry("400x650")

        label_title = tk.Label(add_task_window, text="Tytuł Zadania:", font=("Arial", 12))
        label_title.pack(pady=10)
        entry_title = tk.Entry(add_task_window, font=("Arial", 12), width=40)
        entry_title.pack(pady=5)

        label_description = tk.Label(add_task_window, text="Opis Zadania:", font=("Arial", 12))
        label_description.pack(pady=10)
        text_description = tk.Text(add_task_window, font=("Arial", 12), width=40, height=5)
        text_description.pack(pady=5)

        label_assigned_users = tk.Label(add_task_window, text="Przypisz do:", font=("Arial", 12))
        label_assigned_users.pack(pady=10)

        listbox_users = tk.Listbox(add_task_window, selectmode=tk.MULTIPLE, font=("Arial", 12), width=30, height=10)
        listbox_users.pack(pady=5)

        for member in self.board.members:
            listbox_users.insert(tk.END, member)

        button_submit = tk.Button(add_task_window,text="Dodaj Zadanie",command=lambda: self.submit_new_task(add_task_window,entry_title.get(),text_description.get("1.0", tk.END).strip(),[listbox_users.get(i) for i in listbox_users.curselection()]),font=("Arial", 12),bg="#28a745",fg="white")
        button_submit.pack(pady=20)

    def submit_new_task(self, window, title, description, assigned_users):
        if not title:
            messagebox.showerror("Błąd", "Tytuł zadania nie może być pusty.", parent=window)
            return
        if not description:
            messagebox.showerror("Błąd", "Opis zadania nie może być pusty.", parent=window)
            return
        if not assigned_users:
            messagebox.showerror("Błąd", "Musisz przypisać zadanie do co najmniej jednego użytkownika.", parent=window)
            return

        try:
            task = self.controller.create_task(board_id=self.board.board_id,title=title,description=description,assigned_users=assigned_users)
            task.register_observer(self.task_observer)

            self.board.add_task(task)
            self.populate_tasks()
            messagebox.showinfo("Sukces", f"Zadanie '{task.title}' zostało dodane.", parent=window)
            window.destroy()
        except Exception as e:
            messagebox.showerror("Błąd", str(e), parent=window)

    def move_task_dialog(self, task):
        status_order = ['To Do', 'In Progress', 'Done', 'To Fix']
        current_index = status_order.index(task.get_status())
        possible_directions = {}
        if current_index > 0:
            possible_directions['previous'] = status_order[current_index - 1]
        if current_index < len(status_order) - 1:
            possible_directions['next'] = status_order[current_index + 1]

        dialog = tk.Toplevel(self.master)
        dialog.title("Przesuń Zadanie")
        dialog.geometry("300x100")
        dialog.grab_set()

        def move(direction):
            if direction == "next":
                task.move_next()
            elif direction == "previous":
                task.move_previous() 
            self.controller.move_task(board_id=self.board.board_id,task_id=task.task_id,direction=direction)
            self.populate_tasks()
            dialog.destroy()
            self.refresh()

        if 'previous' in possible_directions:
            btn_previous = tk.Button(dialog,text="Previous",command=lambda: move('previous'),font=("Arial", 12),bg="#6c757d",fg="white",width=10)
            btn_previous.pack(side=tk.LEFT, padx=20, pady=20)
        else:
            btn_previous = tk.Button(dialog,text="Previous",state=tk.DISABLED,font=("Arial", 12),bg="#6c757d",fg="white",width=10)
            btn_previous.pack(side=tk.LEFT, padx=20, pady=20)

        if 'next' in possible_directions:
            btn_next = tk.Button(dialog,text="Next",command=lambda: move('next'),font=("Arial", 12),bg="#17a2b8",fg="white",width=10)
            btn_next.pack(side=tk.RIGHT, padx=20, pady=20)
        else:
            btn_next = tk.Button(dialog,text="Next",state=tk.DISABLED,font=("Arial", 12),bg="#17a2b8",fg="white",width=10)
            btn_next.pack(side=tk.RIGHT, padx=20, pady=20)

    def refresh(self):
        boards = self.controller.get_all_boards()
        for b in boards:
            if b.board_id == self.board.board_id:
                self.board = b
                for task in self.board.tasks:
                    task.register_observer(self.task_observer)
                break
        self.populate_members()
        self.populate_tasks()