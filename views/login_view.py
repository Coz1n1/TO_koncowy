import tkinter as tk
from tkinter import messagebox
from controllers.auth_controller import AuthController
from views.board_view_detail import BoardViewDetail
from views.board_list_view import BoardListView

class LoginView:
    def __init__(self, master):
        self.master = master
        self.controller = AuthController()
        self.master.title("Logowanie")
        self.master.geometry("300x300")

        self.label_username = tk.Label(master, text="Nazwa użytkownika")
        self.label_username.pack(pady=5)
        
        self.entry_username = tk.Entry(master)
        self.entry_username.pack(pady=5)

        self.label_password = tk.Label(master, text="Hasło")
        self.label_password.pack(pady=5)
        self.entry_password = tk.Entry(master, show="*")
        self.entry_password.pack(pady=5)

        self.button_login = tk.Button(master, text="Zaloguj", command=self.login)
        self.button_login.pack(pady=20)

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        try:
            user = self.controller.login_user(username, password)
            messagebox.showinfo("Sukces", f"Zalogowano jako {user.role}")
            self.master.destroy()

            root = tk.Tk()
            root.geometry("800x600")
            app = BoardListView(root, user)
            root.mainloop()
        except ValueError as e:
            messagebox.showerror("Błąd", str(e))