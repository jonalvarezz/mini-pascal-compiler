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
		datatype = node.typ
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
#  ---------------------------------------------------------------

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
	#symtab.pop_scope()

def p_fundecl(p):
	'fundecl : FUN'
	# Crea una nueva tabla de simbolos
	#symtab.new_scope()

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
#	p[0].name = p[1]
#	p[0].value = p[1]
#	p[0].typ=p[3].typ

#	a=symtab.banf(p[0].name,p[3].typ)
#	if a :
#		print "#Error# redeclaracion de identificador '%s' en linea %i" % (p[0].name,a.lineno)

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
#	a=symtab.findl(p[1].name)
#	if hasattr(p[1], "typ"):
#		typ=p[1].typ
#	else:
#		typ=None

#	s=symtab.banf2(p[1].name,typ)
#	if not s:
#		pass
		###print "#Error# Assign '%s' error de tipos" % (p[1].name)

#	if a:
#		print "#Error# variable no declarada '%s' en la linea %i " % (p[1].name,a.lineno)


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

def p_location_1(p):
	'location : ID'
	p[0] = Node('id',[],p[1])
#	p[0] = Node('',[],p[1])
#	p[0].name = p[1]
#	p[0].value = p[1]

def p_location_2(p):
	'location : ID CORI expre CORD'
	p[0] = Node('id[]',[p[3]],p[1])
#	p[0].name = p[1]
#	p[0].value = p[1]

#	if hasattr(p[3],'typ'):
#		if p[3].typ != 'int':
#			print "#Error# El indice de un vector debe ser entero '%s'" % f.name
#		else:
#			p[0].typ = p[3].typ
#  ---------------------------------------------------------------
#  RELACION
#  ---------------------------------------------------------------

def p_relacion_lt(p):
	'relacion : expre LT expre'
	p[0] = Node('<',[p[1],p[3]])

def p_relacion_le(p):
	'relacion : expre LE expre'
	p[0] = Node('<=',[p[1],p[3]])

def p_relacion_gt(p):
	'relacion : expre GT expre'
	p[0] = Node('>',[p[1],p[3]])

def p_relacion_ge(p):
	'relacion : expre GE expre'
	p[0] = Node('>=',[p[1],p[3]])

def p_relacion_eq(p):
	'relacion : expre EQ expre'
	p[0] = Node('=',[p[1],p[3]])

def p_relacion_ne(p):
	'relacion : expre NE expre'
	p[0] = Node('!=',[p[1],p[3]])	 

def p_relacion_and(p):
	'relacion : relacion AND relacion'
	p[0] = Node('and',[p[1],p[3]])

def p_relacion_or(p):
	'relacion : relacion OR relacion'
	p[0] = Node('or',[p[1],p[3]])

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
	p[0].typ = "float_type"

def p_type_i(p):
	'type : INT'
	p[0] = Node('type_int',[],p[1])
	p[0].typ = "int_type"

def p_type_fa(p):
	'type : FLOAT CORI expre CORD'
	p[0] = Node('type_float_Array', [p[3]])
#   p[0].typ='float['+str(p[3].value)+']_type'

def p_type_ia(p):
	'type : INT CORI expre CORD'
	p[0] = Node('type_int_Array', [p[3]])
#	p[0].typ='int['+str(p[3].value)+']_type'

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

def p_expre_mas(p):
	'expre : expre MAS expre'
	p[0]= Node('+',[p[1],p[3]])

def p_expre_menos(p):
	'expre : expre MENOS expre'
	p[0]= Node('-',[p[1],p[3]])
 
def p_expre_mul(p):
	'expre : expre MUL expre'
	p[0]= Node('*',[p[1],p[3]])

def p_expre_div(p):
	'expre : expre DIV expre'
	p[0]= Node('/',[p[1],p[3]])
 
def p_expre_menosu(p):
	'expre : MENOS expre'
	p[0]= Node('umenos',[p[2]])
#	requiere asignacion de tipo pero todavia no se como implementarla

def p_expre_masu(p):
	'expre : MAS expre'
	p[0]= Node('umas',[p[2]])
#	requiere asignacion de tipo pero todavia no se como implementarla

def p_expre_call(p):
	'expre : ID PARI exprelist PARD'
	p[0] = Node( 'call', [p[3]], p[1] )

#	f=symtab.find(p[1])

#	args = len(p[3].children)
#	if 	p[3].leaf:
#		args += 1

#	if not f:
#		print "Error Funcion no declarada '%s' " % (p[1]),
#		lf = get_linea(p[1])
#		print "en la linea '%s'" % lf
#	else:
#		if args != len(f.numpar):
#			print "#Error# Numero de argumentos erroneo en '%s'" % f.name
#		else:
#			if 	p[3].leaf:
				#print "adadsdsad: ", p[3].typ , ":::" , f.name,f.numpar
#				if p[3].typ != f.numpar[0]:
#					print "#Error# Tipos de argumentos erroneo en'%s'" % f.name
#				else:
#					for i in range(0,len(p[3].children)):
#						if hasattr(p[3].children[i],'typ'):
#							if p[3].children[i].typ != f.numpar[i+1]:
#								print "#Error# Tipos de argumentos erroneo en'%s'" % f.name
#								break
#	if hasattr(p[3],'typ'):
#		p[0] = Node('',[p[3]],p[1])
#		p[0].name = p[1]
#		p[0].value = p[1]
#		p[0].call = 1
#		p[0].typ = p[3].typ
#	else:
#		p[0] = Node('',[p[3]],p[1])
#		p[0].call = 1
#		p[0].name = p[1]
#		p[0].value = p[1]

def p_expre_id(p):
	'expre : ID'
	p[0] = Node('id', [], p[1])
	p[0].value = p[1]
	f = symtab.get_symbol(p[1])
#	if f:
		#print "\n* %s *\n" % dir(f)
#		p[0].typ = f

def p_expre_array(p):
	'expre : ID CORI expre CORD'
	p[0] = Node('array',[p[3]],p[1])
	#indices enteros
	if hasattr(p[3],'typ'):
	    if hasattr(p[3],'value'):
			
			if p[3].typ != 'int':
				print ("#Error# El indice del array debe ser un valor entero '%s'" % f.name)
			else:
				p[0].typ = "int["+str(p[3].value)+"]_type"
	    else:
		print ("#Error# no se le encuentra valor")
	


def p_expre_fnum(p):
	'expre : FNUM'
	p[0]= Node('numero_f',[], p[1])
	p[0].value = p[1]
	p[0].typ = "float_type"

def p_expre_inum(p):
	'expre : INUM'
	p[0]= Node('numero',[],p[1])
	p[0].value = p[1]
	p[0].typ = "int_type"

def p_expre_cast_int(p):
	'expre : INT PARI expre PARD'
	p[0] = Node('cast_int',[p[3]],p[1])
	p[0].value = p[p[3].value]
	p[0].typ = "int_type"


def p_expre_cast_float(p):
	'expre : FLOAT PARI expre PARD'
	p[0] = Node('cast_float',[p[3]],p[1])
	p[0].value = p[p[3].value]
	p[0].typ = "float_type"


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
    print ("Syntax error in input!")

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

parser = yacc.yacc(debug=True,errorlog=log)

try :
   f = open(sys.argv[1])
   res = parser.parse(f.read())
   f.close()
   dump_tree( res )
except EOFError:
   print( "Archivo no encontrado" )