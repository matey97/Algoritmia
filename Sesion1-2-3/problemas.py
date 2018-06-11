'''
Created on 27 sept. 2017

@author: al341802-Miguel Matey Sanz
'''

from algoritmia.datastructures.mergefindsets import MergeFindSet
from algoritmia.datastructures.digraphs import UndirectedGraph
from algoritmia.datastructures.queues import Fifo
from labyrinthviewer import LabyrinthViewer
from random import shuffle

def crea_laberinto (nfil,ncol):     ##Problema1
    vertices = [(i,j) for (i) in range(nfil) for (j) in range(ncol)]
    
    mfs = MergeFindSet()
    for v in vertices:
        mfs.add(v)
        
    aristasV = [((f,c),(f+1,c)) for f in range(nfil-1) for c in range(ncol)]
    aristasH = [((f,c),(f,c+1)) for f in range(nfil) for c in range(ncol-1)]
    aristas = aristasV + aristasH
    shuffle(aristas)
    
    pasillos = []
    for (u,v) in aristas:
        if mfs.find(u) != mfs.find(v):
            mfs.merge(u, v)
            pasillos.append((u,v))
            
    return UndirectedGraph(E=pasillos)

def path (g: "UndirectedGraph", source: "(i,j)", target: "(x,y)"):    ##Problema2
    def recorre_profundidad(u,v):
        seen.add(v)
        aristas.append((u,v))
        if v != target:
            for succ in g.succs(v):
                if succ not in seen:
                    recorre_profundidad(v,succ) 
                  
                    
    seen=set()
    aristas=[]
    
    recorre_profundidad(source, source)
    return recuperador_camino(aristas, target)
    

       
def recuperador_camino(aristas, target):    ##Problema2
    dc = {}
    for u,v in aristas:
        dc[v]=u
    
    path=[]
    path.append(target)
    while target != dc[target]:
        target=dc[target]
        path.append(target)
    path.reverse()
    return path 


def crea_laberinto_mod (nfil, ncol, n):     ##Problema3
    vertices = [(i,j) for (i) in range(nfil) for (j) in range(ncol)]
    
    mfs = MergeFindSet()
    for v in vertices:
        mfs.add(v)
        
    aristasV = [((f,c),(f+1,c)) for f in range(nfil-1) for c in range(ncol)]
    aristasH = [((f,c),(f,c+1)) for f in range(nfil) for c in range(ncol-1)]
    aristas = aristasV + aristasH
    shuffle(aristas)
    
    nCamino = n
    pasillos = []
    for (u,v) in aristas:
        if mfs.find(u) != mfs.find(v):
            if nCamino==0:
                mfs.merge(u, v)
            else:
                nCamino-=1
            pasillos.append((u,v))
    
    return UndirectedGraph(E=pasillos)

def shortest_path (g: "UndirectedGraph", source: "(i,j)", target: "(x,y)"):     ##Problema3
    def recorredor_aristas_anchura (g, source):
        aristas=[]
        seen=set()
        queue=Fifo()
        seen.add(source)
        queue.push((source,source))
        while len(queue)>0:
            u,v=queue.pop()
            aristas.append((u,v))
            if v != target:
                for succ in g.succs(v):
                    if succ not in seen:
                        seen.add(succ)
                        queue.push((v,succ))
        return aristas
            
    aristas=recorredor_aristas_anchura(g, source)
    return recuperador_camino(aristas, target)
 
    

##########################    
#### Uso de funciones ####
##########################


g = crea_laberinto_mod(40, 40, 9)

camino1 = path(g, (0,0), (39,39))
camino2 = shortest_path(g, (0,0), (39,39))


lv = LabyrinthViewer(g, canvas_width=600, canvas_height=600, margin=10)
lv.add_path(camino1,'blue',-1)
lv.add_path(camino2,'red',1)
lv.run()

