import numpy as np
import matplotlib.pyplot as plt
import multiprocessing 
import sys
import time        



def taskDPLL(flag, result_queue, lock, counter, samples, start, end):
    for i in range(start, end):

        sample = samples[i].split(",")
        time, sat = preprocessing(flag, sample)
        
        if sat == "UNSATISFIABLE":
            print("UNSATISFIABLE")
            result_queue.put(0)
        else:
            result_queue.put(time)
        
        with lock:
            counter.value += 1
            # Stampa il progresso sovrascrivendo la riga precedente
            print(f"\rTask completati: {counter.value}", end="")
            sys.stdout.flush()  # Assicura che la stampa avvenga immediatamente
    
def preprocessing(flag, sample):
    listona = []
    found = set()

    '''inserisco l'esempio corrente e la soluzione in liste separate'''
    for i in range(9):
        for j in range(9):
            '''aggiungo ad i numeri trovati quelli già presenti nella tabella'''
            if sample[0][i*9+j] != "0":
                listona.append(["+"+str(i+1)+str(j+1)+str(int(sample[0][i*9+j]))])


    # There is at least one number in each entry
    for x in range(1, 10):
        for y in range(1, 10):
            temp = []
            for z in range(1, 10):
                temp.append(str("+")+str(x)+str(y)+str(z))
            listona.append(temp)

    #Each number appears at most once in each row (penso sia ogni colonna in realtà)
    for y in range(1, 10):
        for z in range(1, 10):
            for x in range(1, 9):
                for i in range(x+1, 10):
                    listona.append([str("-")+str(x)+str(y)+str(z), str("-")+str(i)+str(y)+str(z)])
    
    #Each numer appears at most once in each column
    for x in range(1, 10):
        for z in range(1, 10):
            for y in range(1, 9):
                for i in range(y+1, 10):
                    listona.append([str("-")+str(x)+str(y)+str(z), str("-")+str(x)+str(i)+str(z)])

    #Each number appears at most once in each 3x3 subgrid
    for z in range(1, 10):
        for i in range(0, 3):
            for j in range(0, 3):
                for x in range(1, 4):
                    for y in range(1, 4):
                        for k in range(y+1, 4):
                            listona.append([str("-")+str(x+i*3)+str(y+j*3)+str(z), str("-")+str(x+i*3)+str(k+j*3)+str(z)])
                        for k in range(x+1, 4):
                            for l in range(1, 4):
                                listona.append([str("-")+str(x+i*3)+str(y+j*3)+str(z), str("-")+str(k+i*3)+str(l+j*3)+str(z)])

    #There is at most one number in each entry
    for x in range(1, 10):
        for y in range(1, 10):
            for z in range(1, 9):
                for i in range(z+1, 10):
                    listona.append([str("-")+str(x)+str(y)+str(z), str("-")+str(x)+str(y)+str(i)])

    #Each number appears at least once in each row
    for y in range(1, 10):
        for z in range(1, 10):
            temp = []
            for x in range(1, 10):
                temp.append(str("+")+str(x)+str(y)+str(z))
            listona.append(temp)

    #Each number appears at least once in each column
    for x in range(1, 10):
        for z in range(1, 10):
            temp = []
            for y in range(1, 10):
                temp.append(str("+")+str(x)+str(y)+str(z))
            listona.append(temp)

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

    listona.extend(tseytin(dnf)) #ritorna le clausole in cnf
    
    '''trasformo la lista in set dopo aver trasformato le clausole in tuple'''
    listona = {tuple(clause) for clause in listona}

    start = time.time()
    ret = DPLL(listona, found, flag, set(), 3)
    end = time.time()
    return end-start, ret

def DPLL(copiaListona, copiaFound, flagInference, alreadyResolved, countIteration):

    if flagInference and (countIteration > 0):
        copiaListona, alreadyResolved = solveWithInference(copiaListona.copy(), alreadyResolved.copy(), alreadyResolved.copy())

    #print(len(copiaListona))
    
    UPFlag, copiaListona, copiaFound = unitPropagation(copiaListona, copiaFound)
    while UPFlag: #unitPropagation semplifica le clausole
        UPFlag, copiaListona, copiaFound = unitPropagation(copiaListona, copiaFound)

    '''termination test'''
    if clausolaVuota(copiaListona):
        return "UNSATISFIABLE"
    if len(copiaListona) == 0:
        return copiaFound  

    '''splitting rule'''          
    theChosenOne = list(copiaListona).copy()[0][0]
    found1 = copiaFound.copy()
    found1.add((theChosenOne,))
    lista1Copia = copiaListona.copy()
    lista1Copia.add((theChosenOne,))
    firstDPLLRound = DPLL(lista1Copia, found1, flagInference, alreadyResolved, countIteration-1)
    if firstDPLLRound != "UNSATISFIABLE":
        return firstDPLLRound
    found2 = copiaFound.copy()
    found2.add((oppositeSign(theChosenOne),))
    lista2Copia = copiaListona.copy()
    lista2Copia.add((oppositeSign(theChosenOne),))
    return DPLL(lista2Copia, found2, flagInference, alreadyResolved, countIteration-1)
    
def oppositeSign(literal1):
    if literal1[0] == "+":
        return "-"+literal1[1:]
    return "+"+literal1[1:]

def clausolaVuota(listona):
    for clause in listona:
        if len(clause) == 0:
            return True
    return False

def applyInference(clause1, clause2, literal):
    clause3 = set()
    for literal1 in clause1:
        if literal1[1:] != literal[1:]:
            clause3.add(literal1)
    for literal2 in clause2:
        if literal2[1:] != literal[1:]:
            clause3.add(literal2)
    return tuple(clause3,)

# def solveWithInference(copiaListona, alreadyResolved):
    
#     d = {}
#     for clause in copiaListona:
#         if len(clause) not in d:
#             d[len(clause)] = []
#         d[len(clause)].append(clause)

#     if d[2] == None:
#         return
    
#     firstBlockList = d[2]

#     d1 = {}
#     for clause in firstBlockList:
#         for literal in clause:
#             literal_module = literal[1:]
#             if literal_module not in d1:
#                 '''per ogni literal creo due insiemi:
#                 - uno per i literal positivi e uno per i negativi
#                 - gli insiemi contengono la clausola e il corrispondente literal 
#                     grazie al quale farò inferenza'''
#                 d1[literal_module] = [set(), set()]
#             if literal[0] == "+":
#                 d1[literal_module][0].add(clause)
#             else:
#                 d1[literal_module][1].add(clause)

#     newClauses = set()
#     for literal in d1:
#         s1 = d1[literal][0]
#         s2 = d1[literal][1]
#         for first in s1:
#             for second in s2:
#                 check = applyInference(first, second, str("-")+literal) # "-" is for padding
#                 if check not in alreadyResolved:
#                     alreadyResolved.add(check)
#                     newClauses.add(check)
#     print(newClauses)
#     return copiaListona.union(newClauses), alreadyResolved

def solveWithInference(copiaListona, copiaFound, alreadyResolved):
    
    d = {}
    for i, clause in enumerate(copiaListona):
        if len(clause) not in d:
            d[len(clause)] = []
        d[len(clause)].append(clause)

    if d[2] == None:
        return

    return solveAux(d[2], d[2], (2, 2), alreadyResolved, copiaListona)


def solveAux(firstBlockList, secondBlockList, clauseDimensions, alreadyResolved, copiaListona):
    alreadyResolved = alreadyResolved.copy()
    copiaListona = copiaListona.copy()
    '''firstDict == secondDict --> vengono fatte combinazioni all'interno dello stesso dizionario,
    quindi combinazioni con clausole di lunghezza uguale.
    Se firstDict != secondDictla allora voglio fare inferenza tra clausole di lunghezza diversa'''
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

    newClauses = set()
    for literal in d1:
        s1 = d1[literal][0]
        s2 = d1[literal][1]
        for first in s1:
            for second in s2:
                check = applyInference(first, second, str("-")+literal) # "-" is for padding
                if check not in alreadyResolved:
                    alreadyResolved.add(check)
                    newClauses.add(tuple(check))

    return copiaListona.union(newClauses), alreadyResolved


    
def unitPropagation(copiaListona, copiaFound):
    '''trovo tutte le unit clause'''
    literal_found = None
    for clause in copiaListona:
        if len(clause) == 1: 
            literal_found = clause[0]
            copiaFound.add(literal_found)
            break
    
    if literal_found == None:
        return False, copiaListona, copiaFound
    
    # print("Literal found: ", literal_found)

    temp = list(copiaListona.copy())
    for clause in copiaListona:
        for second_literal in clause:
            if literal_found[1:] == second_literal[1:]:
                if second_literal[0] == literal_found[0]:
                    '''il segno è concorde quindi elimino la clausola'''
                    if clause in temp:
                        #print("cercando di rimuovere la clausola: ", clause, "che ha come elemento: ", second_literal)
                        temp.remove(clause)
                        break
                elif second_literal[0] != literal_found[0]:
                    '''il segno è discorde quindi elimino il letterale dalla clausola'''
                    newClause =  list(clause)
                    newClause.remove(second_literal)
                    temp[temp.index(clause)] = tuple(newClause)

    return True, set(temp), copiaFound


'''Da completare. Non necessario al momento. Bisogna solo eliminare i letterali
e aggiungerli alla lista dei trovati'''
def pureLiteralElimination(self):
    dict = {}
    for clause in listona:
        for literal in clause:
            if literal[1:] not in dict:
                '''appendo nel dizionario il segno del literal'''
                dict[literal[1:]] = {literal[:1]}
            else:
                dict[literal[1:]].add(literal[:1])
    for key in dict:
        if len(dict[key]) == 1:
            print("Found pure literal: ", key, dict[key])
    

def tseytin(dnf):
    '''NOTA BENE: in questo caso particolare i literal sono tutti positivi
    quindi quando vengono negati vengono messi automaticamente col segno meno 
    senza eseguire nessun controllo aggiuntivo'''
    cnf = []
    #dummyLiteralClause = []
    for i in range(len(dnf)):
        #dummyLiteralClause.append("-p"+str(i)) #clausole dummy
        temp = dnf[i]
        for j in range(len(temp)):
            cnf.append([temp[j], "-p"+str(i)])
            temp[j] = "-"+temp[j][1:] #nego le clausole
        temp.append("+p"+str(i))
        cnf.append(temp)

    #cnf.append(dummyLiteralClause)

    return cnf
        


if __name__ == "__main__":
    samples = []
    '''inserisco tutti i sample del dataset in una lista'''
    with open("new_difficult_sudoku.csv", "r") as file:
        for line in file:
            samples.append(line)

    timeResults0 = multiprocessing.Queue()
    timeResults1 = multiprocessing.Queue()

    lock = multiprocessing.Lock()
    counter = multiprocessing.Value("i", 0)
    
    #p0 = multiprocessing.Process(target=taskDPLL, args=(0,timeResults0,lock,counter, samples,1,100))
    p1 = multiprocessing.Process(target=taskDPLL, args=(1,timeResults1,lock,counter, samples,1, 2))
    # p2 = multiprocessing.Process(target=taskDPLL, args=(0,timeResults0,lock,counter, samples,100, 200))
    # p3 = multiprocessing.Process(target=taskDPLL, args=(1,timeResults1,lock,counter, samples,100, 200))
    # p4 = multiprocessing.Process(target=taskDPLL, args=(0,timeResults0,lock,counter, samples,200,300))
    # p5 = multiprocessing.Process(target=taskDPLL, args=(1,timeResults1,lock,counter, samples,200,300))
    # p6 = multiprocessing.Process(target=taskDPLL, args=(0,timeResults0,lock,counter, samples,300,400))
    # p7 = multiprocessing.Process(target=taskDPLL, args=(1,timeResults1,lock,counter, samples,300,400))

    #p0.start()
    p1.start()
    # p2.start()
    # p3.start()
    # p4.start()
    # p5.start()
    # p6.start()
    # p7.start()

    # p0.join()
    # p1.join()
    # p2.join()
    # p4.join()
    # p3.join()
    # p5.join()
    # p6.join()
    # p7.join()

    timeResults0 = [timeResults0.get() for i in range(399)]
    timeResults1 = [timeResults1.get() for i in range(399)]
    print()
    print("Tempo impiegato per la risoluzione con inferenza: ", np.mean(timeResults1))
    print("Tempo impiegato per la risoluzione senza inferenza: ", np.mean(timeResults0))


    