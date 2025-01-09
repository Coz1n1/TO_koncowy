import tkinter as tk
from views.welcome_view import WelcomeView

def main():
    root = tk.Tk()
    root.geometry("300x200")
    app = WelcomeView(root)
    root.mainloop()

if __name__ == "__main__":
    main()
