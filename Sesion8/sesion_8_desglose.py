'''
Created on 17 ene. 2018

@author: Miguel
'''
from algoritmia.utils import infinity

def desglose_directo(Q, v, w, m):
    def L(q,n):
        if q == 0 and n == 0:
            return 0
        if q > 0 and n == 0:
            return infinity
        minimo = infinity
        for i in range(min(m[n-1],(q//v[n-1]))+1):
            minimo = min(minimo, L(q-i*v[n-1], n-1) + i*w[n-1])
        return minimo
    
    return L(Q, len(v))

def desglose_rec_mem(Q, v, w, m):
    def L(q,n):
        if q == 0 and n == 0:
            return 0
        if q > 0 and n == 0:
            return infinity 
        if (q,n) not in mem:
            mem[q,n] = infinity
            for i in range(min(m[n-1],(q//v[n-1]))+1):
                mem[q,n] = min(mem[q,n], L(q-i*v[n-1], n-1) + i*w[n-1])
        return mem[q,n]
    mem = {}
    return L(Q, len(v))

def desglose_rec_mem_camino(Q, v, w, m):
    def L(q,n):
        if q == 0 and n == 0:
            return 0
        if q > 0 and n == 0:
            return infinity
        if (q,n) not in mem:
            mem[q,n] = (infinity, (), infinity)
            for i in range(min(m[n-1],(q//v[n-1]))+1):
                mem[q,n] = min(mem[q,n], (L(q-i*v[n-1], n-1) + i*w[n-1], (q-i*v[n-1], n-1), i))
        return mem[q,n][0]
            
    mem = {}
    peso = L(Q, len(v))
    sol = []
    q, n = Q, len(v)
    while q != 0:
        _, (q,n), i = mem[q,n]
        sol.append(i)
    sol.reverse()
    return peso, sol


Q = 24 # cantidad a desglosar
v = [1,2,5,10] # valores faciales de las monedas
w = [1,1,4,6] # pesos de las monedas
m = [3,1,4,1] # cantidad de monedas disponibles de cada tipo

print("Versión recursiva:")
print(desglose_directo(Q, v, w, m))
print()
print("Versión recursiva con memoización:")
print(desglose_rec_mem(Q, v, w, m))
print()
print("Versión recursiva con memoización y recuperación de camino:")
print(desglose_rec_mem_camino(Q, v, w, m))