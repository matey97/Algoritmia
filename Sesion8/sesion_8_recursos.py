'''
Created on 13 dic. 2017

@author: Miguel
'''
from random import randrange, seed
from algoritmia.utils import infinity

# Versión recursiva directa
def recursos_rec(v, m, U):
    def B(n, u):
        if n == 0:
            return 0
        
        maximo = -infinity
        for k in range(min(m[n-1],u)+1):
            maximo = max(maximo, B(n-1,u-k)+v[n-1,k])
        return maximo
    
    N = len(m)
    return B(N, U)

# Versión recursiva con memoización
def recursos_rec_mem(v, m, U):
    def B(n, u):
        if n == 0:
            return 0
        if (n,u) not in mem:
            mem[n,u] = -infinity
            for k in range(min(m[n-1],u)+1):
                mem[n,u] = max(mem[n,u], B(n-1, u-k)+v[n-1,k])
        return mem[n,u]
    
    N = len(m)
    mem = {}
    return B(N, U)

# Versión recursiva con memoización y recuperación de camino
def recursos_rec_mem_camino(v, m, U):
    def B(n, u):
        if n == 0:
            return 0
        if (n,u) not in mem:
            mem[n,u] = (-infinity, (), )
            for k in range(min(m[n-1],u)+1):
                mem[n,u] = max(mem[n,u], (B(n-1, u-k)+v[n-1,k], (n-1,u-k),k))
        return mem[n,u][0]
    
    N = len(m)
    mem = {}
    score = B(N, U)
    sol = []
    n, u = N, U
    while n != 0:
        _, (n, u), k = mem[n,u]
        sol.append(k)
    sol.reverse()
    return score, sol


# PROGRAM PRINCIPAL

U = 12          # número de unidades de recurso disponibles
m = [2,4,2,4,2] # número máximo de recursos que podemos asignar a cada actividad
                # podemos obtener el número de actividades como len(m)
seed(0)
# dicionario/tabla con los beneficios que reportan asignar distintos recursos a cada actividad
# ejemplo: v[1,3] es el beneficio que proporcionará la actividad 1 si se le asignan 3 unidades de recurso
v = dict(((i,u), randrange(100)) for i in range(len(m)) for u in range(0, U+1))

print("Versión recursiva:")
print(recursos_rec(v, m, U))
print()
print("Versión recursiva con memoización:")
print(recursos_rec_mem(v, m, U))
print()
print("Versión recursiva con memoización y recuperación de camino:")
print(recursos_rec_mem_camino(v, m, U))
