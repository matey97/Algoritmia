
'''
Created on 25 sept. 2017

@author: Miguel
'''
from algoritmia.datastructures.digraphs import UndirectedGraph
from algoritmia.datastructures.queues import Fifo


###Busqueda de vertice

def busca_tesoro_primero_anchura (laberinto,v_inicio):
    seen=set()
    queue=Fifo()
    queue.push(v_inicio)
    seen.add(v_inicio)
    while len(queue)>0:
        v=queue.pop()
        if v==v_tesoro:
            return v
        for succ in laberinto.succs(v):
            if succ not in seen:
                seen.add(succ)
                queue.push(succ)
    return None
    
def busca_tesoro_primero_profundidad (laberinto,v_inicio):
    def busca_desde(v):
        seen.add(v)
        if v==v_tesoro: ##Preorden
            return v
        for succ in laberinto.succs(v):
            if succ not in seen:
                res=busca_desde(succ)
                if res!=None:
                    return res
##      if v==v_tesoro: Postorden
##          return v
        return None        
        
    seen=set()
    return busca_desde(v_inicio)
    

pasillos = [((0,0),(0,1)), ((0,2),(0,3)), ((1,0),(1,1)), ((1,1),(1,2)),
            ((2,0),(2,1)), ((2,1),(2,2)), ((2,2),(2,3)), ((0,1),(1,1)),
            ((0,2),(1,2)), ((0,3),(1,3)), ((1,1),(2,1)), ((1,2),(2,2))]

laberinto = UndirectedGraph(E=pasillos)

v_inicio = (0,0)
v_tesoro = (1,3)

pos_tesoro_encontrada_anchura = busca_tesoro_primero_anchura(laberinto, v_inicio)
pos_tesoro_encontrada_profundidad = busca_tesoro_primero_profundidad(laberinto, v_inicio)

if pos_tesoro_encontrada_anchura == None:
    print("Tesoro no encontrado por anchura")
else:
    print("Tesoro encontrado en la habitación {0} por anchura".format(pos_tesoro_encontrada_anchura))
    
if pos_tesoro_encontrada_profundidad == None:
    print("Tesoro no encontrado por profundidad")
else:
    print("Tesoro encontrado en la habitación {0} por profundidad".format(pos_tesoro_encontrada_profundidad))
    
    

##Exploracion/recorrido de vertices

def recorredor_vertices_anchura (grafo,v_inicial):
    vertices=[]
    seen=set()
    queue=Fifo()
    seen.add(v_inicial)
    queue.push(v_inicial)
    while len(queue)>0:
        v=queue.pop()
        vertices.append(v)
        for succ in grafo.succs(v):
            if succ not in seen:
                seen.add(succ)
                queue.push(succ)
    return vertices

def recorredor_vertices_profundidad(grafo, v_inicial):
    def recorre_desde(v):
        seen.add(v)
        vertices.append(v) ##Preorden
        for succ in grafo.succs(v):
            if succ not in seen:
                recorre_desde(succ)
##      vertices.append(v) Postorden
    seen=set()
    vertices=[]
    recorre_desde(v_inicial)
    return vertices

print("Recorrido de vertices en anchura: {0}".format(recorredor_vertices_anchura(laberinto, v_inicio)))
print("Recorrido de vertices en profundidad: {0}".format(recorredor_vertices_profundidad(laberinto, v_inicio)))


##Exploracion/recorrido de aredges
def recorredor_aristas_anchura(grafo,v_inicial):
    aredges]
    seen=set()
    queue=Fifo()
    seen.add(v_inicial)
    queue.push((v_inicial,v_inicial))
    while len(queue)>0:
        u,v=queue.pop()
        aredgesppend((u,v))
        for succ in grafo.succs(v):
            if succ not in seen:
                seen.add(succ)
                queue.push((v,succ))
    return aredges
def recorredor_aristas_profundidad(grafo,v_inicial):
    def recorre_desde(u,v):
        seen.add(v)
        aredgesppend((u,v)) ##Preorden
        for succ in grafo.succs(v):
            if succ not in seen:
                recorre_desde(v, succ)
##      aredgesppend((u,v)) Postorden
    aredges]
    seen=set()
    recorre_desde(v_inicial,v_inicial)
    return aredges
print("Recorrido de aredgesn anchura: {0}".format(recorredor_aristas_anchura(laberinto, v_inicio)))
print("Recorrido de aredgesn profundidad: {0}".format(recorredor_aristas_profundidad(laberinto, v_inicio)))