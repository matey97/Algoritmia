'''
Created on 6 oct. 2017

@author: Miguel
'''
import sys
from algoritmia.datastructures.digraphs import UndirectedGraph
from algoritmia.datastructures.queues import Fifo
from labyrinthviewer import LabyrinthViewer

def load_labyrinth (fichero): #Crea laberinto a partir del fichero
    edges=set()
    fila=0
    for linea in open(fichero, encoding='utf8'):
        muros = linea.split(',')
        for col in range(len(muros)):
            muro=muros[col]
            if 'n' not in muro:
                edges.add(((fila,col),(fila-1,col)))
            if 'e' not in muro:
                edges.add(((fila,col),(fila,col+1)))
            if 's' not in muro:
                edges.add(((fila,col),(fila+1,col)))
            if 'w' not in muro:
                edges.add(((fila,col),(fila,col-1))) 
        fila+=1 
            
    return UndirectedGraph(E=edges)

def load_matrix(row, col):  #Inicializa la matriz de costes a -1
    matrix=[]    
    for _ in range(row+1):  
        matrix.append([-1]*(col+1))
    return matrix

def width_edges (g, source, matrix): #Recorre aristas y actualiza matriz de costes
    edges=[]
    seen=set()
    queue=Fifo()
    seen.add(source)
    queue.push((source,source))
    matrix[source[0]][source[1]]=0
    while len(queue)>0:
        u,v=queue.pop()
        edges.append((u,v))
        for succ in g.succs(v):   
            if succ not in seen:
                matrix[succ[0]][succ[1]]=matrix[v[0]][v[1]]+1 
                seen.add(succ)
                queue.push((v,succ))
    return (edges, matrix)

def farthest_cell_from(g, u, matrix): ##Devuelve la celda mas alejada de u
    edges, matrix=width_edges(g, u, matrix)
    farthest = matrix_max(matrix) 
    return (farthest, edges, matrix)

def matrix_max(matrix):
    maxim=0
    verticemax=()
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j]>maxim:
                maxim=matrix[i][j]
                verticemax=(i,j)
    return verticemax


def path_recoverer(edges, target):    
    bp = {}
    for u,v in edges:
        bp[v]=u
    
    path=[]
    path.append(target)
    while target != bp[target]:
        target=bp[target]
        path.append(target)
    path.reverse()
    return path




lab = load_labyrinth(sys.argv[1])

rows, cols = max(lab.V)

matrix = load_matrix(rows, cols)

##Celda mas alejada de 0,0
u, edges, matrix=farthest_cell_from(lab,(0,0), matrix)

##Celda mas alejada de u, edges contiene aristas para llegar de u a v
v, edges, matrix=farthest_cell_from(lab,u, matrix)

##Distancia entre u y v
cost=matrix[v[0]][v[1]]

##Aplicamos restricciones para la eleccion de la celda inicial y final
if u[0]<v[0]:
    start=u
    last=v
elif u[0]>v[0]:
    start=v
    last=u
elif u[1]>v[1]:
    start=v
    last=u    
elif u[1]<v[1]:
    start=u
    last=v

print(start[0],start[1])
print(last[0],last[1])
print(cost)

if (len(sys.argv)==3 and sys.argv[2]=='-g'):
    camino=path_recoverer(edges, v)
    lv = LabyrinthViewer(lab, canvas_width=600, canvas_height=400, margin=10)
    lv.set_input_point(start)
    lv.set_output_point(last)
    lv.add_path(camino,'blue')
    lv.run()  