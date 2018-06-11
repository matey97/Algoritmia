
import sys
import time
from abc import ABCMeta, abstractmethod

class PartialSolution(metaclass=ABCMeta):
    @abstractmethod
    def is_solution(self)-> "bool":
        pass
    
    @abstractmethod
    def get_solution(self)  -> "solution":
        pass
    
    @abstractmethod
    def successors(self) -> "IEnumerable<PartialSolution>":
        pass     

class BacktrackingSolver(metaclass=ABCMeta):   
    @staticmethod
    def solve(initial_ps : "PartialSolution") -> "IEnumerable<Solution>":
        def bt(ps):
            if ps.is_solution():
                yield ps.get_solution()
            else:
                for new_ps in ps.successors():
                    yield from bt(new_ps)
                    
        yield from bt(initial_ps)

class PartialSolutionWithVisitedControl(PartialSolution):
    @abstractmethod
    def state(self)-> "state": 
        # the returned object must be of an inmutable type  
        pass

class BacktrackingVCSolver(metaclass=ABCMeta):
    @staticmethod   
    def solve(initial_ps : "PartialSolutionWithVisitedControl") -> "IEnumerable<Solution>":           
        def bt(ps):
            seen.add(ps.state())
            if ps.is_solution():
                yield ps.get_solution()
            else:
                for new_ps in ps.successors():
                    state = new_ps.state()
                    if state not in seen:
                        yield from bt(new_ps)
      
        seen = set()
        yield from bt(initial_ps)
        


def loadMatrix(fichero):
    matriz = []
    piezas = 0
    
    with open(fichero) as fich:
        for linea in fich:
            lista=[]
            
            for char in linea:
                if char=='o':
                    piezas+=1
                if char!='\n':
                    lista.append(char)
   
            matriz.append(lista)
    return matriz, piezas

def posiblesMovimientos(matriz):
    for f in range(len(matriz)):
        for c in range(len(matriz[0])):
            if(matriz[f][c]=='o'):
                
                
                
                if c-2>=0 and matriz[f][c-2]=='.' and matriz[f][c-1]=='o': #a izq
                    yield (f,c, f, c-1, f,c-2)
                if f-2>=0 and matriz[f-2][c]=='.' and matriz[f-1][c]=='o':  #a arriba
                    yield (f,c, f-1, c, f-2, c) 
                
   
                if c+2<len(matriz[0]) and matriz[f][c+2]=='.' and matriz[f][c+1]=='o': #a der
                    yield (f,c, f, c+1, f,c+2)
                
                if f+2<len(matriz) and matriz[f+2][c]=='.' and matriz[f+1][c]=='o': #a abajo
                    yield (f,c, f+1, c, f+2,c)

def resolverSolitario(matriz, n_piezas):
    class SolitarioPS(PartialSolutionWithVisitedControl):
        def __init__(self,movimientos):
            self.movimientos = movimientos
            self.n = len(movimientos)
        
        def is_solution(self)->"bool":
            return self.n==n_piezas-1 #Cuando solo queda una pieza
        
        def get_solution(self)->"solution":
            return self.movimientos
        
        def successors(self):
            for movimiento in posiblesMovimientos(matriz):
                #Realiza el movimiento en la matriz
                matriz[movimiento[0]][movimiento[1]]='.'
                matriz[movimiento[2]][movimiento[3]]='.'
                matriz[movimiento[4]][movimiento[5]]='o'
                
                #Indica el movimiento que se realiza, sin tener en cuenta que pieza se ha comido
                movimientoReal= (movimiento[0],movimiento[1],movimiento[4], movimiento[5])
                self.movimientos.append(movimientoReal)

                yield SolitarioPS(self.movimientos)
                self.movimientos.pop()#Si no es una solución buena se quita el movimiento
                
                #Vuelve al estado original la matriz
                matriz[movimiento[0]][movimiento[1]]='o'
                matriz[movimiento[2]][movimiento[3]]='o'
                matriz[movimiento[4]][movimiento[5]]='.'  
                
        def state(self)-> "state": 
            estado=""
            for fila in matriz:
                for elem in fila:
                    if(elem=='o'):
                        estado=estado+str(1)
                    else:
                        estado=estado+str(0)
                    
            return estado
                            
    initialPS = SolitarioPS([])
    return BacktrackingVCSolver.solve(initialPS)

fichero = sys.argv[1]
tablero, piezas = loadMatrix(fichero)

start=time.time()
for solucion in resolverSolitario(tablero, piezas):
    for movimiento in solucion: # Convierte cada tupla de movimiento en un string con espacios
        print(" ".join(map(str, movimiento))) 
        
    break
print(time.time()-start)