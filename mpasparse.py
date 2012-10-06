# Yacc

import ply.yacc as yacc

# Get the token map from the lexer.  This is required.
from calclex import tokens

#  ---------------------------------------------------------------
#  ABSTRACT SYNTAX TREE - NODE
#  ---------------------------------------------------------------

class Node:
	def __init__(self, name, children = None, leaf = None):
		self.name = name
		if children == None:
			children = []
		self.children = children
		self.leaf = leaf
	
	def __str__(self):
		return "<%s>" % self.name

	def __repr__(self):
		return "<%s>" % self.name

	def append(self, node):
		self.children.append(node)

#  ---------------------------------------------------------------
#  ABSTRACT SYNTAX TREE - TYPE SYSTEM
#  ---------------------------------------------------------------

# -----------------------------------------------------------------------------
# Esta funcion de utilidad imprime el AST
# -----------------------------------------------------------------------------

def dump_tree(node, indent = ""):

	if not hasattr(node, "datatype"):
		datatype = ""
	else:
		datatype = node.datatype

	if not node.leaf:
		print "%s%s  %s" % (indent, node.name, datatype)
	else:
		print "%s%s (%s)  %s" % (indent, node.name, node.leaf, datatype)

	indent = indent.replace("-"," ")
	indent = indent.replace("+"," ")
	for i in range(len(node.children)):
		c = node.children[i]
		if i == len(node.children)-1:
			dump_tree(c, indent + "  +-- ")
		else:
			dump_tree(c, indent + "  |-- ")

# -----------------------------------------------------------------------------
# Parser
# -----------------------------------------------------------------------------
def type_float():
	pass

#---------------exprelist---------------------------------------
def exprelist_coma():
   ' exprelist: expre ; exprelist'
   p[1].append(p[3])
	p[0] = p[1]

def exprelist_():
	'exprelist: expre'
	p[0] = p[1]


#---------------expre----------------------------------------------
def p_expre_mas(p):
	'expre: expre MAS expre'
	p[0]= Node('+',p[2],p[3])

def p_expre_menos(p):
	'expre: expre MENOS expre'
	p[0]= Node('-',p[2],p[3])

def p_expre_mul(p):
	'expre: expre MUL expre'
	p[0]= Node('*',p[2],p[3])

def p_expre_div(p):
	'expre: expre DIV expre'
	p[0]= Node('/',p[2],p[3])

def p_expre_masu(p):
	'expre: MAS expre'
	p[0]= Node('',p[2])

def p_expre_menosu(p):
	'expre: MENOS expre'
	p[0]= Node('-',p[2],p[3])


# def p_expre_call(p):
# 	'expression : ID PARI expre PARD'
#  	p[0]= Node('call',p[1],p[3])

def p_expre_id():
	'expre: ID'
	p[0] = Node('id',[],p[1])


def p_expre_cast_int():
	'expre: ID CORI exprelist CORD'
	p[0] = Node('cast_int',p[3],p[])

def p_expre_fnum():
	'expre: FNUM'
	p[0]= Node(numero_flotante,p[1])

def p_expre_inum():
	'expre: INUM'
	p[0]= Node(numero,p[1])

def p_expre_cast_float():
	'expre: ID CORI exprelist CORD'
	p[0] = Node('cast_float',p[3],p[])

def p_expre_mul2():
	'expre: ID CORI exprelist CORD'
	p[0] = Node(mul_cor_fum,p[1],p[3])
	if p[3].typ != 'int'
	 print "!ERROR¡ se esperava un entero" 
				


def p_expre_expre(p):
	'expre: expre MAS expre'
	p[0]= Node('+',p[2],p[3])

#------------------------------------------------------------------
	pass
# Error rule for syntax errors
def p_error(p):
    print "Syntax error in input!"

# Build the parser
parser = yacc.yacc(debug=1)

while True:
   try:
       s = raw_input('calc > ')
   except EOFError:
       break
   if not s: continue
   result = parser.parse(s)
   dump_tree(result)