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

import sys
import ply.lex as lex

debug = False

keywords = (
	'INT', 'int', 'FLOAT', 'float', 'WHILE', 'while', 'IF', 'if', 'THEN', 'then', 'ELSE', 'else', 'BEGIN', 'begin', 'DO', 'do', 'END', 'end', 'PRINT', 'print', 'WRITE', 'write', 'READ', 'read', 'SKIP', 'skip', 'RETURN', 'return', 'BREAK', 'break', 'AND', 'and', 'OR', 'or', 'NOT', 'not', 'FUN', 'fun', 'ID', 'id',
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
    r'((\d*\.\d+)(E[\+-]?\d+)?|([1-9]\d*E[\+-]?\d+))'
    t.value = float(t.value)
    return t

def t_INUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING(t):
    r'\".*\"'
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value in keywords:
        t.type = t.value
    return t

# TODO: Manejo de errores
def t_COMEN(t):
    r'/\*(.|\n|\"|\\)*?\*/'
    return t
#    pass

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("Illegal character %s" % t.value[0])
    t.lexer.skip(1)

# Build

if len(sys.argv) > 1:
    lexer = lex.lex(debug=1)
    try:
        dato = open(sys.argv[1], "r")
    except IOError as e:
        print ("I/O error({0}): {1}".format(e.errno, e.strerror))

    else:
        if debug : print(dato.read())

        lexer.input(dato.read())
        dato.close()

        # Tokenize
        for tok in lexer:
            print (tok)

        #print ( "Numero de lineas: %i" % tok.lexer.lineno )

else:
    print ("File argument expected. Usage:")
    print ("python mpaslex.py <file>")