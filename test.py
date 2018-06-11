'''
Created on 16 ene. 2018

@author: Miguel
'''
from algoritmia.schemes.decreaseandconquer import IDecreaseAndConquerProblem, DecreaseAndConquerSolver
from algoritmia.utils import infinity


def busca_indice_solitario(v, i, j):
    class Busca_indice_problem(IDecreaseAndConquerProblem): 
        def __init__(self, v, i, j):
            self.v = v
            self.i = i
            self.j = j
        
        def is_simple(self):
            return self.j-1<=self.i
        
        def trivial_solution(self):
            return self.i
        
        def decrease(self):
            h = (self.i+self.j)//2
            if self.v[h] == self.v[h+1] and (j-h)%2==0: return Busca_indice_problem(self.v, self.i, h)
            elif self.v[h] == self.v[h+1] and (j-h)%2!=0: return Busca_indice_problem(self.v, h+1, self.j)
            elif self.v[h] == self.v[h-1] and (j-h)%2!=0: return Busca_indice_problem(self.v, self.i, h)
            elif self.v[h] == self.v[h-1] and (j-h)%2==0: return Busca_indice_problem(self.v, h+1, self.j)
            else: return Busca_indice_problem(self.v, h, h+1)
        
        def process(self, s):
            return s
    
    solver = DecreaseAndConquerSolver()
    return solver.solve(Busca_indice_problem(v, i, j))

v = [1,1,2,2,3,4,4,5,5,6,6,7,7,8,8]
v=[10,10,17,17,18,18,21,21,23]
v=[1,3,3,5,5,7,7,8,8,9,9,10,10]

pos = busca_indice_solitario(v, 0, len(v))
print(pos, v[pos])


def solve(v):
    ini = 0
    fin = len(v)
    while fin-1!=ini:
        med = (ini+fin)//2
        if v[med] < v[med-1] and v[med] < v[med+1]:
            return v[med]
        elif v[med] > v[med-1] and v[med] < v[med+1]:
            fin = med
        else:
            ini = med+1
    return v[ini]
            
v = [5,6,8,6,2,1,6,4,5,6] 
print(solve(v))

def p_dinamica(S,L):
    def M(s,n):
        if n == 0 and s == 0:
            return 1
        if s == 0 and n > 0:
            return -infinity
        if n == 0 and s!=0:
            return -infinity
        maxim = -infinity
        for elem in L[n-1]:
            maxim = max(maxim, M(s-elem, n-1)*elem)
        return maxim
    
    return M(S, len(L))       

            
S = 16
L = [[4,2],[10,6],[8,2]]
print(p_dinamica(S, L))


def menor_numero_intervalos(p, a):
    indices_ordenados = sorted(range(len(p)), key=lambda i:p[i])
    n_intervalos = 0
    intervalos = []
    fin = -1
    for i in indices_ordenados:
        if fin ==-1 or p[i] > fin:
            n_intervalos+=1
            fin = p[i]+a
            intervalos.append((p[i], fin))
    return n_intervalos, intervalos

v = [1,3,9,2,7]
a = 3

print(menor_numero_intervalos(v, a))