'''
Created on 27 sept. 2017

@author: al341802-Miguel Matey Sanz
'''

def cuadrados(lista):
    for elem in lista:
        yield elem*elem

res = cuadrados([1,2,10,4,5])


for elem in res:
    print(elem)