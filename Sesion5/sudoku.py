'''
Created on 8 nov. 2017

@author: Miguel
'''

from bt_scheme import PartialSolution, BacktrackingSolver
from algoritmia.utils import argmin

def pos_huecos(mat):
    lista_huecos = []
    for fila in range(len(mat)):
        for col in range(len(mat[0])):
            if mat[fila][col] == 0:
                lista_huecos.append([fila,col])
    return lista_huecos

def primera_libre(mat): 
    for fila in range(9):
        for col in range(9):
            if mat[fila][col] == 0:
                return (fila,col)
    return None
            
def posibles_en(mat, fila, col): 
    used = set(mat[fila][c] for c in range(9))
    used = used.union(mat[f][col] for f in range(9))
    fc, cc = fila//3*3, col//3*3
    used = used.union(mat[fc+f][cc+c] for f in range(3) for c in range(3))
    return set(range(1,10)) - used

def prettyPrint(mat):
    for i, fila in enumerate(mat):
        for j, columna in enumerate(fila):
            print(columna if columna != 0 else ' ', end= "")
            if j in [2, 5]:
                print ("|", end="")
        print()
        if i in [2, 5]:
            print ("---+---+---")
            
class SudokuPS(PartialSolution):
    def __init__(self, matriz_sudoku, pos_huecos):
        self.mat = matriz_sudoku
        self.pos_huecos = pos_huecos
    
    # Indica si la sol. parcial es ya una solución factible (completa)
    def is_solution(self):
        # IMPLEMENTAR
        return primera_libre(self.mat) == None
    
    # Si es sol. factible, la devuelve. Sino lanza excepcion
    def get_solution(self):
        # IMPLEMENTAR
        return self.mat
   
    # Devuelve la lista de sus sol. parciales sucesoras
    def successors(self):
        # IMPLEMENTAR
        '''
        if primera_libre(self.mat) != None: 
            f,c = primera_libre(self.mat)
            posibles = posibles_en(self.mat, f, c)
            for posible_valor in posibles:
                mat_aux = [row[:] for row in self.mat]
                mat_aux[f][c] = posible_valor
                yield SudokuPS(mat_aux)
        '''
        if len(self.pos_huecos) != 0:
            f, c = argmin(self.pos_huecos, lambda x : len(posibles_en(self.mat, x[0], x[1])))
            posibles = posibles_en(self.mat, f, c) 
            self.pos_huecos.remove([f,c])
            for posible_valor in posibles:
                self.mat[f][c] = posible_valor
                yield SudokuPS(self.mat, self.pos_huecos)
            self.pos_huecos.append([f,c])
            self.mat[f][c] = 0
        
    

# PROGRAMA PRINCIPAL -------------------------------------------------------  
#matriz_sudoku = [[0,0,0,3,1,6,0,5,9],[0,0,6,0,0,0,8,0,7],[0,0,0,0,0,0,2,0,0],
#                [0,5,0,0,3,0,0,9,0],[7,9,0,6,0,2,0,1,8],[0,1,0,0,8,0,0,4,0],
#                [0,0,8,0,0,0,0,0,0],[3,0,9,0,0,0,6,0,0],[5,6,0,8,4,7,0,0,0]]
 
## El sudoku más difícil del mundo 
matriz_sudoku = [[8,0,0,0,0,0,0,0,0],[0,0,3,6,0,0,0,0,0],[0,7,0,0,9,0,2,0,0],    
                 [0,5,0,0,0,7,0,0,0],[0,0,0,0,4,5,7,0,0],[0,0,0,1,0,0,0,3,0],    
                 [0,0,1,0,0,0,0,6,8],[0,0,8,5,0,0,0,1,0],[0,9,0,0,0,0,4,0,0]]
 
print("Original:")
prettyPrint(matriz_sudoku)
print("\nSoluciones:")
## Mostrar todas las soluciones
# IMPLEMENTAR utilizando SudokuPS y BacktrackingSolver
lista_huecos = pos_huecos(matriz_sudoku)
initial_sudoku = SudokuPS(matriz_sudoku, lista_huecos)
for solution in BacktrackingSolver.solve(initial_sudoku):
    prettyPrint(solution)
print("<TERMINDADO>") # Espera a ver este mensaje para saber que el programa ha terminado