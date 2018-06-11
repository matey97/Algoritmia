'''
Created on 22 nov. 2017

@author: al341802-Miguel Matey Sanz
'''
from algoritmia.schemes.decreaseandconquer import IDecreaseAndConquerProblem
from algoritmia.schemes.decreaseandconquer import DecreaseAndConquerSolver

def punto_fijo(v):
    b = 0
    e = len(v)
    
    while (e-1 != b): 
        h = (b+e)//2
        if v[h] == h:
            return h
        elif v[h] < h:
            b = h
        elif v[h] > h:
            e = h+1 

class DCPunto_fijo(IDecreaseAndConquerProblem):
    
    def __init__(self, v, b, e):
        self.v = v
        self.b = b
        self.e = e
    
    def is_simple(self):
        return self.e-1==self.b
    
    def trivial_solution(self):
        return self.b if self.b==self.v[self.b] else None
    
    def decrease(self):
        h = (self.b+self.e)//2
        if self.v[h] < h: return DCPunto_fijo(self.v, h+1, self.e)
        elif self.v[h] > h: return DCPunto_fijo(self.v, self.b, h)
        else: return DCPunto_fijo(self.v, h, h+1)
    
    def process(self, s):
        return s
        
        

def main():
    v = [-10, -5, 1, 2, 4]
    res = punto_fijo(v)
    
    print("Sin esquema:",res)
    solver = DecreaseAndConquerSolver()
    print("Con esquema:",solver.solve(DCPunto_fijo(v, 0, len(v))))
    
main() 