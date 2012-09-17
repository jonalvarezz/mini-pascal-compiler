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
    r'((\d*\.\d+)(E|e[\+-]?\d+)?|([1-9]\d*E|e[\+-]?\d+))'
    t.value = float(t.value)
    return t

def t_INUM(t):
    r'[0-9]+[^a-zA-Z_]'
    t.value = int(t.value)
    return t

def t_error_ID(t):
    r'\d+[a-zA-Z_-]*'
    print ( "ERROR: Identificador mal formado linea %s" % t.lineno )
    t.lexer.skip(1)


def t_ID(t):
    r'[a-zA-Z_-][a-zA-Z0-9_-]*'
    if t.value in keywords:
        t.type = t.value
    return t

def t_STRING(t):
    r'\".*\"'
    return t


# TODO: Manejo de errores
def t_error_COMEN(t):
    r'/\*(.|\n|\"|\\)*?'
    print ( "ERROR: Comentario no cerrado linea: %s" % t.lineno )
    t.lexer.skip(1)

def t_COMEN(t):
    r'/\*(.|\n|\"|\\)*?\*/'
    return t
#    pass

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("ERROR: Caracter no válido %s" % t.value[0])
    t.lexer.skip(1)

# Build

lexer = lex.lex(debug=0)

if __name__ == '__main__':
    try: 
        lex.runmain()
    except IOError as e:
        print ("I/O error({0}): {1}".format(e.errno, e.strerror))