
from abc import ABCMeta, abstractmethod
import sys
infinity = float("infinity")
sys.setrecursionlimit(10000)   

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
        
## Implementacion
 
def solitario_solver(matriz, piezas):
    class SolitarioPS(PartialSolutionWithVisitedControl):
        
        def __init__(self, decisiones):
            self.decisiones = decisiones
            self.huecos = encuentra_huecos()
            self.piezas_restantes = piezas - len(decisiones)
            
        def is_solution(self)->"bool":
            return self.piezas_restantes == 1
        
        def get_solution(self):
            return self.decisiones
        
        def state(self):
            #Definimos el estado como los huecos del tablero
            estado = []
            for hueco in self.huecos:
                estado.append((hueco[0],hueco[1]))
            return tuple(estado)
                    
        def successors(self):
            if self.piezas_restantes != 1: 
                #Para cada bola que puede moverse y su posicion final...
                for bola_y_donde in bolas_que_pueden_moverse_y_donde():
                    iBola, jBola = bola_y_donde[0]
                    iHueco, jHueco = bola_y_donde[1]
                    iNuevoHueco, jNuevoHueco = posicion_nuevo_hueco(bola_y_donde[0], bola_y_donde[1])  #Calcula la posición de la bola que se salta
                    matriz[iHueco][jHueco] = 'o' ##Donde había un hueco, ahora hay una bola
                    matriz[iBola][jBola] = '.' ##Donde había una bola, ahora hay un hueco
                    matriz[iNuevoHueco][jNuevoHueco] = '.'
                    yield SolitarioPS(self.decisiones+((iBola,jBola,iHueco,jHueco),))
                    matriz[iHueco][jHueco] = '.' ##Restauramos el estado del tablero
                    matriz[iBola][jBola] = 'o' 
                    matriz[iNuevoHueco][jNuevoHueco] = 'o'
      
         
    def encuentra_huecos():  ##Encuentra los huecos ('.') del tablero
        return tuple([(i,j) for j in range(len(matriz[0])) for i in range(len(matriz)) if matriz[i][j] == '.'])         
                    
           
    def bolas_que_pueden_moverse_y_donde(): ##Devuelve lista movimientos posibles (bola, hueco)
        bolas = []
        for i in range(filas):
            for j in range(columnas):
                elem = matriz[i][j]
                if elem == 'o':
                    if j-2 >=0 and matriz[i][j-2] == '.' and matriz[i][j-1] == 'o': ##La bola se mueve a la izquierda
                        bolas.append(((i,j),(i,j-2)))
                    if i-2 >=0 and matriz[i-2][j] == '.' and matriz[i-1][j] == 'o': ##La bola se mueve hacia arriba
                        bolas.append(((i,j),(i-2,j)))
                    if j+2 < columnas and matriz[i][j+2] == '.' and matriz[i][j+1] == 'o': ##La bola se mueve a la derecha
                        bolas.append(((i,j),(i,j+2)))
                    if i+2 < filas and matriz[i+2][j] == '.' and matriz[i+1][j] == 'o': ##La bola se mueve hacia abajo
                        bolas.append(((i,j),(i+2,j)))        
        return bolas
   
    def posicion_nuevo_hueco(bola, hueco): ##Devuelve la posicion de la bola saltada por la bola,que se convertira en un hueco 
        iHueco, jHueco = hueco
        iBola, jBola = bola
        if (iHueco == iBola): #La bola a mover y el hueco estan en la misma fila
            iNuevoHueco = iHueco
            if (jHueco > jBola): #La bola a mover esta a la derecha del hueco
                jNuevoHueco = jHueco - 1
            else:
                jNuevoHueco = jHueco + 1
        else: #La bola a mover y el hueco estan en la misma columna
            jNuevoHueco = jHueco
            if (iHueco > iBola): #La bola a mover esta por arriba del hueco
                iNuevoHueco = iHueco - 1
            else:
                iNuevoHueco = iHueco + 1
        return [iNuevoHueco, jNuevoHueco]
        
    filas = len(matriz)
    columnas = len(matriz[0])
    initial_ps = SolitarioPS(())
    return BacktrackingVCSolver.solve(initial_ps)
        
        
def monta_tablero(fichero):
    mat = []
    piezas = 0
    for linea in open(fichero): 
        fila = []
        for elem in linea:
            if elem != '\n':
                fila.append(elem)
                if elem == 'o':
                    piezas += 1
        mat.append(fila)
    return (mat, piezas)

def main():
    fichero = sys.argv[1]
    mat, piezas = monta_tablero(fichero)
    for solution in solitario_solver(mat, piezas):
        for paso in solution:
            print(paso[0],paso[1],paso[2],paso[3])
        break
    
main()
            
            