
from algoritmia.schemes.divideandconquer import DivideAndConquerSolver
from algoritmia.schemes.divideandconquer import IDivideAndConquerProblem
import sys

class DCCalendario (IDivideAndConquerProblem):
    
    def __init__(self, jugadores, b, e):
        self.jugadores = jugadores
        self.b = b
        self.e = e
        
    def is_simple(self):
        return self.e - self.b == 2 
    
    def trivial_solution(self):
        #Devolvemos participantes y el partido entre ellos
        return ((self.jugadores[self.b], self.jugadores[self.b+1]), ((self.jugadores[self.b], self.jugadores[self.b+1]),))
    
    def divide(self):
        h = (self.b+self.e)//2
        yield DCCalendario(self.jugadores, self.b, h)
        yield DCCalendario(self.jugadores, h, self.e)
    
    def combine(self, solution):
        grupoA, grupoB = solution
        
        sol=[]
        
        #Juntamos los dias de grupoA y grupoB
        #En [0] estan representados los jugadores en una misma tupla 
        #En [!0] se representan los partidos tal que [1]-->dia 1, [2]-->dia 2...     
        
        for i in range(0, len(grupoA)):
            sol.append(grupoA[i]+grupoB[i]) #Sumamos los jugadores y los partidos del mismo dia
                
        #ej. con 8  -->  gA = (('p1', 'p2', 'p3', 'p4'), (('p1', 'p2'), ('p3', 'p4')), (('p1', 'p3'), ('p2', 'p4')), (('p1', 'p4'), ('p2', 'p3')))
        #                gB = (('p5', 'p6', 'p7', 'p8'), (('p5', 'p6'), ('p7', 'p8')), (('p5', 'p7'), ('p6', 'p8')), (('p5', 'p8'), ('p6', 'p7')))
        #                sol = [('p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7', 'p8'), (('p1', 'p2'), ('p3', 'p4'), ('p5', 'p6'), ('p7', 'p8')), (('p1', 'p3'), ('p2', 'p4'), ('p5', 'p7'), ('p6', 'p8')), (('p1', 'p4'), ('p2', 'p3'), ('p5', 'p8'), ('p6', 'p7'))]
        #                                 Tupla de jugadores                                        Partidos del dia 1                                           Partidos del dia 2                                        Partidos del dia 3
        
        #En sol tenemos la primera parte del calendario, con enfrentamientos entre jugadores del mismo grupo
        #Ahora hacemos la segunda parte, haciendo partidos entre jugadores de diferentes grupos
        
        n_dias = (self.e-self.b)//2
        
        for dia in range(1,n_dias+1):
            aux = []
            for i in range(len(grupoA[0])): 
                aux.append((grupoA[0][i], grupoB[0][(i+dia-1)%((self.e-self.b)//2)]))
            sol.append(tuple(aux))
                    
        return tuple(sol)


def crea_vector_jugadores(n):
    v = []
    for i in range(1, n+1):
        v.append("p{0}".format(i))
    return v

def muestra_solucion(solution):
    for day in range(1,len(solution)):
        print('Day {0}:'.format(day))
        for p in solution[day]:
            print("\t",p[0],'vs',p[1])

def main():
    n_jugadores = int(sys.argv[1])
    v_jugadores = crea_vector_jugadores(n_jugadores)
    pr_calendario = DCCalendario(v_jugadores, 0, len(v_jugadores))
    solution = DivideAndConquerSolver().solve(pr_calendario)
    #print(solution)
    muestra_solucion(solution)
    
main()


    