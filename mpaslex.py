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
	'LT', 'LE', 'GT', 'GE', 'EQ', 'NE', 'MAS', 'MENOS', 'DIV', 'MUL', 'PARI', 'PARD', 'COMA', 'DPUN', 'CORI', 'CORD', 'PCOMA', 'PUN'
)




