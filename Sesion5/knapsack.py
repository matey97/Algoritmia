'''
Created on 8 nov. 2017

@author: Miguel
'''

from bt_scheme import PartialSolutionWithOptimization, BacktrackingOptSolver



class KnapsackPS(PartialSolutionWithOptimization):
    def __init__(self, decisions, W, V, C): # Quita params y por los que tú consideres
        self.decisions = decisions
        self.W = W
        self.V = V
        self.C = C
        
    def is_solution(self):
        return len(self.decisions) == len(self.W)
    
    def get_solution(self):
        return self.decisions
   
    def successors(self):
        if len(self.decisions) < len(self.W):
            i = len(self.decisions)
            if self.C - self.W[i] >= 0:
                self.C -= self.W[i]
                yield KnapsackPS(self.decisions + (1,), W, V, self.C)
                self.C += self.W[i]
            yield KnapsackPS(self.decisions + (0,), W, V, self.C)
    
    def state(self):
        return (len(self.decisions), self.f())
    
    def f(self):
        return -sum([self.V[i]*self.decisions[i] for i in range(len(self.decisions))])

# Programa principal ------------------------------------------
W = [1,4,2,3]
V = [2,3,4,2]
C = 7
# Mostrar todas las soluciones
# IMPLEMENTAR utilizando KnapsackPS y BacktrackingOptSolver
init_ps = KnapsackPS((), W, V, C)
for solution in BacktrackingOptSolver.solve(init_ps):
    print(solution)
print("\n<TERMINADO>")