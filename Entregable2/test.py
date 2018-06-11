'''
Created on 2 nov. 2017

@author: Miguel
'''
import random
import sys

longitud = random.randrange(50, 100)
cadena = ""
for j in range(longitud):
    if random.random() > 0.5:
        cadena += 'x'
    else:
        cadena += 'o'

print(cadena)