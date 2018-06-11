from tempfile import TemporaryFile
import sys

CARA = 0
CRUZ = 1
cCARA = 'o'
cCRUZ = 'x'


def gira(pila, t):
    return [1 - i for i in pila[:t][::-1]] + pila[t:]


def fromString(s):
    return [CARA if c == cCARA
                 else CRUZ if c == cCRUZ
                 else error("Caracter erróneo: {}".format(c))
            for c in s]

def toString(pila):
    s = ""
    for m in pila:
        s += cCARA if m == CARA else cCRUZ
    return s

def ejecuta(programa, cadena):
    stdout = sys.stdout
    stderr = sys.stderr
    argv = sys.argv

    fsalida = TemporaryFile(mode="w+")
    ferror = TemporaryFile(mode="w+")

    sys.stdout = fsalida
    sys.stderr = ferror
    sys.argv = [programa, cadena]
    globales = {"__name__": "__main__"}
    modules = list(sys.modules.keys())

    try:
        exec(compile(open(programa).read(), programa, 'exec'), globales)
    except SystemExit:
        pass
    except:
        import traceback
        sei = sys.exc_info()
        sys.stderr = stderr
        sys.stdout = stdout
        traceback.print_exception(sei[0], sei[1], sei[2])
        sys.exit(1)

    for i in list(sys.modules.keys()):
        if i not in modules:
            del sys.modules[i]
    sys.stdout = stdout
    sys.stderr = stderr
    sys.argv = argv

    fsalida.seek(0)
    ordenes = []
    for l in fsalida.readlines():
        try:
            n = int(l)
        except ValueError:
            error('En la salida del programa he encontrado "{}" en lugar de un número'.format(n))
        ordenes.append(n)
    return ordenes

def error(m):
    sys.stderr.write(m + "\n")
    sys.exit(1)

def verifica(pasos, pila):
    p = pila[:]
    for t in pasos:
        if t > len(p) or t < 0:
            error("Valor no válido para el número de monedas: {}".format(t))
        p2 = gira(p, t)
        print("{} , {} -> {}".format(toString(p), t, toString(p2)))
        p = p2

    if CRUZ in p:
        error("El resultado no es correcto")
    print("Ejemplo correcto")


def main():
    if len(sys.argv) != 3:
        error("Necesito exactamente dos argumentos: el programa y la pila.")

    programa = sys.argv[1]
    pila = sys.argv[2]

    pasos = ejecuta(programa, pila)
    verifica(pasos, fromString(pila))

main()

