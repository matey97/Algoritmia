'''
Created on 4 oct. 2017

@author: Miguel
'''
from algoritmia.datastructures.mergefindsets import MergeFindSet
from algoritmia.datastructures.digraphs import UndirectedGraph
from algoritmia.datastructures.queues import Fifo
from labyrinthviewer import LabyrinthViewer
from random import shuffle

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


g = crea_laberinto_mod(40, 40, 9)

camino = shortest_path(g, (0,0), (39,39))


lv = LabyrinthViewer(g, canvas_width=600, canvas_height=400, margin=10)
lv.add_path(camino,'blue')
lv.run()