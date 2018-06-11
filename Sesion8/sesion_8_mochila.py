'''
Created on 13 dic. 2017

@author: Miguel
'''
from algoritmia.utils import infinity

#Versión recursiva directa
def mochila_rec(v, w, W):
    def B(n, c):
        if n == 0:
            return 0
        elif n > 0 and w[n-1] <= c:
            return max(B(n-1,c),B(n-1,c-w[n-1])+v[n-1])
        elif n > 0 and w[n-1] > c:
            return B(n-1,c)
            
    N = len(v)
    return B(N, W)

#Versión recursiva con memoización
def mochila_rec_mem(v, w, W):
    def B(n, c):
        if n == 0: 
            return 0
        if (n, c) not in mem:
            #mem[n,c] = infinity
            if n > 0 and w[n-1] <= c:
                mem[n,c] = max(B(n-1,c),B(n-1,c-w[n-1])+v[n-1])
            elif n > 0 and w[n-1] > c:
                mem[n,c] = B(n-1,c)
        return mem[n,c]
    
    N = len(v)
    mem = {}
    return B(N, W)

#Versión recursiva con memoización y recuperación de camino
def mochila_rec_mem_camino(v, w, W):
    def B(n, c):
        if n == 0: 
            return 0
        if (n, c) not in mem:
            mem[n,c] = (-infinity, (),)
            if n > 0 and w[n-1] <= c:
                mem[n,c] = max((B(n-1,c), (n-1,c), 0),(B(n-1,c-w[n-1])+v[n-1], (n-1,c-w[n-1]), 1))
            elif n > 0 and w[n-1] > c:
                mem[n,c] = (B(n-1,c), (n-1,c), 0)
        return mem[n,c][0]
    
    N = len(v)
    mem = {} 
    score = B(N, W)
    n, c = N, W
    sol = []
    while (n,c) != (0,0):
        _, (n_prev, c_prev), decision = mem[n,c]
        sol.append(decision)
        n, c = n_prev, c_prev
    sol.reverse()
    return score, sol

# Versión iterativa con recuperación de camino
def mochila_iter_camino(v, w, W):
    mem = {}
    mem[0,0] = (0, (None,None), None)
    N = len(v) # número de objetos
    
    for c in range(1, W+1): mem[0,c] = (0, (None,None), None)
    for n in range(1, N+1):
        for c in range(0, c+1):
            if n > 0 and w[n-1] <= c:
                mem[n,c] = max((mem[n-1,c][0], (n-1,c), 0),(mem[n-1, c-w[n-1]][0]+v[n-1], (n-1,c-w[n-1]), 1))
            elif n > 0 and w[n-1] > c:
                mem[n,c] = (mem[n-1,c][0], (n-1,c), 0)
    
    score = mem[N,W][0]
    n, c = N, W
    sol = []
    while (n,c) != (0,0):
        _, (n_prev, c_prev), decision = mem[n,c]
        sol.append(decision)
        n, c = n_prev, c_prev
    sol.reverse()
    return score, sol

# Versión iterativa con reduccion del coste espacial
def mochila_iter_reduccion_coste(v, w, W):
    N = len(v) # número de objetos
    current = [0]*(W+1)
    previous = [None] * (W+1) 
    for n in range(1, N+1):
        previous, current = current, previous
        for c in range(0, W+1):
            if n > 0 and w[n-1] <= c:
                current[c] = max(previous[c], previous[c-w[n-1]]+v[n-1])
            elif n > 0 and w[n-1] > c:
                current[c] = previous[c]
              
    return current[W]

# PROGRAM PRINCIPAL

v = [90,75,60,20,10]
w = [4,3,3,2,2]
W = 6

print("Versión recursiva:")
print(mochila_rec(v, w, W))
print()
print("Versión recursiva con memoización:")
print(mochila_rec_mem(v, w, W))
print()
print("Versión recursiva con memoización y recuperación de camino:")
print(mochila_rec_mem_camino(v, w, W))
print()
print("Versión iterativa con recuperación de camino:")
print(mochila_iter_camino(v, w, W))
print()
print("Versión iterativa con reduccion del coste espacial:")
print(mochila_iter_reduccion_coste(v, w, W))
