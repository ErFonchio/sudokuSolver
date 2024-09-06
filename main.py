from tkinter import *
from Gui import Gui
import numpy as np

FPS = 60
TIME = int(1000/FPS)
WIDTH = 270
HEIGHT = 370 

class Main:

    def __init__(self):
        self.tk = Tk()
        self.table = [[0 for i in range(9)] for j in range(9)]
        self.solution = [[0 for i in range(9)] for j in range(9)]
        self.gui = Gui(self.tk, WIDTH, HEIGHT, self.table)
        self.samples = []
        self.found = set()
        self.listona = []
        

    def world(self):
        '''preprocessing'''
        self.preprocessing()

        '''loop manager for computation and rendering'''
        self.manager_loop()
        
        '''mainloop for tkinter engine'''
        self.tk.mainloop() 

    def manager_loop(self):

        if self.gui.checkFlag:
            self.check(self.table)
            self.gui.checkFlag = False
        if self.gui.solveFlag:
            self.solve()
            self.gui.solveFlag = False
        elif self.gui.modifiedValueFlag:
            ...
            self.gui.modifiedValueFlag = False

        '''gui loop'''
        self.gui.manager_loop()

        '''viene richiamata la funzione manager_loop dopo [TIME] tempo'''
        self.tk.after(TIME, self.manager_loop)
        
    def preprocessing(self):

        '''inserisco tutti i sample del dataset in una lista'''
        with open("sudoku_dataset.csv", "r") as file:
            for line in file:
                self.samples.append(line)
        
        '''inserisco l'esempio corrente e la soluzione in liste separate'''
        sample = self.samples[1].split(",")
        for i in range(9):
            table = []
            solution = []
            for j in range(9):
                table.append(int(sample[0][i*9+j]))
                solution.append(int(sample[1][i*9+j]))
                '''aggiungo ad i numeri trovati quelli già presenti nella tabella'''
                if sample[0][i*9+j] != "0":
                    self.found.add("+"+str(i+1)+str(j+1)+str(int(sample[0][i*9+j])))
            self.table[i] = table
            self.solution[i] = solution

        self.gui.printTable(self.table)

        self.listona = []

        # There is at least one number in each entry
        for x in range(1, 10):
            for y in range(1, 10):
                temp = []
                for z in range(1, 10):
                    temp.append(str("+")+str(x)+str(y)+str(z))
                self.listona.append(temp)

        #Each number appears at most once in each row (penso sia ogni colonna in realtà)
        for y in range(1, 10):
            for z in range(1, 10):
                for x in range(1, 9):
                    for i in range(x+1, 10):
                        self.listona.append([str("-")+str(x)+str(y)+str(z), str("-")+str(i)+str(y)+str(z)])
        
        #Each numer appears at most once in each column
        for x in range(1, 10):
            for z in range(1, 10):
                for y in range(1, 9):
                    for i in range(y+1, 10):
                        self.listona.append([str("-")+str(x)+str(y)+str(z), str("-")+str(x)+str(i)+str(z)])

        #Each number appears at most once in each 3x3 subgrid
        for z in range(1, 10):
            for i in range(0, 3):
                for j in range(0, 3):
                    for x in range(1, 4):
                        for y in range(1, 4):
                            for k in range(y+1, 4):
                                self.listona.append([str("-")+str(x+i*3)+str(y+j*3)+str(z), str("-")+str(x+i*3)+str(k+j*3)+str(z)])
                            for k in range(x+1, 4):
                                for l in range(1, 4):
                                    self.listona.append([str("-")+str(x+i*3)+str(y+j*3)+str(z), str("-")+str(k+i*3)+str(l+j*3)+str(z)])

        #There is at most one number in each entry
        for x in range(1, 10):
            for y in range(1, 10):
                for z in range(1, 9):
                    for i in range(z+1, 10):
                        self.listona.append([str("-")+str(x)+str(y)+str(z), str("-")+str(x)+str(y)+str(i)])

        #Each number appears at least once in each row
        for y in range(1, 10):
            for z in range(1, 10):
                temp = []
                for x in range(1, 10):
                    temp.append(str("+")+str(x)+str(y)+str(z))
                self.listona.append(temp)

        #Each number appears at least once in each column
        for x in range(1, 10):
            for z in range(1, 10):
                temp = []
                for y in range(1, 10):
                    temp.append(str("+")+str(x)+str(y)+str(z))
                self.listona.append(temp)

        #Each number appears at least once in each 3x3 subgrid
        '''la lista seguente deve essere convertita da dnf a cnf'''
        dnf = []
        for z in range(1, 10):
            temp = []
            for i in range(0, 3):
                for j in range(0, 3):
                    for x in range(1, 4):
                        for y in range(1, 4):
                            temp.append(str("+")+str(x+i*3)+str(y+j*3)+str(z))
            dnf.append(temp)

        self.listona.extend(self.tseytin(dnf)) #fa side-effect su listona

        '''let's filter the listona based on the value already present in the table'''
        self.listona = list(filter(self.filterFn, self.listona))
        '''trasformo la lista in set dopo aver trasformato le clausole in tuple'''
        self.listona = {tuple(clause) for clause in self.listona}

        self.pureLiteralElimination() 
            
        self.unitPropagation()
        
                    

    def solve(self):
        for i in range(len(self.listona)):
            if len(self.listona[i]) == 1:
                print("Found unit clause: ", self.listona[i])
        else:
            print("No unit clause found")


        
    def filterFn(self, clause):
        for i in range(len(clause)):
            if clause[i][1:] in self.found:
                return False
            return True
        
    def unitPropagation(self):
        to_discard = set()
        for clause in self.listona:
            if len(clause) == 1:
                to_discard.add(clause)
                self.clauseFound(clause)
        self.listona = self.listona - to_discard
                
    def clauseFound(self, clause): #aggiorna self.table e notifica la gui di aggiornare la griglia
        '''le clausole sono nel formato [+-]xyz oppure [+-]p[0-9]'''
        print("Clause found: ", clause[0])
        self.found.add(clause[0])
        if len(clause[0]) == 4: #se è una clausola xyz
            x = int(clause[0][1])
            y = int(clause[0][2])
            z = int(clause[0][3])
            self.table[x-1][y-1] = z
            self.gui.updateValue(x-1, y-1, z)



    '''Da completare. Non necessario al momento. Bisogna solo eliminare i letterali
    e aggiungerli alla lista dei trovati'''
    def pureLiteralElimination(self):
        dict = {}
        for clause in self.listona:
            for literal in clause:
                if literal[1:] not in dict:
                    '''appendo nel dizionario il segno del literal'''
                    dict[literal[1:]] = {literal[:1]}
                else:
                    dict[literal[1:]].add(literal[:1])
        for key in dict:
            if len(dict[key]) == 1:
                print("Found pure literal: ", key, dict[key])
        

    def tseytin(self, dnf):
        '''NOTA BENE: in questo caso particolare i literal sono tutti positivi
        quindi quando vengono negati vengono messi automaticamente col segno meno 
        senza eseguire nessun controllo aggiuntivo'''
        cnf = []
        dummyLiteralClause = []
        for i in range(len(dnf)):
            dummyLiteralClause.append("+p"+str(i)) #clausole dummy
            temp = dnf[i]
            for j in range(len(temp)):
                cnf.append([temp[j], "-p"+str(i)])
                temp[j] = "-"+temp[j][1:] #nego le clausole
            temp.append("+p"+str(i))
            cnf.append(temp)

        cnf.append(dummyLiteralClause)

        return cnf
        
            


    def check(self, table):
        print("Checking: ", table)
        array = np.array(table)
        array_t = array.transpose()
        '''ogni riga deve contenere un numero da 1 a 9 senza ripetizioni'''
        '''ogni colonna deve contenere un numero da 1 a 9 senza ripetizioni'''
        for i in range(9):
            row = np.extract(array[i] != 0, array[i])
            col = np.extract(array_t[i] != 0, array_t[i])
            if len(row) != len(set(row)):
                print("Errore in riga", i)
                self.gui.changeCheckColor("red")
                return False
            if len(col) != len(set(col)):
                print("Errore in colonna", i)
                self.gui.changeCheckColor("red")
                return False
            if np.sum(row) > 45:
                print("somma >= 45 in riga", i)
                self.gui.changeCheckColor("red")
                return False
            if np.sum(col) > 45:
                print("somma >= 45 in colonna", i)
                self.gui.changeCheckColor("red")
                return False
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                if np.sum(array[i:i+3, j:j+3]) > 45:
                    print("somma > 45 in subgriglia", i, j)
                    self.gui.changeCheckColor("red")
                    return False
        self.gui.changeCheckColor("green")
        return True


if __name__ == "__main__":

    m = Main()
    m.world()

    