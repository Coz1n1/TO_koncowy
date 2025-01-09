import tkinter as tk
from views.login_view import LoginView
from views.register_view import RegisterView

class WelcomeView:
    def __init__(self, master):
        self.master = master
        self.master.geometry("300x200")

        self.label_welcome = tk.Label(master, text="Witamy w aplikacji DoThings", font=("Arial", 14))
        self.label_welcome.pack(pady=20)

        self.button_login = tk.Button(master, text="Zaloguj się", width=15, command=self.open_login)
        self.button_login.pack(pady=5)

        self.button_register = tk.Button(master, text="Zarejestruj się", width=15, command=self.open_register)
        self.button_register.pack(pady=5)

    def open_login(self):
        self.master.destroy()
        root = tk.Tk()
        app = LoginView(root)
        root.mainloop()

    def open_register(self):
        self.master.destroy()
        root = tk.Tk()
        app = RegisterView(root)
        root.mainloop()
