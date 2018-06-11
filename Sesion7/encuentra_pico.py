'''
Created on 22 nov. 2017

@author: al341802-Miguel Matey Sanz
'''
from algoritmia.schemes.decreaseandconquer import IDecreaseAndConquerProblem
from algoritmia.schemes.decreaseandconquer import DecreaseAndConquerSolver


def encuentra_pico(v):
    b = 0
    e = len(v)
    
    while (e-1 != b): 
        h = (b+e)//2
        if v[h] >= v[h-1]:
            b = h
        elif v[h-1] >= v[h]:
            e = h
    return b
 
class DCEncuentra_pico(IDecreaseAndConquerProblem):
    
    def __init__(self, v, b, e):
        self.v = v
        self.b = b
        self.e = e
    
    def is_simple(self):
        return self.e-1==self.b
    
    def trivial_solution(self):
        return self.b
    
    def decrease(self):
        h = (self.b+self.e)//2
        if self.v[h] >= self.v[h-1]: return DCEncuentra_pico(self.v, h, self.e)
        elif self.v[h] <= self.v[h-1]: return DCEncuentra_pico(self.v, self.b, h)
        else: return DCEncuentra_pico(self.v, h, h+1)
    
    def process(self, s):
        return s 
            
            
def main():
    v = [10, 20, 15, 2, 23, 90, 67]
    res = encuentra_pico(v)
    
    print("Sin esquema:",res)
    solver = DecreaseAndConquerSolver()
    print("Con esquema:",solver.solve(DCEncuentra_pico(v, 0, len(v))))
    
main() 