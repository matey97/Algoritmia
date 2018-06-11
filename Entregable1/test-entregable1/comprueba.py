#!/usr/bin/python
# -*- coding: utf-8 -*-
#
##############################################################################
#
# comprueba.py 0.97: a simple program checker
#
# Copyright (C) 2008-2013 Juan Miguel Vilar
#                         Universitat Jaume I
#                         Castelló (Spain)
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
#  Any questions regarding this software should be directed to:
#
#   Juan Miguel Vilar
#   Departament de Llenguatges i Sistemes Informàtics
#   Universitat Jaume I
#   E12071 Castellón (SPAIN)
#
#   email: jvilar@lsi.uji.es
#
##############################################################################
#
# comprueba.py
#

from optparse import OptionParser
import os
from subprocess import Popen
import sys
import re

################################################################################
#
# Colores:
#

AMARILLO=33
AZUL=34
MAGENTA=35
NEGRO=30
ROJO=31
VERDE=32

FONDOROJO=41

BRILLANTE=1

noColores= False

def colorea(color, cadena, colorSalida= 0):
  if noColores:
    return cadena
  if type(color)== type(1):
    r= "\x1b[%dm" % color
  else:
    r= ""
    for i in color:
      r+= "\x1b[%dm" % i
  if cadena[-1]!= "\n":
    r+= cadena
  else:
    r+= cadena[:-1]
  if type(colorSalida)== type(1):
    r+= "\x1b[%dm" % colorSalida
  else:
    for i in colorSalida:
      r+= "\x1b[%dm" % i
  if cadena[-1]== "\n":
    r+= "\n"
  return r

################################################################################
#
# Errores:
#

def error(m):
  sys.stderr.write(colorea(ROJO, "Error: %s\n" % m))
  sys.exit(1)

def aviso(m):
  sys.stderr.write(colorea(AMARILLO, "Aviso: %s\n" %m))

################################################################################
#
# Ficheros:
#

def abre(n):
  try:
    return file(n)
  except:
    error ("No he podido abrir %s para lectura" % n)

def abreONone(n):
  if n== None:
    return None
  return abre(n)

################################################################################
#
# Redirección:
#

class RedirigeSalida:
  def __init__(self, original=sys.stdout):
    self.original= original
    self._acumulado= ""

  def write(self, l):
    self._acumulado+= l

  def flush(self):
    pass

  def acumulado(self):
    return self._acumulado

  def limpia(self):
    self._acumulado= ""

  def escribeOriginal(self, l):
    self.original.write(l)

  def __del__(self):
    if self._acumulado:
      self.original.write(self._acumulado)
      self._acumulado= ""


class RedirigeEntrada:
  def __init__(self, fentrada, salida, error, procesador):
    self.fentrada= fentrada # fichero de entrada
    self.salida= salida
    self.error= error
    self.procesador= procesador

    self.eof= False
    self.entrada= ""
    self.nlinea= 0
    self.pos= 0

  def leelinea(self):
    if self.eof:
      return ""
    if self.nlinea:
      salidaEncontrada= self.salida.acumulado()
      self.salida.limpia()
      errorEncontrado= self.error.acumulado()
      self.error.limpia()
      self.procesador.presentaSalida(salidaEncontrada, errorEncontrado)
    l= self.fentrada.readline()
    if not l:
      self.eof= True
      self.procesador.trataEOF()
      return
    self.nlinea= self.nlinea+1
    self.entrada= self.procesador.trataLinea(l, self.nlinea)

  def read(self, n):
    if self.eof:
      return ""
    if n!= 1:
      l= ""
      for i in range(n):
        l= l+self.read(1)
      return l
    if self.pos==len(self.entrada):
      self.leelinea()
    if self.eof:
      return ""
    c= self.entrada[self.pos]
    self.pos= self.pos+1
    return c

  def readline(self):
    if self.eof:
      return ""
    self.leelinea()
    if self.eof:
      return ""
    return self.entrada

  def isatty(self):
    return 0

  def close(self):
    pass

  def flush(self):
    pass

  def __del__(self):
    if not self.eof:
      salidaEncontrada= self.salida.acumulado()
      self.salida.limpia()
      errorEncontrado= self.error.acumulado()
      self.error.limpia()
      if salidaEncontrada != "" or errorEncontrado != "":
        self.procesador.presentaSalida(salidaEncontrada, errorEncontrado)
      self.procesador.entradaNoLeida()
      self.procesador.trataEOF()

  def __iter__(self):
    while 1:
      line=self.readline()
      if not line: break
      yield line

################################################################################
#
# Procesadores (actuan sobre la entrada y la salida):
#

class Procesador:
  def trataLinea(self, l, nlinea):
    """Recibe la línea leída y el número de línea"""
    return l

  def presentaSalida(self, salidaEncontrada, errorEncontrado):
    """Recibe la salida y el error correspondiente a la última línea leída"""
    pass

  def entradaNoLeida(self):
    """Trata el evento en que hay entrada no leída pero que no se procesará
    porque se cierra la entrada estándar"""
    pass

  def trataEOF(self):
    """Se invoca cuando se ha terminado de procesar el fichero"""
    pass

class Comprobador(Procesador):
  """Procesador que comprueba que lo encontrado coincide con lo esperado"""
  def __init__(self, salida, mostrarTodas, separaCampos, separaError, nombre):
    self.salida= salida
    self.mostrarTodas= mostrarTodas
    self.separaCampos= separaCampos
    self.separaError= separaError
    self.salida.write(self.barra(" "+nombre+" "))
    self.vistaEntrada= False
    self.nerrores= 0
    self.nlinea= 0

  def trataLinea(self, l, nlinea):
    self.vistaEntrada= True
    hayFinL= l[-1]=="\n"
    if hayFinL: l= l[:-1]
    campos= l.split(self.separaCampos)
    camposError= campos[-1].split(self.separaError)
    campos[-1]= camposError[0]
    camposError= camposError[1:]

    self.entrada= campos[0].rstrip()
    if hayFinL:
      self.entrada= self.entrada+"\n"

    self.salidaEsperada= [ s.strip() for s in campos[1:] ]
    self.errorEsperado= [ s.strip() for s in camposError ]
    self.nlinea= nlinea
    return self.entrada

  def errorEnSalida(self, esperado, encontrado):
    finOk= (encontrado== "" or encontrado[-1]=="\n")
    if len(esperado)== 0 and encontrado== "":
      return False
    if len(esperado)!= 0 and finOk:
      s= [c.strip() for c in encontrado.split("\n")]
      s= s[:-1] # La última línea tiene \n por finOk
      if s== esperado:
        return False
    return True

  def muestraSalida(self, esperado, encontrado, tituloEsperado, tituloEncontrado):
    self.salida.write("---------------------------------------\n")
    self.salida.write(tituloEsperado+"\n")
    if len(esperado)== 0:
      self.salida.write(colorea(ROJO, "Ninguna")+"\n")
    else:
      for l in esperado:
        self.salida.write("  %s\n" % l)
    self.salida.write("--\n")
    self.salida.write(tituloEncontrado+"\n")
    if encontrado== "":
      self.salida.write(colorea(ROJO, "Ninguna")+"\n")
    else:
      s= encontrado.split("\n")
      if encontrado[-1]=="\n":
        s= s[:-1]
      for l in s:
        self.salida.write("  %s\n" % l)

  def presentaSalida(self, salidaEncontrada, errorEncontrado):
    if not self.vistaEntrada:
      esalida= self.errorEnSalida("", salidaEncontrada)
      eerror= self.errorEnSalida("", errorEncontrado)
    else:
      esalida= self.errorEnSalida(self.salidaEsperada, salidaEncontrada)
      eerror= self.errorEnSalida(self.errorEsperado, errorEncontrado)
    if esalida or eerror:
      self.nerrores+= 1
    if ( not self.mostrarTodas and not esalida
         and not eerror):
      return
    if not self.vistaEntrada:
      self.salida.write(colorea(ROJO,"Antes de la primera entrada\n"))
      if esalida:
        self.muestraSalida("", salidaEncontrada, "Salida esperada:", "Salida encontrada:")
      if eerror:
        self.muestraSalida("", errorEncontrado, "Salida de error esperada:", "Salida de error encontrada:")
    else:
      self.salida.write("Línea: %s\n" % colorea(VERDE,str(self.nlinea)))
      self.salida.write("Entrada: %s\n" % self.entrada.rstrip())
      if esalida or self.mostrarTodas:
        self.muestraSalida(self.salidaEsperada, salidaEncontrada,
                           "Salida esperada:", "Salida encontrada:")
      else:
        self.salida.write("Salida estándar: " + colorea(VERDE, "correcta\n"))
      if eerror or self.mostrarTodas:
        self.muestraSalida(self.errorEsperado, errorEncontrado,
                             "Salida de error esperada:", "Salida de error encontrada:")
      else:
        self.salida.write("---------------------------------------\n")
        self.salida.write("Salida de error: " + colorea(VERDE, "correcta\n"))
    self.salida.write(self.barra(""))

  def entradaNoLeida(self):
    self.salida.write("Línea: %s\n" % colorea(VERDE, str(self.nlinea+1)))
    self.salida.write(colorea(ROJO, "Termina el programa y no se ha leído toda la entrada\n"))
    self.salida.write(self.barra(""))
    self.nerrores += 1

  def trataEOF(self):
    if self.nerrores== 0:
      m= colorea(VERDE, "No ha habido errores")
    elif self.nerrores == 1:
      m= colorea(ROJO, "Ha habido un error")
    else:
      m= colorea(ROJO, "Ha habido %d errores" % self.nerrores)
    self.salida.write(m+"\n")
    self.salida.write(self.barra(" FIN "))

  def barra(self, m):
    return colorea(MAGENTA,"==%s%s\n" % (m, max(1, 40-len(m)-2)*"="))

class Generador(Procesador):
  """Genera la salida en el formato adecuado para ser utilizado con -e"""
  def __init__(self, salida, separaCampos, separaError):
    self.salida= salida
    self.separaCampos= separaCampos
    self.separaError= separaError
    self.nlinea = 0

  def trataLinea(self, l, nlinea):
    self.entrada= l
    self.nlinea = nlinea
    return l

  def presentaSalida(self, salidaEncontrada, errorEncontrado):
    fin= ""
    if len(self.entrada)!= "" and self.entrada[-1]== "\n":
      self.entrada= self.entrada[:-1]
      fin="\n"
    self.salida.write(self.entrada)
    if salidaEncontrada!= "":
      self.salida.write(" "+self.separaCampos+" ")
      if salidaEncontrada!= "" and salidaEncontrada[-1]=="\n":
        salidaEncontrada= salidaEncontrada[:-1]
      self.salida.write((" "+self.separaCampos+" ").join(salidaEncontrada.split("\n")))
    if errorEncontrado!= "":
      self.salida.write(" "+self.separaError+" ")
      if errorEncontrado!= "" and errorEncontrado[-1]=="\n":
        errorEncontrado= errorEncontrado[:-1]
      self.salida.write((" "+self.separaError+" ").join(errorEncontrado.split("\n")))
    self.salida.write(fin)

  def entradaNoLeida(self):
    raise Exception ("Hay entrada no leída en modo generador (última línea procesada: %d)" % self.nlinea)

  def trataEOF(self):
    pass


################################################################################
#
# Pruebas simples:
#

def pruebaSimple(options, args):
  if len(args)== 0:
    error("Necesito al menos el nombre del programa")
  programa= args[0]
  entrada= None
  salidaEsperada= None
  errorEsperado= None
  esDirectorio= False
  if len(args)==1:
    pass
  elif os.path.isdir(args[1]):
    esDirectorio= True
  else:
    if len(args)== 2:
      salidaEsperada= args[1]
    elif len(args)== 3:
      entrada= args[1]
      salidaEsperada= args[2]
    elif len(args)== 4:
      entrada= args[1]
      salidaEsperada= args[2]
      errorEsperado= args[3]
    else:
      error("Demasiados argumentos")
  if esDirectorio:
    bien= 0
    mal= 0
    for directorio in args[1:]:
      d= {}
      for nfichero in sorted(os.listdir(directorio)):
        (nombre, sufijo)= os.path.splitext(nfichero)
        if sufijo!= "":
          sufijo= sufijo[1:]
        fichero= os.path.join(directorio, nfichero)
        t= d.get(nombre, (None,None,None))
        if sufijo== options.sufijoEntrada:
          d[nombre]= (fichero, t[1], t[2])
        elif sufijo== options.sufijoSalida:
          d[nombre]= (t[0], fichero, t[2])
        elif sufijo== options.sufijoError:
          d[nombre]= (t[0], t[1], fichero)
      for (entrada, salidaEsperada, errorEsperado) in sorted(d.values()):
        if len(options.argumentos) > 0:
          linea = programa + " " + " ".join(options.argumentos)
        else:
          linea = programa
        if options.argumento and entrada!= None:
          r= ejecutaPrograma(linea+" "+entrada, None, salidaEsperada, errorEsperado)
        else:
          r= ejecutaPrograma(linea, entrada, salidaEsperada, errorEsperado)
        if r:
          bien+= 1
        else:
          mal+= 1
    print colorea(MAGENTA, "===========================\n")
    print colorea(AZUL, "Probados %d ficheros" % (bien+mal))
    if mal== 0:
      print colorea(VERDE, "Todos correctos")
    else:
      print colorea(VERDE, "Correctos: %d" % bien)
      print colorea(ROJO, "Erróneos: %d" % mal)
  else:
    if options.argumento and entrada!= None:
      ejecutaPrograma(programa+ " "+entrada, None, salidaEsperada, errorEsperado)
    else:
      ejecutaPrograma(programa, entrada, salidaEsperada, errorEsperado)

def ejecutaPrograma(nombre, entrada, salidaEsperada, errorEsperado):
  print colorea((AZUL,BRILLANTE), "Ejecutando %s" % nombre)
  if entrada!= None:
    print "- Fichero de entrada: %s" % entrada
  if salidaEsperada!= None:
    print "- Salida esperada: %s" % salidaEsperada
  if errorEsperado!= None:
    print "- Error esperado: %s" % errorEsperado

  fentrada= abreONone(entrada)
  fsalidaEsperada= abreONone(salidaEsperada)
  ferrorEsperado= abreONone(errorEsperado)

  fsalida= os.tmpfile()
  ferror= os.tmpfile()

  try:
    programa= Popen(nombre.split(), shell=False, stdin=fentrada, stdout=fsalida, stderr=ferror)
  except OSError, e:
    error("No he podido ejecutar %s, (%s)" % (nombre,e))

  codigo= programa.wait()
  fsalida.seek(0)
  ferror.seek(0)

  print colorea((AZUL,BRILLANTE), "Resultado:")
  vaBien= True
  if codigo!= 0:
    print colorea(AMARILLO, "Código de error %d" % codigo)
    # vaBien= False
  r= comparaFicheros("- Salida estándar:", fsalidaEsperada, fsalida)
  vaBien= vaBien and r
  r= comparaFicheros("- Salida de error:", ferrorEsperado, ferror)
  vaBien= vaBien and r
  return vaBien

################################################################################
#
# Pruebas entrelazadas:
#

def pruebaEntrelazado(options, args):
  salida= sys.stdout
  if len(args)== 0:
    error("Necesito al menos un parámetro, el nombre del programa")
  elif len(args)== 1:
    ejecutaEntrelazado(args[0], sys.stdin, salida, options, "stdin")
  else:
    for e in args[1:]:
      if not os.path.isdir(e):
        entrada= abre(e)
        ejecutaEntrelazado(args[0], entrada, salida, options, e)
      else: # Es un directorio
        for nfichero in sorted(os.listdir(e)):
          (nombre, sufijo)= os.path.splitext(nfichero)
          if sufijo!= "":
            sufijo= sufijo[1:]
          if sufijo== options.sufijoEntrelazado:
            fichero= os.path.join(e, nfichero)
            entrada= abre(fichero)
            ejecutaEntrelazado(args[0], entrada, salida, options, fichero)

def ejecutaEntrelazado(programa, entrada, salida, options, nombre):
  # Nos guardamos los ficheros originales
  stdout= sys.stdout
  stdin= sys.stdin
  stderr= sys.stderr

  # Preparamos las redirecciones
  sys.stdout=RedirigeSalida(salida)
  sys.stderr=RedirigeSalida(salida)
  if options.genera:
    procesador= Generador(stdout, options.separaCampos, options.marcaError)
  else:
    procesador= Comprobador(stdout, options.todas, options.separaCampos, options.marcaError, nombre)
  sys.stdin=RedirigeEntrada(entrada, sys.stdout, sys.stderr, procesador)

  # Guardamos sys.argv y construimos el del programa
  argv= sys.argv[:]
  sys.argv=[programa] + options.argumentos
  path= os.path.dirname(programa)
  if not path in sys.path:
    sys.path.append(path)

  # Anotamos qué modulos había antes de la ejecución
  modules= sys.modules.keys()

  # Prepara el entorno de ejecución
  globales={}
  # Fuerza la ejecución de programas guardados con if __name__=="__main__"
  globales["__name__"]="__main__"
  try:
    execfile(programa, globales)
  except SystemExit:
    pass
  except:
    import traceback
    sei= sys.exc_info()
    traceback.print_exception(sei[0],sei[1],sei[2])

  # Limpiamos los restos que pudieran quedar de la ejecucion
  for i in sys.modules.keys():
    if not i in modules:
      del sys.modules[i]
  sys.stdout= stdout
  sys.stdin= stdin
  sys.stderr= stderr
  sys.argv= argv

################################################################################
#
# Comparaciones
#

class Comparacion:
  """Guarda los resultados de una comparación"""
  def __init__(self, _iguales, _diferencias):
    self._iguales= _iguales
    self._diferencias= _diferencias

  def iguales(self):
    """Cierto si ambos ficheros son iguales"""
    return self._iguales

  def diferencias(self):
    """Diferencias entre los ficheros"""
    return self._diferencias

  def __str__(self):
    if self._iguales:
      return "Iguales"
    else:
      return "".join([str(d) for d in self._diferencias])

  def pretty(self, linRef, linObtenido):
    if self._iguales:
      return "Iguales"
    else:
      return "".join([d.pretty(linRef, linObtenido) for d in self._diferencias])

def nlineas(n):
  """Escribe n líneas o línea según el valor de n"""
  if n==0:
    return "cero líneas"
  elif n==1:
    return "una línea"
  elif n==2:
    return "dos líneas"
  else:
    return "%d líneas" % n

def s(n):
  """Devuelve s si n!= 1"""
  if n!= 1:
    return "s"
  else:
    return ""

class Diferencia:
  """Una diferencia"""
  def __init__(self, posRef, tallaRef, posObtenido, tallaObtenido):
    """Guarda la posición y líneas de los ficheros"""
    self.posRef= posRef
    self.tallaRef= tallaRef
    self.posObtenido= posObtenido
    self.tallaObtenido= tallaObtenido

  def esVacia(self):
    return self.tallaRef== 0 and self.tallaObtenido== 0

  def __add__(self, other):
    if (self.posRef+self.tallaRef!= other.posRef or
        self.posObtenido+self.tallaObtenido!= other.posObtenido):
      return self, other
    return Diferencia(self.posRef, self.tallaRef+other.tallaRef,
                      self.posObtenido, self.tallaObtenido+other.tallaObtenido)

  def pretty(self, linRef, linObtenido):
    sr= s(self.tallaRef)
    nr= nlineas(self.tallaRef)
    so= s(self.tallaObtenido)
    no= nlineas(self.tallaObtenido)
    lineasRef= "".join([" - "+l for l in linRef[self.posRef-1:self.posRef-1+self.tallaRef]])
    lineasObt= "".join([" + "+l for l in linObtenido[self.posObtenido-1:self.posObtenido-1+self.tallaObtenido]])
    if self.tallaRef!= 0:
      if self.tallaObtenido!= 0:
        r= "** %s cambiada%s; en la posición %d de la referencia pone:\n" % (nr, sr, self.posRef)
        r+= lineasRef
        r+="*  y en la posición %d de la salida pone:\n" % self.posObtenido
        r+= lineasObt
      else:
        r= ( "** borrada%s %s en la posición %d de la referencia:\n" % (sr, nr, self.posRef))
        r+= lineasRef
    else:
      if self.tallaObtenido!= 0:
        r= ( "** %s inesperada%s en la posición %d de la salida:\n" %
             (no, so, self.posObtenido))
        r+= lineasObt
      else:
        r= "** diferencia vacía en %d y %d" % (self.posRef, self.posObtenido)
    return r

  def __str__(self):
    return "Diferencia"


class ListaDiferencias:
  """Almacena una lista de diferencias de manera persistente"""
  def __init__(self, c= None, a= None):
    self.contenido= c
    self.anterior= a

  def esVacia(self):
    return self.contenido== None and self.anterior==None

  def append(self, d):
    """Añade d, que es una diferencia, al final de la lista"""
    if d.esVacia():
      return self
    if self.esVacia():
      return ListaDiferencias(d, None)
    d2= self.contenido+d
    if type(d2)== type(d):
      return ListaDiferencias(d2, self.anterior)
    else:
      return ListaDiferencias(d, self)

  def __iter__(self):
    if self.anterior!= None:
      for d in self.anterior:
        yield d
    if self.contenido!= None:
      yield self.contenido

def muestra(l):
  for puntos,difs in l:
    print "  ",puntos,[str(d) for d in difs]

def comparaFicheros(titulo, fRef, fObtenido):
  if fRef!= None:
    lRef= fRef.readlines()
  else:
    lRef= []
  if fObtenido!= None:
    lObtenidas= fObtenido.readlines()
  else:
    lObtenidas= []
  comparacion= comparaLineas(lRef, lObtenidas)
  print titulo,
  if comparacion.iguales():
    print colorea(VERDE, "correcta")
  else:
    print colorea(ROJO, "errores")
    print comparacion.pretty(lRef, lObtenidas)
  return comparacion.iguales()

def comparaLineas(lReferencia, lObtenidas):
  actual= [(0,ListaDiferencias())]
  for posRef in range(len(lReferencia)):
    posRef+= 1
    ld= actual[-1][1].append(Diferencia(posRef, 1, 1, 0))
    actual.append((actual[-1][0]+1,ld))
  posObtenida= 0
  for lObtenida in lObtenidas:
    anterior= actual
    posObtenida+= 1
    ld= ListaDiferencias()
    ld= ld.append(Diferencia(1, 0, 1, posObtenida))
    actual= [(anterior[0][0]+1, ld)]
    posRef= 0
    for lRef in lReferencia:
      posRef+=1
      ins= anterior[posRef][0]+1
      if lRef== lObtenida:
        sust= anterior[posRef-1][0]
      else:
        sust= anterior[posRef-1][0]+1
      borr= actual[-1][0]+1
      puntos= min(ins, sust, borr)
      if puntos== sust:
        ld= anterior[posRef-1][1]
        if lRef== lObtenida:
          diferencia= Diferencia(posRef, 0, posObtenida, 0)
        else:
          diferencia= Diferencia(posRef, 1, posObtenida, 1)
      elif puntos== borr:
        ld= actual[-1][1]
        diferencia= Diferencia(posRef, 1, posObtenida, 0)
      elif puntos== ins:
        ld= anterior[posRef][1]
        diferencia= Diferencia(posRef, 0, posObtenida, 1)
      actual.append((puntos, ld.append(diferencia)))
  if actual[-1][0]== 0:
    return Comparacion(True, [])
  else:
    return Comparacion(False, actual[-1][1])

################################################################################
#
# Principal:
#

def analizaSufijos(options):
  c= options.sufijos.split(",")
  if len(c)!= 3:
    error("La cadena pasada a --sufijos tiene que tener tres componentes separados por comas")
  options.sufijoEntrada= c[0]
  options.sufijoSalida= c[1]
  options.sufijoError= c[2]

def main():
  parser= OptionParser(usage= "%prog [<opciones>] <programa> [ [<entrada>] <salida> [<error>] ] | {<directorio>} ]")
  parser.add_option("-a", "--argumento", action="store_true", default= False,
                    help= u"el fichero de entrada se pasa como argumento al programa, sin efecto en el modo entrelazado. Si se usa con -A, el fichero de entrada es el último argumento.")
  parser.add_option("-A", "--argumentos", type="string", default=None,
                    help= u"lista de argumentos que se pasan al programa, separados por blancos. Por defecto no se le pasa ninguno")
  parser.add_option("-E", "--marcaError", type="string", default="@*",
                    help= u"separador de las líneas de error en modo entrelazado, por defecto: %default.")
  parser.add_option("-e", u"--entrelazado", action="store_true", default= False,
                    help= u"utilizar el modo entrelazado.")
  parser.add_option("-g", u"--genera", action="store_true", default= False,
                    help= u"generar la salida en el formato adecuado para entrelazado (implica -e).")
  parser.add_option("-n", u"--noColores", action="store_true", default= False,
                    help= u"no utilizar colores en la salida.")
  parser.add_option("-S", "--separaCampos", type="string", default= "@@",
                    help= u"separador de los campos en modo entrelazado, por defecto: %default.")
  parser.add_option("-s", "--sufijos", type="string", default="i,o,e",
                    help= u"sufijos de los ficheros de entrada, salida y error, por defecto: %default.")
  parser.add_option("-t", u"--todas", action="store_true", default= False,
                    help= u"en modo entrelazado, muestra todas las líneas incluso si no hay diferencias respecto a lo esperado.")
  parser.add_option("-x", u"--sufijoEntrelazado", type="string", default="pr",
                    help= u"sufijo de los ficheros con pruebas entrelazadas, por defecto: %default.")

  (options, args)= parser.parse_args()
  if options.genera:
    options.entrelazado= True
  global noColores
  noColores= options.noColores

  if options.argumentos is None:
    options.argumentos = []
  else:
    options.argumentos = options.argumentos.split()

  print options
  print args
  analizaSufijos(options)
  if options.entrelazado:
    pruebaEntrelazado(options, args)
  else:
    pruebaSimple(options, args)

if __name__== "__main__":
  main()
