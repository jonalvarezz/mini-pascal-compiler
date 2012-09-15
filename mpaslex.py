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

keywords = (
	'INT', 'FLOAT', 'WHILE', 'IF', 'THEN', 'ELSE', 'BEGIN', 'DO', 'END', 'PRINT', 'WRITE', 'READ', 'SKIP', 'RETURN', 'BREAK', 'AND', 'OR', 'NOT', 'FUN', 'ID',
)

tokens = keywords + (
	'LT', 'LE', 'GT', 'GE', 'EQ', 'NE', 'MAS', 'MENOS', 'DIV', 'MUL', 'PARI', 'PARD', 'COMA', 'DPUN', 'CORI', 'CORD', 'PCOMA', 'PUN', 'ASIG', 'INUM', 'FNUM', 'STRING', 'COMEN'
)

t_ignore = ' \t'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9]_'
    if t.value in keywords:
        t.type = t.value
    return t

t_LT = r'<'
t_LE = r'<='
t_GT = r'>'
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
t_ASIG = r':='

t_FNUM = r'((\d*\.\d+)(E[\+-]?\d+)?|([1-9]\d*E[\+-]?\d+))'
t_STRING = r'\".\"'

# TODO: Manejo de errores
t_COMEN = r'/\*(.|\n|\"|\\)*?\*/'

def t_NEWLINE(t):
    r'\n'
    t.lexer.lineno += 1
    return t


def t_error(t):
    print("Illegal character %s" % t.value[0])
    t.lexer.skip(1)

lex.lex()

for tok in lexer:
    print tok

print "Numero de lineas: %i" % tok.lexer.lineno

