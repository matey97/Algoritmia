'''
Created on 4 oct. 2017

@author: Miguel
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

def path_directo(g, source, target): ##Devuelve en camino directamente
    def path_desde(u):
        seen.add(u)
        camino.append(u)
        if u == target:
            return True
        for succ in g.succs(u):
            if succ not in seen:
                if path_desde(succ):
                    return True
        camino.pop()
        return False
            
    seen=set()
    camino=[]
    path_desde(source)
    return camino

def path (g: "UndirectedGraph", source: "(i,j)", target: "(x,y)"):    ##Problema2, Calcula aristas --> recupera camino con backpointers
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

g = crea_laberinto(40, 40)

camino = path(g, (0,0), (39,39))
camino2 = path_directo(g, (0,0), (39,39))

lv = LabyrinthViewer(g, canvas_width=600, canvas_height=400, margin=10)
lv.add_path(camino,'blue',-1)
lv.add_path(camino2,'red',1)
lv.run()