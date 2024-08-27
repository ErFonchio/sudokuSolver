import tkinter as tk
from tkinter.simpledialog import askstring

PIXEL_SIZE = 50
BACKGROUND_COLOR = "grey"
LABEL_COLOR = "#f2cc8f"

class Gui:
    def __init__(self, window, width, height):
        self.root = window
        self.root.maxsize(width, height+100)
        self.root.name = "Sudoku"
        self.width = width
        self.height = height
        self.mainframe = tk.Frame(self.root, width=self.width, height=self.height, background=BACKGROUND_COLOR)
        self.mainframe.pack()
        self.labelList = [[tk.Label(self.mainframe, text='0', background=LABEL_COLOR, ) for i in range(9)] for j in range(9)]
        for i in range(len(self.labelList)):
            for j in range(len(self.labelList[i])):
                self.labelList[i][j].place(x=j*PIXEL_SIZE, y=i*PIXEL_SIZE, width=PIXEL_SIZE-2, height=PIXEL_SIZE-2)
                self.labelList[i][j].bind("<Button-1>", lambda event, x=i, y=j: self.clickLabel(event, x, y))

        self.values = [[0 for i in range(9)] for j in range(9)]

    def clickLabel(self, event, x, y):
        current_text = event.widget.cget("text")
        new_text = askstring("Modifica testo", f"Inserisci nuovo testo per la cella ({x}, {y}):", initialvalue=current_text)
        if new_text is not None:
            event.widget.config(text=new_text)
            self.values[x][y] = new_text

    def manager_loop(self):
        #print("manager_loop")
        ...