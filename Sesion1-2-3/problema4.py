'''
Created on 4 oct. 2017

@author: Miguel
'''
from algoritmia.datastructures.mergefindsets import MergeFindSet
from algoritmia.datastructures.digraphs import UndirectedGraph
from algoritmia.datastructures.queues import Fifo
from labyrinthviewer import LabyrinthViewer
from vertex2dgraphviewer import Vertex2dGraphViewer
from random import shuffle

def horse_graph (rows, cols):
    vertices = [(i,j) for i in range(0,rows) for j in range(0,cols)]
    
    aristas=[]

    for fila in range(0,rows):
        for col in range(0,cols):
            if fila-1>=0 and col+2<cols:
                aristas.append(((fila,col),(fila-1,col+2)))
            if fila+1<rows and col+2<cols:
                aristas.append(((fila,col),(fila+1,col+2))) 
            if fila+2<rows and col+1<cols:
                aristas.append(((fila,col),(fila+2,col+1)))
            if fila+2<rows and col-1>=0:
                aristas.append(((fila,col),(fila+2,col-1)))  
     
    mat=[]             
    for i in range(rows):   
        mat.append([])
        for j in range(cols):
            mat[i].append(-1)
            
    return (UndirectedGraph(V=vertices,E=aristas),mat)

def saltos_desde(g, source, matrix):
    saltos=[]
    seen=set()
    queue=Fifo()
    seen.add(source)
    queue.push((source,source))
    aux=list(source)
    matrix[aux[0]][aux[1]]=0
    while len(queue)>0:
        u,v=queue.pop()
        saltos.append((u,v))
        for succ in g.succs(v):
            if succ not in seen:
                seen.add(succ)
                queue.push((v,succ))
                aux1=list(succ)
                aux2=list(v)
                matrix[aux1[0]][aux1[1]]=matrix[aux2[0]][aux2[1]]+1
    return (matrix,saltos)


g, mat=horse_graph(3,3)

mat, saltos=saltos_desde(g, (0,0), mat)

for i in range(len(mat)):
    print(mat[i])

print("Casillas alcanzables:",len(saltos))    
    
viewer=Vertex2dGraphViewer(g, window_size=(500,500))
viewer.run()
