import tkinter as tk
from tkinter import messagebox
from controllers.auth_controller import AuthController
from views.login_view import LoginView

class RegisterView:
    def __init__(self, master):
        self.master = master
        self.controller = AuthController()
        self.master.title("Rejestracja")
        self.master.geometry("400x500")

        self.label_title = tk.Label(master, text="Rejestracja", font=("Arial", 16, "bold"))
        self.label_title.pack(pady=10)

        self.label_username = tk.Label(master, text="Nazwa użytkownika", font=("Arial", 12))
        self.label_username.pack(pady=5)

        self.entry_username = tk.Entry(master, font=("Arial", 12))
        self.entry_username.pack(pady=5)

        self.label_password = tk.Label(master, text="Hasło", font=("Arial", 12))
        self.label_password.pack(pady=5)
        self.entry_password = tk.Entry(master, show="*", font=("Arial", 12))
        self.entry_password.pack(pady=5)

        self.label_role = tk.Label(master, text="Rola", font=("Arial", 12))
        self.label_role.pack(pady=5)
        self.role_var = tk.StringVar()
        self.role_var.set("admin")
        self.option_role = tk.OptionMenu(master, self.role_var, "admin", "member", command=self.on_role_change)
        self.option_role.config(font=("Arial", 12))
        self.option_role.pack(pady=5)

        self.valid_specializations = ["Programista", "Designer", "Project Manager"]

        self.frame_specialization = tk.Frame(master)
        self.frame_specialization.pack(pady=5)

        self.specialization_var = tk.StringVar()
        self.specialization_var.set("Wybierz specjalizację")

        self.option_specialization = tk.OptionMenu(self.frame_specialization,self.specialization_var,"Wybierz specjalizację",*self.valid_specializations)
        self.option_specialization.config(font=("Arial", 12), width=20)
        self.option_specialization.pack(side=tk.LEFT, padx=5)

        self.update_specialization_visibility()

        self.button_register = tk.Button(master, text="Zarejestruj", command=self.register, font=("Arial", 12), width=20)
        self.button_register.pack(pady=20)

    def on_role_change(self, selected_role):
        self.update_specialization_visibility()

    def update_specialization_visibility(self):
        role = self.role_var.get()
        if role == 'member':
            self.frame_specialization.pack(pady=5)
        else:
            self.frame_specialization.pack_forget()

    def register(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()
        role = self.role_var.get()
        specialization = self.specialization_var.get().strip() if role == 'member' else None

        if not username:
            messagebox.showerror("Błąd", "Wprowadź nazwę użytkownika")
            return
        if not password:
            messagebox.showerror("Błąd", "Wprowadxź hasło")
            return
        if role == 'member':
            if specialization not in self.valid_specializations:
                messagebox.showerror("Błąd", "Wybierz prawidłową specjalizację")
                return

        self.controller.register_user(username, password, role, specialization)
        messagebox.showinfo("Sukces", "Rejestracja zakończona")
        self.master.destroy()
        root = tk.Tk()
        root.geometry("400x500")
        app = LoginView(root)
        root.mainloop()
