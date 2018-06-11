import sys 
from algoritmia.utils import infinity

def planeador(alturas, puntos):
    #altura --> altura actual del planeador ||| globos --> Cuantos globos quedan
    def P(altura, globos):
        if globos == 0:
            return 0    #Si no quedan globos no podemos conseguir puntos
        if (altura, globos) not in mem:
            mem[altura,globos] = -infinity, (None,None), None
            if globos > 0 and altura > alturas[globos-1]:   #Si estamos mas alto que el globo, no lo podemos coger (venimos desde atrás, lo que significa que sería como si subiesemos en el recorrido normal)
                mem[altura,globos] = (P(altura, globos-1),(altura, globos-1),0)
            elif globos > 0 and altura <= alturas[globos-1]:    #Si estamos mas bajo que el globo o a igual altura, lo podemos coger (venimos desde atrás, lo que significa que sería como si bajasemos en el recorrido normal)
                mem[altura,globos] =  max((P(altura, globos-1),(altura, globos-1),0), 
                                          (P(alturas[globos-1], globos-1) + puntos[globos-1],(alturas[globos-1], globos-1),1))
        return mem[altura,globos][0]

        
    mem = {}
    
    #La altura con la que empezamos la recursividad la ponemos en 0, ya que esta altura sería la ultima (también se podría poner min(alturas)).
    puntuacion = P(0, len(alturas))
    
    #Recuperación de camino
    solucion = []
    altura, globos = 0, len(alturas)
    while globos != 0:  #Pararemos cuando no queden globos (globos==0), la altura no nos importa
        _, (altura_p, globos_p), decision = mem[altura, globos]
        solucion.append(decision)
        altura, globos = altura_p, globos_p
    solucion.reverse()
    
    return puntuacion, solucion

#Obtiene del fichero las alturas y los puntos de cada globo, almacenandolos en dos vectores
def alturas_puntos_de_fichero(fichero):
    alturas = []
    puntos = []
        
    for linea in open(fichero):
        linea = linea.split()
        alturas.append(int(linea[0]))
        puntos.append(int(linea[1]))
    
    return alturas, puntos

#Imprime la solucion en el formato requerido
def imprime_solucion(puntuacion, solucion):
    print(puntuacion)
    for i in range(len(solucion)):
        if solucion[i] == 1:
            print(i+1, end=' ')


def main():
    alturas, puntos = alturas_puntos_de_fichero(sys.argv[1])
    puntuacion, solucion = planeador(alturas, puntos)
    imprime_solucion(puntuacion, solucion)
    
main()