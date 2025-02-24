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
        self.DeerField = Field(50, 125, 225, 50, "Enter number of Deer")
        self.WolvesField = Field(50, 200, 225, 50, "Enter number of Wolves")
        self.GridField = Field(50, 275, 225, 50, "Enter grid size")
        self.StepsField = Field(50, 350, 225, 50, "Enter number of Steps")

        titleField.createLabel(self.root)
        self.DeerField.createField(self.root)
        self.WolvesField.createField(self.root)
        self.GridField.createField(self.root)
        self.StepsField.createField(self.root)

        submitButton = tk.Button(self.root, width=50, text="Submit", command=self.submitInput)
        submitButton.place(x=175, y=425, width=250, height=50)

        self.root.mainloop()

    def submitInput(self):
        deer = self.DeerField.getEntry().get()
        wolves = self.WolvesField.getEntry().get()
        gridSize = self.GridField.getEntry().get()
        steps = self.StepsField.getEntry().get()

        if not deer.isnumeric() or not wolves.isnumeric() or not gridSize.isnumeric() or not steps.isnumeric():
            messagebox.showinfo("Invalid Inputs", "Must input numbers")
            return False
        self.deer = abs(int(deer))
        self.wolves = abs(int(wolves))
        self.gridSize = abs(int(gridSize))
        self.steps = abs(int(steps))
        self.root.destroy()
