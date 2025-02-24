import tkinter as tk
from tkinterUtils import Field
from tkinter import messagebox
import math

class InputScreen:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("600x500")
        self.root.config(bg="#3f0073")
        self.root.title("Input")

        titleField = Field(50, 50, 500, 50, "Input details")
        self.RabbitField = Field(50, 125, 225, 50, "Enter number of Rabbits")
        self.FoxesField = Field(50, 200, 225, 50, "Enter number of Foxes")
        self.GridField = Field(50, 275, 225, 50, "Enter grid size")
        self.StepsField = Field(50, 350, 225, 50, "Enter number of Steps")

        titleField.createLabel(self.root)
        self.RabbitField.createField(self.root)
        self.FoxesField.createField(self.root)
        self.GridField.createField(self.root)
        self.StepsField.createField(self.root)

        submitButton = tk.Button(self.root, width=50, text="Submit", command=self.submitInput)
        submitButton.place(x=175, y=425, width=250, height=50)

        self.root.mainloop()

    def submitInput(self):
        rabbits = self.RabbitField.getEntry().get()
        foxes = self.FoxesField.getEntry().get()
        gridSize = self.GridField.getEntry().get()
        steps = self.StepsField.getEntry().get()

        if not rabbits.isnumeric() or not foxes.isnumeric() or not gridSize.isnumeric() or not steps.isnumeric():
            messagebox.showinfo("Invalid Inputs", "Must input numbers")
            return False
        self.rabbits = abs(int(rabbits))
        self.foxes = abs(int(foxes))
        self.gridSize = abs(int(gridSize))
        self.steps = abs(int(steps))
        self.root.destroy()
