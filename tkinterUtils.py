import tkinter as tk


class Field:
    def __init__(self, x, y, width, height, text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.__text = text
        self.label = None
        self.__entry = None

    def updateText(self, newText):
        self.__text = newText

    def createLabel(self, root, col="white", x=None, y=None):
        if x is None:
            x = self.x
        if y is None:
            y = self.y
        self.label = tk.Label(root, width=self.width, text=self.__text, bg=col,wraplength=self.width-10)
        self.label.place(x=x, y=y, width=self.width, height=self.height)

    def createEntry(self, root, col="grey", x=None, y=None, separation=50):
        if x is None:
            x = self.x + self.width + separation
        if y is None:
            y = self.y
        self.__entry = tk.Entry(root, bg=col)
        self.__entry.place(x=x, y=y, width=self.width, height=self.height)

    def createField(self, root, separation=50, col1="white", col2="grey"):
        self.createLabel(root, col1)
        self.createEntry(root, col2, separation=separation)

    def getEntry(self):
        return self.__entry
