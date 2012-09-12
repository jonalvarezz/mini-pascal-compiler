lista de todos los tokens
==========================

INUMBER ::= '\d+'

Gramatica independiente del contexto
=====================================

assing	::= ID := expr

expr	::= expr + expr
	| expr - expr
	| expr * expr
	| expr / expr
	| (expr)
	| ID