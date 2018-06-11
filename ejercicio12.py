'''
Created on 27 sept. 2017

@author: al341802-Miguel Matey Sanz
'''

def cuadrados(lista):  #Ejer11
    for elem in lista:
        yield elem*elem
             
def first(n,itera): #Ejer12
    if n>0:
        c=0
        for elem in itera:
            yield elem
            c+=1
            if c>=n: break
               
def filter(cond: "Int -> Bool",itera):  #Ejer13
    for elem in itera:
        if cond(elem):
            yield elem
            
def take_while(cond: "Int -> Bool", itera):  #Ejer14

    for elem in itera:
        if not cond(elem): break
        yield elem       

def squares():  #Ejer15
    i=1
    while True: 
        yield i*i
        i+=1

def esCapicua(n):
    original=str(n)
    reverso=original[::-1]
    return original==reverso
'''
print(list(first(20,range(50, 200))))    
print(list(first(100,[2,4,5,7,2])))     
print(list(filter(lambda n:n<100,range(50,200))))    
print(list(filter(lambda n:n%2==0,[2,4,5,7,2])))
print(list(take_while(lambda n:n<100,range(50,200))))    
print(list(take_while(lambda n:n%2==0,[2,4,5,7,2])))
'''

print(list(first(100,squares())))
print(list(take_while(lambda n:n<100, squares())))
print(list(first(20,filter(esCapicua,squares()))))