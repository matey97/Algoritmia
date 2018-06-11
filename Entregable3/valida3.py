'''
Created on Nov 9, 2017

@author: David Llorens
'''
import sys

OUT = '#'
P = 'o'
E = '.'

def prettyPrint(mat):
    rows = len(mat)
    cols = len(mat[0])
    for r in range(rows):
        for c in range(cols):
            print(' ' if mat[r][c]==OUT else mat[r][c], end='')
        print()

def load_tablero(filename):
    lines = [list(line.strip()) for line in open(filename).readlines()]
    return lines

def load_solution(filename):
    sol =[]
    for lin in [line.strip().split() for line in open(filename).readlines()]:
        a,b,c,d = [int(x) for x in lin]
        sol.append(((a,b),(c,d)))
    return sol

def count_pieces(tablero):
    return sum([lin.count(P) for lin in tablero])

def move(tab, source, target):
    rows = len(tab)
    cols = len(tab[0])
    sr, sc = source
    tr, tc = target
    if min(sr,sc,tr,tc)<0 or max(sc,tc)>=cols or max(sr,tr)>=rows:
        return False
    if not(sr==tr and abs(tc-sc)==2 or sc==tc and abs(tr-sr)==2):
        return False
    mr = sr if tr==sr else (tr-sr)//2+sr
    mc = sc if tc==sc else (tc-sc)//2+sc
    if not(tab[sr][sc]==P and tab[tr][tc]==E and tab[mr][mc]==P):
        return False
    tab[sr][sc] = tab[mr][mc] = E
    tab[tr][tc] = P
    return True

def valida(tablero, sol): 
    if len(sol) != count_pieces(tablero)-1:
        return "ERROR: La longitud de la solución no es válida."
    t = [row[:] for row in tablero]
    for  i,(source, target) in enumerate(sol):
        if not move(t, source, target):
            prettyPrint(t)
            return "ERROR: No se pudo efectuar el paso {0}: mover ficha de {1} a {2}.".format(i+1, source, target)
    return "<Solución válida>"
      
# PROG PRINCIPAL
if len(sys.argv)==3:
    try:
        tablero = load_tablero(sys.argv[1])
    except:
        print("Error leyendo el tablero")
        sys.exit(1)
    try:
        solucion = load_solution(sys.argv[2])
    except Exception as e:
        print("Error leyendo la solución", e)
        sys.exit(1)
    print(valida(tablero, solucion))
else:
    print('Ejemplo de uso:')
    print('    python3 valida3.py tablero1.txt solucion1.txt')
          





