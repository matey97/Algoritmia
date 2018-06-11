from bab_scheme import BabPartialSolution, BabSolver
from algoritmia.datastructures.priorityqueues import MinHeap
from math import ceil
from random import seed, randint, uniform, gauss
from itertools import groupby
from algoritmia.utils import argmin

seed(5)
      
def bin_packing_solver(objects, C):
    class BinPacking_BaB_PS(BabPartialSolution):
        def __init__(self, decisions, container_weights):
            self.decisions = decisions
            self.container_weights = container_weights
            self.n = len(decisions)
            self._opt = self.calc_opt_bound()
            self._pes = self.calc_pes_bound()
        
        # IMPLEMENTAR: Relaja el problema. Trata los objetos que quedan como si fueran un 'liquido'
        def calc_opt_bound(self) -> "int or float":
            
            if len(self.container_weights) == 0: ##Si aun no hemos tomado decision
                return ceil(sum(objects)/C)
            if self.n == len(objects): ##Si estamos en una hoja
                return len(self.container_weights)
            
            peso_objetos_restantes = sum(objects[self.n:])
            obj_peso_min = objects[-1]
            
            for i in range(len(self.container_weights)):
                if self.container_weights[i] + obj_peso_min <= C:
                    peso_objetos_restantes -= C - self.container_weights[i] 
            
            contenedores_necesarios = ceil(peso_objetos_restantes/C)
            
            return len(self.container_weights) + contenedores_necesarios   
        
        # IMPLEMENTAR: Algoritmo voraz. Completa la solución parcial actual con "En el primero en el que quepa"
        def calc_pes_bound(self) -> "int or float":
            pesos_contenedores = list(self.container_weights)
            
            for i in range(self.n, len(objects)):
                for n_contenedor in range(len(pesos_contenedores)):
                    if objects[i] + pesos_contenedores[n_contenedor] <= C:
                        pesos_contenedores[n_contenedor]+=objects[i]
                        break
                else:
                    pesos_contenedores.append(objects[i])
                    
            return len(pesos_contenedores)
                        
    
        def is_solution(self) -> "bool":
            return self.n == len(objects)
        
        def get_solution(self) -> "solution":
            return self.decisions
        
        def successors(self) -> "Iterable<BinPackingPS>":
            if self.n < len(objects):
                object_weight = objects[self.n]
                for num_container, container_weight in enumerate(self.container_weights):
                    if container_weight + object_weight <= C:
                        list_cw = list(self.container_weights) # copia tupla a lista
                        list_cw[num_container] += object_weight
                        yield BinPacking_BaB_PS(self.decisions+(num_container,), tuple(list_cw))
                num_container = len(self.container_weights)
                yield BinPacking_BaB_PS(self.decisions+(num_container,), self.container_weights+(object_weight,))
       
    initial_ps = BinPacking_BaB_PS((),())
    return BabSolver.solveMinimization(initial_ps)

def show_solution_grouped_by_containers(sol):
    print("\nSOLUTION GROUPED BY CONTAINERS (shows the weights of objects in each container):")
    for pos, g in groupby(sorted([o,i] for i,o in enumerate(sol)), lambda e:e[0]):
        print ("\t{}: {}".format(pos, [objects[e[1]] for e in g]))
      
def create_exact_binpacking_problem(num_containers, objects_per_container):
    objects = []
    num_c = num_containers
    num_e_c = objects_per_container
    min_v = 25
    max_v = 35
    C = max_v*num_e_c+0
    for ic in range(num_c):
        s=0
        for ie in range(num_e_c-1):
            o = randint(min_v,max_v)
            objects.append(o)
            s+=o
        objects.append(C-s)
    return C, sorted(objects, reverse=True)  
 
# Programa principal --------------------------------------------------------------------------
      
# Descomenta el problema que quieras resolver:
#C, objects = 10, [6,6,3,3,2,2,2,2,2,2]              # SOLUCIÓN ÓPTIMA: 3 contenedores
#C, objects = create_exact_binpacking_problem(6, 3)  # SOLUCIÓN ÓPTIMA: 6 contenedores
C, objects = create_exact_binpacking_problem(12, 3) # SOLUCIÓN ÓPTIMA: 12 contenedores

print("PROBLEM TO SOLVE:")
print("\tContainer capacity:", C)
print("\tObjects (weights):", objects)

sol = bin_packing_solver(objects, C)

print("\nBEST SOLUTION:")
print("\tB&B solution: {0} containers. Details: {1}".format(max(sol)+1, sol))

show_solution_grouped_by_containers(sol)

