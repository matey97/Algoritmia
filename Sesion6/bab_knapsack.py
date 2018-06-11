from bab_scheme import BabPartialSolution, BabSolver
from random import randint, seed
                
seed(5)

# IMPORTANTE:
# Para facilitar la implementación y no tener que trabajar con un nivel adicional de índices, 
# asumiremos que los objetos (listas W y V) están ordenados de mayor a menor ratio valor/peso.

def knapsack_bab_solver(W, V, C):
    class KnapSack_BaB_PS(BabPartialSolution):
        __slots__ = ("decisions", "current_weight", "current_value", "n")
        
        def __init__(self, decisions, current_weight, current_value):
            self.decisions = decisions
            self.current_weight = current_weight
            self.current_value = current_value
            self.n = len(decisions)
            self._pes = self.calc_pes_bound()
            self._opt = self.calc_opt_bound()
        
        # IMPLEMENTAR: relajar problema (resolver mochila continua para los objetos que quedan)
        def calc_opt_bound(self) -> "int or float":
            peso_restante = C - self.current_weight
            valor_actual = self.current_value
            
            for i in range(len(V[self.n:])):
                cant = min(1, peso_restante/W[i+self.n])
                peso_restante -= W[i+self.n]*cant
                valor_actual += cant*V[i+self.n]
        
            return valor_actual
            
        # IMPLEMENTAR: utilizar algoritmo voraz (visto en el tema de voraces)
        def calc_pes_bound(self) -> "int or float":
            peso_restante = C - self.current_weight
            valor_actual = self.current_value
            
            for i in range(len(V[self.n:])):
                if peso_restante - W[i+self.n] >= 0:
                    peso_restante -= W[i+self.n]
                    valor_actual += V[i+self.n]
              
            return valor_actual      
        
        def is_solution(self) -> "bool":
            return self.n == len(V)
        
        def get_solution(self) -> "solution":
            return (self.decisions, self.current_weight, self.current_value)
        
        def successors(self) -> "Iterable<KnapSack_BaB_PS>":
            if self.n<len(V):
                if W[self.n] <= C-self.current_weight:
                    yield KnapSack_BaB_PS(self.decisions+(1,), self.current_weight+W[self.n], self.current_value+V[self.n])
                yield KnapSack_BaB_PS(self.decisions+(0,), self.current_weight, self.current_value) 
            
    initial_decisions = ()
    initial_weight = 0
    initial_value = 0
    initial_ps = KnapSack_BaB_PS(initial_decisions, initial_weight, initial_value)
    return BabSolver.solveMaximization(initial_ps)
  
def sorted_by_dec_ratio(Wold, Vold):
    idxs = sorted(range(len(Wold)), key = lambda i : -Vold[i]/Wold[i] )
    Wnew = [Wold[i] for i in idxs]
    Vnew = [Vold[i] for i in idxs]
    return Wnew, Vnew

def create_knapsack_problem(num_objects):
    Wnew = [randint(10,100) for _ in range(num_objects)]
    Vnew = [Wnew[i]*randint(1,4) for i in range(num_objects)]
    C = int(sum(Wnew)*0.3)
    W, V = sorted_by_dec_ratio(Wnew, Vnew)
    return W, V, C

# Program principal ------------------------------------------------------------------------------------

# Tres instacion del problema. Descomenta el que quieras resolver:
W, V, C = [2, 1, 6, 5, 6], [4, 1, 3, 2, 2], 10 # Solution: value = 8, weight = 9, decisions = (1, 1, 1, 0, 0)
W, V, C = create_knapsack_problem(20)          # Solution: value = 1118, weight = 344, decisions = (1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0)
#W, V, C = create_knapsack_problem(35)          # Solution: value = 1830, weight = 543, decisions = (1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

print("PROBLEM:")
print("\tNum. objects:", len(W))
print("\tKnapsack capacity:", C)

print("\nStart B&B...")
solution_decisions, solution_weight, solution_value = knapsack_bab_solver(W, V, C)

print("\tSolution: value = {0}, weight = {1}, decisions = {2}".format(solution_value, solution_weight, solution_decisions)) 
print("...END.")
