#-----------------------------------------------------------------------------
# Name:        mpascal.py
# Purpose:
#
# Author:      Daniel Bernal - Jonathan Alvarez
#
# Created:     12/09/2012
# Copyright:   (c) Daniel Bernal - Jonathan Alvarez 2012
# Licence:     Free share
#-----------------------------------------------------------------------------

import ply.lex as lex
import symtab

debug = False

keywords = (
    'INT', 'FLOAT', 'WHILE', 'IF', 'THEN', 'ELSE', 'BEGIN', 'DO', 'END', 'PRINT', 'WRITE', 'READ', 'SKIP', 'RETURN', 'BREAK', 'AND', 'OR', 'NOT', 'FUN', 'ID',
)

tokens = keywords + (
    'LT', 'LE', 'GT', 'GE', 'EQ', 'NE', 'MAS', 'MENOS', 'DIV', 'MUL', 'PARI', 'PARD', 'COMA', 'DPUN', 'CORI', 'CORD', 'PCOMA', 'PUN', 'ASIG', 'INUM', 'FNUM', 'STRING', 'COMEN'
)

t_ignore = ' \t'

t_LT = r'\<'
t_LE = r'<='
t_GT = r'\>'
t_GE = r'=>'
t_EQ = r'='
t_NE = r'!='
t_MAS = r'\+'
t_MENOS = r'-'
t_DIV = r'/'
t_MUL = r'\*'
t_PARI = r'\('
t_PARD = r'\)'
t_COMA = r'\,'
t_DPUN = r':'
t_CORI = r'\['
t_CORD = r'\]'
t_PCOMA = r';'
t_PUN = r'\.'
t_ASIG = r'\:='


def t_FNUM(t):
    r'((\d*\.\d+)(E|e[\+-]?\d+)?|([1-9]\d*E|e[\+-]?\d+))'
    try :
        t.value = float(t.value)
    except ValueError:
        print ( "Numero mal formado. Error de Valor. linea %s" % t.lineno )
    else:
        return t

def t_INUM(t):
    r'[0-9]+[^a-zA-Z_\-;\:\)\]\,]?'
    try :
        t.value = int(t.value)
    except ValueError:
        print ( "Numero mal formado. Error de Valor. linea %s" % t.lineno )
    else:
        return t

def t_error_ID(t):
    r'\d+[a-zA-Z_]*'
    print ( ">>ERROR: Identificador mal formado linea %s" % t.lineno )
    t.lexer.skip(1)

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value.upper() in keywords:
        t.type = t.value.upper()
    # Agrega el ID a la tabla de simbolos
    else: 
        t.type = 'ID'
        symtab.attach_symbol(t)
    return t

def is_valid_STRING(t):
    s = str(t.value)
    i = 0
    #Escapes no validos.
    s = s[1:-1] #avoid '"'
    while s.find("\\") != -1 :
        i = s.find("\\") + 1 #get next char after '\'
        s = s[i:]
        tok = str(s[:1])
        if tok != "n" and tok != "\"" and tok != "\\":
            print (">>ERROR Secuencia de escape de STRING no valido \\%s" % tok )
            print (">>>> Linea %s" % t.lineno)
            return False
        if tok == "\\" :
            s = s[1:]
    return True

def t_STRING(t):
    r'\".*\"'
    if is_valid_STRING(t) :
        return t
    else :
        t.lexer.skip(1)

def t_error_STRING(t):
    r'\".*'
    print (">>ERROR Formacion STRING incorrecta, linea: %s" % t.lineno )
    t.lexer.skip(1)

def t_COMEN(t):
    r'/\*(.|\n|\"|\\)*?\*/'
    return t

def t_error_COMEN(t):
    r'/\*(.|\n|\"|\\)*?'
    print ( ">>ERROR: Comentario mal formado linea %s, linea no valida" % t.lineno )
    t.lexer.skip(1)

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print(">>ERROR: Caracter no valido %s" % t.value[0])
    print(">>>>> linea %s" %  t.lineno)
    t.lexer.skip(1)

# Build

lexer = lex.lex(debug=0)
symtab.new_scope()

if __name__ == '__main__':
    try: 
        lex.runmain()
        print( "\n^^^^^^^^^^^^^^^^^^^^^^^" )
        print( "Analisis completo. Los errores se marcan arriba." )
    except IOError as e:
        print ("I/O error({0}): {1}".format(e.errno, e.strerror))