'''
Created on 17 ene. 2018

@author: Miguel
'''

def punto_fijo(a):
    ini = 0
    fin = len(a)
    while fin-1!=ini:
        med = (fin+ini)//2
        if a[med] == med:
            return med
        elif a[med] < med:
            ini = med
        else:
            fin = med+1


v = [-10,-5, 1, 3, 6]

print(punto_fijo(v))