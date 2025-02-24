import tkinter as tk
from tkinterUtils import Field
import loginScreen
import registerScreen


class MainMenu:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("400x300")
        self.root.config(bg="#3f0073")
        self.root.title("Menu")

        titleField = Field(50, 50, 300, 50, "What would you like to do")
        titleField.createLabel(self.root)

        loginButton = tk.Button(self.root, width=50, text="Log in", command=self.login)
        loginButton.place(x=75, y=125, width=250, height=50)

        registerButton = tk.Button(self.root, width=50, text="Register", command=self.register)
        registerButton.place(x=75, y=200, width=250, height=50)

        self.root.mainloop()

    def login(self):
        self.root.destroy()
        loginScreen.LoginScreen()

    def register(self):
        registerScreen.RegisterScreen()


menu = MainMenu()
