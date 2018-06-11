'''
Created on 20 sept. 2017

@author: al341802-Miguel Matey Sanz
'''

from  algoritmia.datastructures.digraphs import UndirectedGraph

lc = [('Villaarriba','Villaconejos'),('Villaarriba','Villaabajo'),('Villaabajo','Villavilla'),
      ('Villaconejos','Villavilla'),('Villaabajo','Villorrio'),('Villorrio','Villita')]

g = UndirectedGraph(E=lc)
print(g)

for ciudad in g.V:
    print(ciudad, g.succs(ciudad))
    
