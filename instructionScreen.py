import tkinter as tk

import statScreen
from tkinterUtils import Field
import foxSim



class InstructionScreen:
    def __init__(self, userID):
        self.root = tk.Tk()
        self.root.geometry("600x500")
        self.root.config(bg="#3f0073")
        self.root.title("Instructions")
        self.userID = userID

        titleText = Field(50, 25, 500, 50, "Simulation Instructions")
        titleText.createLabel(self.root)

        self.textPanel = Field(50, 125, 250, 350, "Click on the buttons to find out more about the simulation")
        self.textPanel.createLabel(self.root)

        descriptionButton = tk.Button(self.root, width=200, text="Description", command=self.descriptionPanel)
        descriptionButton.place(x=350, y=125, width=200, height=50)

        simulationButton = tk.Button(self.root, width=200, text="Fox/Rabbit Sim", command=self.foxSim)
        simulationButton.place(x=350, y=200, width=200, height=50)

        simulationButton = tk.Button(self.root, width=200, text="Wolf/Deer Sim", command=self.simulationPanel)
        simulationButton.place(x=350, y=275, width=200, height=50)

        simulationButton = tk.Button(self.root, width=200, text="Statistics", command=self.statsScreen)
        simulationButton.place(x=350, y=350, width=200, height=50)

        simulationButton = tk.Button(self.root, width=200, text="Quit", command=self.simulationPanel)
        simulationButton.place(x=350, y=425, width=200, height=50)
        self.root.mainloop()

    def descriptionPanel(self):
        descriptionText = "Description Text"
        self.textPanel.label.config(text=descriptionText)

    def simulationPanel(self):
        simulationText = "Simulation Text"
        self.textPanel.label.config(text=simulationText)

    def foxSim(self):
        self.root.destroy()
        foxSim.game(self.userID)

    def statsScreen(self):
        self.root.destroy()
        statScreen.StatScreen(self.userID)


if __name__ == "__main__":
    InstructionScreen(9999999)