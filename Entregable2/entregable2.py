import sys

CARA = 'o'
CRUZ = 'x'

def cara_arriba (cadena_monedas):
    
    def gira_bloque(lista, i):
        aux = lista[:i]
        aux.reverse()
        for j, a in enumerate(aux):
            if a==CRUZ:
                lista[j]=CARA
            else:
                lista[j]=CRUZ
            
    lista = []
    res = []
    
    for moneda in cadena_monedas:
        lista.append(moneda)
    
    for i, m in enumerate(lista): #Coste n*m --> Coste n bucle for + Coste m giraBloque(...)
        if not CRUZ in lista:
            break
        #Girar bloque si actual!=ultimo y actual!=siguiente o actual es el ultimo y es una cruz
        if (i!=len(lista)-1 and m != lista[i+1]) or (i==len(lista)-1 and m==CRUZ):
            gira_bloque(lista, i+1) 
            res.append(i+1)   
        
    return res


def main():
    res = cara_arriba(sys.argv[1])

    for elem in res:
        print(elem)

main()
    
    