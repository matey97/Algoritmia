'''
Created on 16 ene. 2018

@author: Miguel
'''


def mientras_quepa(W,C):
    solucion = []
    n_contenedor = 0
    p_contenedor = C
    
    for peso_i in W:
        if peso_i <= p_contenedor:
            solucion.append(n_contenedor)
            p_contenedor -= peso_i
        else:
            n_contenedor += 1
            p_contenedor = C - peso_i
            solucion.append(n_contenedor)
    
    return solucion
            
def primero_que_quepa(W,C):
    solucion = []
    contenedores = []
    contenedores.append(C)
    
    for peso_i in W:
        for n_contenedor in range(len(contenedores)):
            if peso_i <= contenedores[n_contenedor]:
                solucion.append(n_contenedor)
                contenedores[n_contenedor] -= peso_i 
                break
        else:
            contenedores.append(C - peso_i)
            solucion.append(len(contenedores)-1)
    
    return solucion

def primero_que_quepa_ordenado(W,C):
    indices_ordenados = sorted(range(len(W)), key = lambda x: -W[x])
    
    solucion = [-1]*len(W)
    contenedores = []
    contenedores.append(C)
    
    for i in indices_ordenados:
        peso_i = W[i]
        for n_contenedor in range(len(contenedores)):
            if peso_i <= contenedores[n_contenedor]:
                solucion[i]=n_contenedor
                contenedores[n_contenedor] -= peso_i 
                break
        else:
            contenedores.append(C - peso_i)
            solucion[i] = len(contenedores)-1
            
    return solucion

W, C = [1, 2, 8, 7, 8, 3], 10

for solve in [mientras_quepa, primero_que_quepa, primero_que_quepa_ordenado]:
    sol = solve(W, C)
    print("Método:", solve.__name__)
    if sol is None:
        print("No implementado")
    else:
        print("Solución: {}, usados {} contenedores\n".format(sol, 1 + max(sol)))