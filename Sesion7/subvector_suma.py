'''
Created on 22 nov. 2017

@author: al341802-Miguel Matey Sanz
'''

from algoritmia.schemes.divideandconquer import IDivideAndConquerProblem
from algoritmia.schemes.divideandconquer import DivideAndConquerSolver

class subvector_suma(IDivideAndConquerProblem):
    def __init__(self,v, b, e):
        self.v = v
        self.b = b
        self.e = e
    
    def is_simple(self):
        return self.e - 1 == self.b
    
    def trivial_solution(self):
        pass
    
    def divide(self):
        h = (self.b+self.e)//2
        yield subvector_suma(self.v, self.b, h)
        yield subvector_suma(self.v, h, self.e)
    
    def combine(self, s):
        pass
        


v = [10, -2, 5, 4, -14, 3, -7]
b, e = 0, len(v)
h = (b+e)//2
for i in range(h):
    
for i in range(h, len(v)):
    
