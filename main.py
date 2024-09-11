from tkinter import *
from Gui import Gui
import numpy as np
import time
import random

FPS = 60
TIME = int(1000/FPS)
WIDTH = 405
HEIGHT = 505

class Main:

    def __init__(self):
        self.tk = Tk()
        self.tk.title("Sudoku")
        self.table = [[0 for i in range(9)] for j in range(9)]
        self.solution = [[0 for i in range(9)] for j in range(9)]
        self.gui = Gui(self.tk, WIDTH, HEIGHT, self.table)
        self.samples = []
        self.found = set()
        self.listona = []
        self.alreadyResolved = set()
        self.flagInference = False
        

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
            start = time.time()
            self.DPLL(self.listona, self.found, 3)
            print("Time: ", time.time()-start)
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
        with open("new_difficult_sudoku.csv", "r") as file:
            for line in file:
                self.samples.append(line)
        
        '''inserisco l'esempio corrente e la soluzione in liste separate'''
        sample = self.samples[22].split(",")
        for i in range(9):
            table = []
            solution = []
            for j in range(9):
                table.append(int(sample[0][i*9+j]))
                solution.append(int(sample[1][i*9+j]))
                '''aggiungo ad i numeri trovati quelli già presenti nella tabella'''
                if sample[0][i*9+j] != "0":
                    self.found.add("+"+str(i+1)+str(j+1)+str(int(sample[0][i*9+j])))
                    self.listona.append(["+"+str(i+1)+str(j+1)+str(int(sample[0][i*9+j]))])
            self.table[i] = table
            self.solution[i] = solution

        self.gui.printTable(self.table)

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
        for z in range(1, 10):
            temp = []
            for i in range(0, 3):
                for j in range(0, 3):
                    for x in range(1, 4):
                        for y in range(1, 4):
                            temp.append(str("+")+str(x+i*3)+str(y+j*3)+str(z))
            self.listona.append(temp)
        
        random.shuffle(self.listona)
        
        '''trasformo la lista in set dopo aver trasformato le clausole in tuple'''
        self.listona = {tuple(clause) for clause in self.listona}

    def DPLL(self, copiaListona, copiaFound, count):

        if len(self.alreadyResolved) < 50:
            self.solveWithInference(copiaListona, copiaFound)
        self.pureLiteralElimination()
        UPFlag, copiaListona, copiaFound = self.unitPropagation(copiaListona, copiaFound)
        while UPFlag: #unitPropagation semplifica le clausole
            UPFlag, copiaListona, copiaFound = self.unitPropagation(copiaListona, copiaFound)

        '''termination test'''
        if self.clausolaVuota(copiaListona):
            return "UNSATISFIABLE"
        if len(copiaListona) == 0:
            return copiaFound  

        '''splitting rule'''          
        theChosenOne = list(copiaListona).copy()[0][0]
        found1 = copiaFound.copy()
        found1.add((theChosenOne,))
        lista1Copia = copiaListona.copy()
        lista1Copia.add((theChosenOne,))
        firstDPLLRound = self.DPLL(lista1Copia, found1, count-1)
        if firstDPLLRound != "UNSATISFIABLE":
            return firstDPLLRound
        found2 = copiaFound.copy()
        found2.add((self.oppositeSign(theChosenOne),))
        lista2Copia = copiaListona.copy()
        lista2Copia.add((self.oppositeSign(theChosenOne),))
        return self.DPLL(lista2Copia, found2, count-1)
        


    def oppositeSign(self, literal1):
        if literal1[0] == "+":
            return "-"+literal1[1:]
        return "+"+literal1[1:]

    def clausolaVuota(self, listona):
        for clause in listona:
            if len(clause) == 0:
                return True
        return False

    def applyInference(self, clause1, clause2, literal):
        clause3 = set()
        for literal1 in clause1:
            if literal1[1:] != literal[1:]:
                clause3.add(literal1)
        for literal2 in clause2:
            if literal2[1:] != literal[1:]:
                clause3.add(literal2)
        return tuple(clause3,)

    def solveWithInference(self, copiaListona, copiaFound):
        '''divido le clausole in diverse zone in ordine di importanza (lunghezza):
        d[1] = a
        d[2] = (x, a)
        d[3] = (x, y, a)
        '''

        d = {}
        for i, clause in enumerate(copiaListona):
            if len(clause) not in d:
                d[len(clause)] = []
            d[len(clause)].append(clause)

        if d[2] == None:
            return

        '''quello che voglio fare è dare ad una funzione le combinazioni di clausole
        che voglio in base alle loro lunghezze. Ad esempio, voglio dare tutte le clausole
        di lunghezza binaria e fare inferenza tra loro. Oppure voglio dare le clausole binarie
        assieme a quelle ternarie. L'obiettivo è di coprire le combinazioni che mi danno il prima
        possibile un risultato che posso inserire nel sudoku.'''

        # for i in range(len(d.keys())):
        #     for j in range(i, len(d.keys())):
        #         '''per questa versione uso solo le clausole binarie'''
        #         if i == j and list(d.keys())[i] == 2:
        #             self.solveAux(d[list(d.keys())[i]], d[list(d.keys())[j]], (list(d.keys())[i], list(d.keys())[j]))

        self.solveAux(d[2], d[2], (2, 2))
    
    
    def solveAux(self, firstBlockList, secondBlockList, clauseDimensions):
        '''firstDict == secondDict --> vengono fatte combinazioni all'interno dello stesso dizionario,
        quindi combinazioni con clausole di lunghezza uguale.
        Se firstDict != secondDictla allora voglio fare inferenza tra clausole di lunghezza diversa'''
        if clauseDimensions[0] == clauseDimensions[1]:
            d1 = {}
            for clause in firstBlockList:
                for literal in clause:
                    literal_module = literal[1:]
                    if literal_module not in d1:
                        '''per ogni literal creo due insiemi:
                        - uno per i literal positivi e uno per i negativi
                        - gli insiemi contengono la clausola e il corrispondente literal 
                            grazie al quale farò inferenza'''
                        d1[literal_module] = [set(), set()]
                    if literal[0] == "+":
                        d1[literal_module][0].add(clause)
                    else:
                        d1[literal_module][1].add(clause)

            '''se blockList è composta da clausole binarie cerco le clausole di grado 1 
            ( (!x, a),(x, a) --> (a) )'''
            if clauseDimensions[0] == 2:
                newClauses = set()
                for literal in d1:
                    s1 = d1[literal][0]
                    s2 = d1[literal][1]
                    for first in s1:
                        for second in s2:
                            if len(self.alreadyResolved) > 50:
                                self.listona.union(newClauses) 
                                return
                            check = self.applyInference(first, second, str("-")+literal) # "-" is for padding
                            if check not in self.alreadyResolved:
                                self.alreadyResolved.add(check)
                                '''è stato trovato un letterale'''
                                if len(check) == 1:
                                    self.clauseFound(check)
                                
                                '''generiamo nuove clausole di grado 2'''
                                newClauses.add(tuple(check))

                self.listona = self.listona.union(newClauses) 
        
        else:   #ho a che fare con blocchi di clausole di lunghezze diverse 
            d1 = {}
            d2  = {}
            for clause in firstBlockList: #quelli da 2
                for literal in clause:
                    literal_module = literal[1:]
                    if literal_module not in d1:
                        '''per ogni literal creo due insiemi:
                        - uno per i literal positivi e uno per i negativi
                        - gli insiemi contengono la clausola 
                        con la quale farò inferenza'''
                        d1[literal_module] = [set(), set()]
                    if literal[0] == "+":
                        d1[literal_module][0].add(clause)
                    else:
                        d1[literal_module][1].add(clause)


            for clause in secondBlockList: #quelli da 9
                for literal in clause:
                    literal_module = literal[1:]
                    if literal_module not in d2:
                        '''per ogni literal creo due insiemi:
                        - uno per i literal positivi e uno per i negativi
                        - gli insiemi contengono la clausola e il corrispondente literal 
                            grazie al quale farò inferenza'''
                        d2[literal_module] = [set(), set()]
                    if literal[0] == "+":
                        d2[literal_module][0].add(clause)
                    else:
                        d2[literal_module][1].add(clause)

            '''adesso voglio fare inferenza tra quelli positivi del primo gruppo e negativi del secondo
            e poi quelli negativi del primo e positivi del secondo gruppo. Ovviamente faccio inferenza sulle clausole
            che hanno lo stesso literal.'''

            newClauses = set()

            for literal in d1: #literal == chiave del dizionario
                s1 = d1[literal][0] #literal positivi di d1
                if literal not in d2:
                    continue
                s2 = d2[literal][1] #literal negativi di d2
                
                for first in s1:
                    for second in s2:
                        check = self.applyInference(first, second, str("-")+literal) # "-" is for padding
                        if check not in self.alreadyResolved:
                            self.alreadyResolved.add(check)
                            '''è stato trovato un letterale'''
                            if len(check) == 1:
                                print("Trovato il boss: ", first, second, check)
                                self.clauseFound(check)
                            
                            '''generiamo nuove clausole di grado 2'''
                            newClauses.add(tuple(check))

                s1 = d1[literal][1] #literal positivi di d1
                if literal not in d2:
                    continue
                s2 = d2[literal][0] #literal negativi di d2 
                for first in s1:
                    for second in s2:
                        check = self.applyInference(first, second, str("-")+literal) # "-" is for padding
                        if check not in self.alreadyResolved:
                            self.alreadyResolved.add(check)
                            '''è stato trovato un letterale'''
                            if len(check) == 1:
                                #print("Trovato il boss: ", first, second, check)
                                self.clauseFound(check)
                            
                            '''generiamo nuove clausole di grado 2'''
                            newClauses.add(tuple(check))

            self.listona = self.listona.union(newClauses) 

        
    def unitPropagation(self, copiaListona, copiaFound):
        '''trovo tutte le unit clause'''
        literal_found = None
        for clause in copiaListona:
            if len(clause) == 1: 
                literal_found = clause[0]
                copiaFound.add(literal_found)
                self.clauseFound(clause)
                break
        
        if literal_found == None:
            return False, copiaListona, copiaFound

        temp = list(copiaListona.copy())
        for clause in copiaListona:
            for second_literal in clause:
                if literal_found[1:] == second_literal[1:]:
                    #print("paragonando primo e secondo literal: ", literal_found[0], second_literal[0])
                    if second_literal[0] == literal_found[0]:
                        '''il segno è concorde quindi elimino la clausola'''
                        temp.remove(clause)
                        break
                    elif second_literal[0] != literal_found[0]:
                        '''il segno è discorde quindi elimino il letterale dalla clausola'''
                        newClause =  list(clause)
                        newClause.remove(second_literal)
                        temp[temp.index(clause)] = tuple(newClause)

        return True, set(temp), copiaFound

                
    def clauseFound(self, clause): #aggiorna self.table e notifica la gui di aggiornare la griglia
        '''le clausole sono nel formato [+-]xyz oppure [+-]p[0-9]'''
        if len(clause[0]) == 4 and clause[0][0] == "+": #se è una clausola xyz
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
                self.listona.add(tuple(["+"+key]) if "+" in dict[key] else tuple(["-"+key]))
                '''la unit propagation si occuperà del resto'''

    def check(self, table):
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

    