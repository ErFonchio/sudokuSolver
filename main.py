from tkinter import *
from Gui import Gui

FPS = 60
TIME = int(1000/FPS)
WIDTH = 450
HEIGHT = 500

class Main:

    def __init__(self):
        self.tk = Tk()
        self.gui = Gui(self.tk, WIDTH, HEIGHT)

    def world(self):
        '''preprocessing'''
        self.preprocessing()

        '''loop manager for computation and rendering'''
        self.manager_loop()
        
        '''mainloop for tkinter engine'''
        self.tk.mainloop() 

    def manager_loop(self):

        '''gui loop'''
        self.gui.manager_loop()

        '''viene richiamata la funzione manager_loop dopo [TIME] tempo'''
        self.tk.after(TIME, self.manager_loop)
        
    def preprocessing(self):

        listona = []

        # There is at least one number in each entry
        #Each number appears at most once in each row

        #Each numer appears at most once in each column

        #Each number appears at most once in each 3x3 subgrid

        #There is at most one number in each entry

        #Each number appears at least once in each row

        #Each number appears at least once in each column

        #Each number appears at least once in each 3x3 subgrid

if __name__ == "__main__":

    m = Main()
    m.world()