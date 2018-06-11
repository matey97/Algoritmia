'''
Created on 18 de sept. de 2017

@author: Miguel
'''
import math

def ecuacionPrimerGrado(b,c):
    if b!=0:
        return -c/b
    return "Infinitas Soluciones"

def ecuacionSegundoGrado(a,b,c):
    
    if a==0:
        return ecuacionPrimerGrado(b,c)
    
    dentroRaiz=b**2-4*a*c

    if dentroRaiz>=0:
        raiz=math.sqrt(dentroRaiz)    
    else:
        return "No hay soluciones"

    x1=(-b+raiz)/(2*a)
    x2=(-b-raiz)/(2*a)
    return (x1, x2)

a=int(input("Introduce a: "))
b=int(input("Introduce b: "))
c=int(input("Introduce c: "))


print("Soluciones: {0}".format(ecuacionSegundoGrado(a,b,c)))

       
