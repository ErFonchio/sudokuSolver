import tkinter as tk
from tkinter.simpledialog import askstring
from tkmacosx import Button

PIXEL_SIZE = 30
BACKGROUND_COLOR = "grey"
LABEL_COLOR = "#f2cc8f"

class Gui:
    def __init__(self, window, width, height, table):
        self.checkFlag = False
        self.solveFlag = False
        self.modifiedValueFlag = False
        self.root = window
        self.root.maxsize(width, height)
        self.root.name = "Sudoku"
        self.width = width
        self.height = height
        self.secondFrameHeight = 100
        self.mainframe = tk.Frame(self.root, width=self.width, height=self.height-self.secondFrameHeight, background=BACKGROUND_COLOR)
        self.mainframe.pack()
        self.labelList = [[tk.Label(self.mainframe, text='0', background=LABEL_COLOR, ) for i in range(9)] for j in range(9)]
        for i in range(len(self.labelList)):
            for j in range(len(self.labelList[i])):
                self.labelList[i][j].place(x=j*PIXEL_SIZE, y=i*PIXEL_SIZE, width=PIXEL_SIZE-2, height=PIXEL_SIZE-2)
                self.labelList[i][j].bind("<Button-1>", lambda event, x=i, y=j: self.clickLabel(event, x, y))

        self.values = table
        self.secondFrame = tk.Frame(self.root, width=self.width, height=self.secondFrameHeight, background=BACKGROUND_COLOR)
        self.secondFrame.pack()
        self.checkButton = Button(self.secondFrame, text="Check", command=self.checkFn)
        self.checkButton.grid(row=0, column=0)
        self.solveButton = Button(self.secondFrame, text="Solve", command=self.solveFn)
        self.solveButton.grid(row=0, column=1)
    
    def clickLabel(self, event, x, y):
        current_text = event.widget.cget("text")
        new_text = askstring("Modifica testo", f"Inserisci nuovo testo per la cella ({x}, {y}):", initialvalue=current_text)
        if new_text is not None:
            event.widget.config(text=new_text)
            self.values[x][y] = int(new_text)
            self.gui.modifiedValueFlag = True
 
    def checkFn(self):
        self.checkFlag = True

    def solveFn(self):
        self.solveFlag = True

    def changeCheckColor(self, color):
        print("Cambiando col colore", color)
        self.checkButton.config(bg=color)

    def printTable(self, table):
        for i in range(9):
            for j in range(9):
                self.labelList[i][j].config(text=table[i][j])

    def updateValue(self, x, y, value):
        self.labelList[x][y].config(text=value)

    def manager_loop(self):
        #print("manager_loop")
        ...