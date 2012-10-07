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

#  ---------------------------------------------------------------
#  LOCATION
#  ---------------------------------------------------------------

def p_location_1(p):
	'location: ID'
	p[0] = Node('ID',[],p[1])

def p_location_2(p):
	'location: ID CORI expre CORD'
	p[0] = Node('ID[]',[],p[1])

#  ---------------------------------------------------------------
#  RELACION
#  ---------------------------------------------------------------

def p_relacion_condicion(p):
    'relacion: expre condicion expre'
     p[0] = Node('relacion_condicion', [p[1],p[3]])

def p_relacion_lt(p):
	'relacion: expre LT expre'
	 p[0] = Node('<',[p[1],p[3]])

def p_relacion_le(p):
	'relacion: expre LE expre'
	 p[0] = Node('<=',[p[1],p[3]])

def p_relacion_gt(p):
	'relacion: expre GT expre'
	 p[0] = Node('>',[p[1],p[3]])

def p_relacion_ge(p):
	'relacion: expre GE expre'
	 p[0] = Node('>=',[p[1],p[3]])

def p_relacion_eq(p):
	'relacion: expre EQ expre'
	 p[0] = Node('=',[p[1],p[3]])

def p_relacion_ne(p):
	'relacion: expre NE expre'
	 p[0] = Node('!=',[p[1],p[3]])	 

def p_relacion_and(p):
	'relacion: relacion AND relacion'
	 p[0] = Node('and',[p[1],p[3]])

def p_relacion_or(p):
	'relacion: relacion OR relacion'
	 p[0] = Node('or',[p[1],p[3]])

def p_relacion_not(p):
	'relacion: NOT relacion'
	p[0] =node('not',[p[2]])

def p_relacion_parent(p):
	'relacion: PARI relacion PARD'
	p[0] =node('relacion',[p[2]])

#  ---------------------------------------------------------------
#  TYPE
#  ---------------------------------------------------------------

def p_type_f(p):
	'type: FLOAT'
	p[0] = Node('FLOAT',[],p[1])

def p_type_i(p):
	'type: INT'
	p[0] = Node('INT',[],p[1])

def p_type_fa(p):
	'type: FLOAT CORI expre CORD'
	p[0] = Node('FLOAT_Array',[],p[3])

def p_type_ia(p):
	'type: INT CORI expre CORD'
	p[0] = Node('INT_Array',[],p[3])

#  ---------------------------------------------------------------
#  EXPRLIST
#  ---------------------------------------------------------------

def p_exprelist_coma(p):
   'exprelist: exprelist COMA expre'
	p[0] = p[1].append(p[3])

def p_exprelist_(p):
	'exprelist: expre'
	p[0] = p[1]
	
#  ---------------------------------------------------------------
#  EXPRE
#  ---------------------------------------------------------------

def p_expre_mas(p):
	'expre: expre MAS expre'
	p[0]= Node('+',[p[1],p[3]])

def p_expre_menos(p):
	'expre: expre MENOS expre'
	p[0]= Node('-',[p[1],p[3]])
 
def p_expre_mul(p):
	'expre: expre MUL expre'
	p[0]= Node('*',[p[1],p[3]])

def p_expre_div(p):
	'expre: expre DIV expre'
	p[0]= Node('/',[p[1],p[3]])
 
 def p_expre_menosu(p):
	'expre: MENOS expre'
	p[0]= Node('umenos',[p[2]])

def p_expre_masu(p):
	'expre: MAS expre'
	p[0]= Node('umas',[p[2]])

def p_expre_call(p):
	'expre: ID PARI exprelist PARD'
	#TODO
	p[0] = Node('call',[p[3]],p[1])

def p_expre_id(p):
	'expre: ID'
	p[0] = Node('id', [], p[1])
	p[0].value = p[1]

def p_expre_array(p):
	'expre: ID CORI exprelist CORD'
	p[0] = Node('array',[p[3]],p[1])

	#indices enteros
	if hasattr(p[3],'typ'):
		if p[3].typ != 'int':
			print "#Error# El indice del array debe ser un valor entero '%s'" % f.name
		else:
			p[0].typ = p[3].typ

def p_expre_fnum(p):
	'expre: FNUM'
	p[0]= Node('numero_f',p[1])

def p_expre_inum(p):
	'expre: INUM'
	p[0]= Node('numero',p[1])

def p_expre_cast_int(p):
	'expre: INT PARI expre PARD'
	p[0] = Node('cast_int',[p[3]],p[1])

def p_expre_cast_float(p):
	'expre: FLOAR PARI expre PARD'
	p[0] = Node('cast_float',[p[3]],p[1])


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
#  PARSER
# -----------------------------------------------------------------------------

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