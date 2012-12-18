# Yacc
import ply.yacc as yacc
import sys
from mpaslex import tokens
import symtab
import mpastype
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

def dump_tree(node, indent = ""):

	if not hasattr(node, "typ"):
		datatype = ""
	else:
		if node.typ == 'error':
			datatype = node.typ
		elif node.typ[1] :
			datatype = str(node.typ[0]) + "_" + str(node.typ[1])
		else:
			datatype = node.typ[0]
	try:
		if not node.leaf:
			print ("%s %s  %s" % (indent, node.name, datatype))
		else:
			print ("%s%s (%s)  %s" % (indent, node.name, node.leaf, datatype))

		indent = indent.replace("-"," ")
		indent = indent.replace("+"," ")
		for i in range(len(node.children)):
			c = node.children[i]
			if i == len(node.children)-1:
				dump_tree(c, indent + "  +-- ")
			else:
				dump_tree(c, indent + "  |-- ")

	except AttributeError:
		print( 'Error de atributo en el nodo: %s, tipo de dato: %s' % (node, datatype))
		

#  ---------------------------------------------------------------
#  PRECEDENCIAS
#  ---------------------------------------------------------------

precedence =(
	('left', 'OR'),
	('left', 'AND'),
    ('left', 'NOT'),
    ('left', 'MAS', 'MENOS'),
    ('left', 'MUL', 'DIV'),   
	('right', 'ELSE'),
)

#  ---------------------------------------------------------------
#  PROGRAMA
#  ---------------------------------------------------------------

def p_programa_0(p):
	'programa : funcionlista'
	p[0] = p[1]

#  ---------------------------------------------------------------
#  LISTA DE FUNCIONES
#  ------------------------------------------newtype('int')---------------------

def p_funcionlista_1(p):
	'''funcionlista : funcion'''
	p[0] = Node('programa',[p[1]])

def p_funcionlista_2(p):
	'''funcionlista : funcionlista funcion'''
	p[1].append(p[2])
	p[0] = p[1]

#  ---------------------------------------------------------------
#  FUNCION
#  ---------------------------------------------------------------

def p_funcion(p):
	'funcion : fundecl ID PARI argumento PARD locales BEGIN lineas END'
	p[0] = Node( 'funcion', [p[4], p[6], p[8]], p[2] )
	# Elimina la tabla de simbolos actual, y restaura la anterior.
	symtab.pop_scope()

def p_fundecl(p):
	'fundecl : FUN'
	# Crea una nueva tabla de simbolos
	symtab.new_scope()

#  ---------------------------------------------------------------
#  ARGUMENTO
#  ---------------------------------------------------------------

def p_argumento_0(p):
	'argumento : vacio'
	p[0] = Node( 'argumento()' )

def p_argumento_1(p):
	'argumento : declaracion'
	p[0] = p[1]

#  ---------------------------------------------------------------
#  DECLARACIONES
#  ---------------------------------------------------------------

def p_declaracion_0(p):
	'declaracion : dec'
	p[0] = Node( 'argumento', [p[1]] )

def p_declaracion_1(p):
	'declaracion : declaracion COMA dec'
	p[1].append(p[3])
	p[0] = p[1]

#  ---------------------------------------------------------------
#  LOCALES
#  ---------------------------------------------------------------

def p_locales_0(p):
	'locales : loclist PCOMA'
	p[0] = p[1]

def p_locales_1(p):
	'locales : vacio'
	p[0] = Node('locales')

#  ---------------------------------------------------------------
#  LOCLIST
#  ---------------------------------------------------------------

def p_loclist_0(p):
	'loclist : loc'
	p[0] = Node( 'loclist_dec', [p[1]] )
	p[0].name = p[1].name

def p_loclist_2(p):
	'loclist : loclist PCOMA loc'
	p[1].append(p[3])
	p[0] = p[1]

#  ---------------------------------------------------------------
#  LOC
#  ---------------------------------------------------------------

def p_loc_0(p):
	'loc : dec'
	p[0] = p[1]

def p_loc_1(p):
	'loc : funcion'
	p[0] = p[1]

#  ---------------------------------------------------------------
#  DEC
#  ---------------------------------------------------------------

def p_dec(p):
	'dec : ID DPUN type'
	p[0] = Node( 'declaracion', [p[3]], p[1] )

	p[0].name = p[1]
	p[0].value = p[1]
	p[0].typ = p[3].typ
	a = symtab.setid( p[0].name, p[3].typ )
	if not a :
		dir ( p[0] )
		print ( ">>ERROR: redeclaracion del identificador '%s'" % (p[0].name) )


#  ---------------------------------------------------------------
#  LINEAS
#  ---------------------------------------------------------------

def p_lineas_0(p):
	'lineas : linea'
	p[0] = Node('lineas', [p[1]])

def p_lineas_1(p):
	'lineas : lineas PCOMA linea'
	p[1].append(p[3])
	p[0] = p[1]

#  ---------------------------------------------------------------
#  LINEA
#  ---------------------------------------------------------------

def p_linea_0(p):
	'linea : expre'
	p[0] = Node( 'expre', [p[1]] )

def p_linea_1(p):
	'linea : WRITE PARI expre PARD'
	p[0] = Node( 'write', [p[3]] )

def p_linea_2(p):
	'linea : READ PARI location PARD'
	p[0] = Node( 'read', [p[3]] )

def p_linea_3(p):
	'linea : PRINT PARI STRING PARD'
	p[0] = Node( 'print', [], p[3] )

def p_linea_4(p):
	'linea : ID ASIG expre'
	p[0] = Node( ':=', [p[3]], p[1] )

	p[0].assign = 1

	# Validacion id no declarado.
	data = symtab.find_id( p[1] )
	if not data :
		print ( ">>ERROR: identificador '%s' no declarada." % p[1] )

	# Comprobacion asignacion de tipo
	p1 = symtab.get_id( p[1] )
	typ = symtab.comparate_types(p1, p[3])
	if typ == 'error' :
		print( ">>ERROR: Se esperaban expresiones del mismo tipo. linea: ")

def p_linea_5(p):
	'linea : RETURN expre'
	p[0] = Node( 'return', [p[2]], p[1] )

def p_linea_7(p):
	'linea : SKIP'
	p[0] = Node( 'skip', [p[1]] )

def p_linea_8(p):
	'linea : BREAK'
	p[0] = Node( 'break', [], p[1] )

def p_linea_9(p):
	'linea : WHILE relacion DO linea'
	p[0] = Node( 'while', [p[2], p[4]] )

def p_linea_10(p):
	'linea : IF relacion THEN linea else_r'
	p[0] = Node( 'if', [p[2], p[4], p[5]] )

def p_linea_11(p):
	'linea : BEGIN lineas END'
	p[0] = p[2]

#  ---------------------------------------------------------------
#  ELSE
#  ---------------------------------------------------------------

def p_else_0(p):
	'else_r : ELSE linea'
	p[0] = Node( 'else', [p[2]] )

def p_else_1(p):
	'else_r : vacio'
	p[0] = Node( 'else' )

#  ---------------------------------------------------------------
#  LOCATION
#  ---------------------------------------------------------------
#  bug detectado!!! no entra nunca por aki la funcion read coje id en ves de alguna de estas

def p_location_1(p):
	'location : ID'
	p[0] = Node('id',[],p[1])
	p[0].name = p[1]
	p[0].value = p[1]

	# Validacion id no declarado.
	data = symtab.find_id( p[1] )
	if not data :
		print ( ">>ERROR: identificador '%s' no declarada." % p[1] )


def p_location_2(p):
	'location : ID CORI expre CORD'
	p[0] = Node('array',[p[3]],p[1])

	# Tipo del id
	typ = symtab.find_type(p[1])
	try:
		p[0].typ = (typ[0], p[3].value)
	except AttributeError:
		p[0].typ= (typ[0], "unknow")
		pass
	p[0].value = p[1]

	# Indices enteros
	if hasattr(p[3],'typ'):
		if p[3].typ[0] != 'int':
			print (">>ERROR:  El indice del array %s debe ser un valor entero" % typ[0])

	# Validacion id no declarado.
	data = symtab.find_id( p[1] )
	if not data :
		print ( ">>ERROR: identificador '%s' no declarada." % p[1] )


#  ---------------------------------------------------------------
#  RELACION
#  ---------------------------------------------------------------

def p_relacion(p):
	"""relacion : expre LT expre
				| expre LE expre
				| expre GT expre
				| expre GE expre
				| expre EQ expre
				| expre NE expre
	"""
	p[0] = Node(p[2], [p[1], p[3]])
	typ = symtab.comparate_types(p[1], p[3])
	p[0].typ = typ
	if typ == 'error' :
		print( ">>ERROR: Se esperaban relaciones del mismo tipo.")

def p_relacion_1(p):
	"""relacion : relacion AND relacion
				| relacion OR relacion
	"""
	p[0] = Node(p[2], [p[1],p[3]])

def p_relacion_not(p):
	'relacion : NOT relacion'
	p[0] = Node('not',[p[2]])

def p_relacion_parent(p):
	'relacion : PARI relacion PARD'
	p[0] = Node('relacion',[p[2]])

#  ---------------------------------------------------------------
#  TYPE
#  ---------------------------------------------------------------

def p_type_f(p):
	'type : FLOAT'
	p[0] = Node('type_float',[], p[1])
	p[0].typ = ("float", None)

def p_type_i(p):
	'type : INT'
	p[0] = Node('type_int',[],p[1])
	p[0].typ = ("int", None)

def p_type_fa(p):
	'type : FLOAT CORI expre CORD'
	p[0] = Node('type_float_Array', [p[3]])
	try:
		p[0].typ= ("float", p[3].value)
	except AttributeError:
		p[0].typ= ("float", "unknow")
		pass


def p_type_ia(p):
	'type : INT CORI expre CORD'
	p[0] = Node('type_int_Array', [p[3]])
	try:
		p[0].typ= ("int", p[3].value)
	except AttributeError:
		p[0].typ= ("int", "unknow")
		pass

#  ---------------------------------------------------------------
#  EXPRLIST
#  ---------------------------------------------------------------

def p_exprelist_coma(p):
	'exprelist : exprelist COMA expre'
	p[1].append(p[3])
	p[0] = p[1]

def p_exprelist_(p):
	'exprelist : expre'
	p[0] = p[1]
# y las funciones sin parametros hay exprelist vacias ????''
	
#  ---------------------------------------------------------------
#  EXPRE
#  ---------------------------------------------------------------

def p_expre(p):
	"""expre : expre MAS expre
			 | expre MENOS expre
			 | expre MUL expre
			 | expre DIV expre
	"""
	p[0]= Node(p[2], [p[1], p[3]])
	typ = symtab.comparate_types(p[1], p[3])
	p[0].typ = typ
	if typ == 'error' :
		print( ">>ERROR: Se esperaban expresiones del mismo tipo.")
 
def p_expre_menosu(p):
	'expre : MENOS expre'
	p[0]= Node('umenos',[p[2]])
	p[0].typ = p[2].typ

def p_expre_masu(p):
	'expre : MAS expre'
	p[0]= Node('umas',[p[2]])
	p[0].typ = p[2].typ

def p_expre_call(p):
	'expre : ID PARI exprelist PARD'
	p[0] = Node( 'call', [p[3]], p[1] )

	typ = symtab.find_type(p[1])
	try:
		p[0].typ = (typ[0], p[3].value)
	except AttributeError:
		p[0].typ= (typ[0], "unknow")
		pass

def p_expre_id(p):
	'expre : ID'
	p[0] = Node('id', [], p[1])
	p[0].value = p[1]
	
	# Validacion id no declarado.
	data = symtab.find_id( p[1] )
	if not data :
		print ( ">>ERROR: identificador '%s' no declarada. Linea" % p[1] )
 
	# tipo de dato
	typ = symtab.find_type(p[1])
	if typ :
		p[0].typ = typ


def p_expre_array(p):
	'expre : ID CORI expre CORD'
	p[0] = Node('array',[p[3]],p[1])

	typ = symtab.find_type(p[1])
	try:
		p[0].typ = (typ[0], p[3].value)
	except AttributeError:
		p[0].typ= (typ[0], "unknow")
		pass

	# indices enteros
	if hasattr(p[3],'typ') & hasattr(p[3],'value'):
		if p[3].typ != 'int':
			print (">>ERROR:  El indice del array %s debe ser un valor entero" % typ[0])
	


def p_expre_fnum(p):
	'expre : FNUM'
	p[0]= Node('numero_f',[], p[1])
	p[0].value = p[1]
	p[0].typ = ("float", None)

def p_expre_inum(p):
	'expre : INUM'
	p[0]= Node('numero',[],p[1])
	p[0].value = p[1]
	p[0].typ = ("int", None)

def p_expre_cast_int(p):
	'expre : INT PARI expre PARD'
	p[0] = Node('cast_int',[p[3]],p[1])
	p[0].value = p[3].value
	p[0].typ = ("int", None)


def p_expre_cast_float(p):
	'expre : FLOAT PARI expre PARD'
	p[0] = Node('cast_float',[p[3]],p[1])
	p[0].value = p[3].value
	p[0].typ = ("float", None)


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
#  PARSER
# -----------------------------------------------------------------------------

#Regla vacio
def p_vacio(p):
	'vacio :'
	pass

# Error rule for syntax errors
def p_error(p):
    print ("Syntax error in input! Near '%s' line: %s" % (p.value,p.lineno))

# Build the parser ------------------------------------------
# Set up a logging object
import logging
logging.basicConfig(
    level = logging.DEBUG,
    filename = "parselog.txt",
    filemode = "w",
    format = "%(filename)10s:%(lineno)4d:%(message)s"
)

log = logging.getLogger()


#parser()



def parse(data):
	parser = yacc.yacc(debug=True,errorlog=log)
	try :
   		res = parser.parse(data)
   		dump_tree( res )
	except EOFError:
   		print( "Archivo no encontrado" )
   	return res
	

