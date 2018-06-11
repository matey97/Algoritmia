def mientras_quepa(W, C):
    lista=[]
    contenedor = 0
    p_contenedor = C
    for w in W:
#         if p_contenedor - w >= 0:
#             lista.append(contenedor)
#             p_contenedor -= w
#         else:
#             contenedor += 1
#             p_contenedor = C 
#             if p_contenedor - w >= 0:
#                 lista.append(contenedor)
#                 p_contenedor -= w 
        if p_contenedor < w:
            contenedor += 1
            p_contenedor = contenedor
        lista.append(contenedor)
        p_contenedor -=w        
    return lista

def primero_que_quepa(W, C):
    lista = []
    contenedores = []
    contenedores.append(C)
    
    for w in W:
        for i in range(len(contenedores)):
            if contenedores[i] >= w:
                lista.append(i)
                contenedores[i] -= w    
                break
        else: #Se ejecuta si no se sale del for con BREAK
            contenedores.append(C)
            i=len(contenedores)-1
            lista.append(i)
            contenedores[i] -= w
    return lista

def primero_que_quepa_ordenado(W, C):
    indices_ordenados = sorted(range(len(W)), key = lambda i:-W[i])
    lista=[-1]*len(W)
    contenedores = []
    contenedores.append(C)
    for w in indices_ordenados:
        for i in range(len(contenedores)):
            if contenedores[i] >= W[w]:
                lista[w]=i
                contenedores[i] -= W[w]    
                break
        else: #Se ejecuta si no se sale del for con BREAK
            contenedores.append(C)
            i=len(contenedores)-1
            lista[w]=i
            contenedores[i] -= W[w]
    return lista 
    


W, C = [1, 2, 8, 7, 8, 3], 10

for solve in [mientras_quepa, primero_que_quepa, primero_que_quepa_ordenado]:
    sol = solve(W, C)
    print("Método:", solve.__name__)
    if sol is None:
        print("No implementado")
    else:
        print("Solución: {}, usados {} contenedores\n".format(sol, 1 + max(sol)))