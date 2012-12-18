import symtab
listaf = []
pilavalores = []


def generate(file,top):
	print >>file, "! Creado por mpascal.py"
	print >>file, "! Daniel Bernal Jona Alvarez, IS744 (2012-2)"
	
	emit_program(file,top)
	anexo_get_expr(top)

def get_tipo(top,tipo):
    funciones = top.children
    global listaf
    for f in funciones:
    	if f.name == tipo:
    		listaf.append(f)
    	get_tipo(f,tipo)

def anexo_get_tipo(rea,tipo):
	global listaf
	listaf = []
	get_tipo(rea,tipo)
	return listaf 

def anexo_get_expr(top):
	global listaf
	expr = "numero id + - * / < > <= >= = != and or".split()
	listaf = []
	for i in expr :
		get_tipo(top, i)
	return listaf

def eval_expressions(out, lista):
	for s in lista :
		eval_expression(out, s)

def eval_expression(out, expr):
	if expr.name == 'numero':
		print >>out, "! push", expr.value
	elif expr.name == 'id':
		print >>out, "! push", expr.value
	elif expr.name == '+':
		left = expr.children[0]
		right = expr.children[1]
		eval_expression(out,left)
		eval_expression(out,right)
		print >>out, "! add"
	elif expr.name == '-':
		left = expr.children[0]
		right = expr.children[1]
		eval_expression(out,left)
		eval_expression(out,right)
		print >>out, "! sub"
	elif expr.name == '*':
		left = expr.children[0]
		right = expr.children[1]
		eval_expression(out,left)
		eval_expression(out,right)
		print >>out, "! multiplicacion"
	elif expr.name == '/':
		left = expr.children[0]
		right = expr.children[1]
		eval_expression(out,left)
		eval_expression(out,right)
		print >>out, "! division"
	elif expr.name == '<':
		left = expr.children[0]
		right = expr.children[1]
		eval_expression(out,left)
		eval_expression(out,right)
		print >>out, "! mayor"
	elif expr.name == '>':
		left = expr.children[0]
		right = expr.children[1]
		eval_expression(out,left)
		eval_expression(out,right)
		print >>out, "! menor"
	elif expr.name == '<=':
		left = expr.children[0]
		right = expr.children[1]
		eval_expression(out,left)
		eval_expression(out,right)
		print >>out, "! mayor_igual"
	elif expr.name == '>=':
		left = expr.children[0]
		right = expr.children[1]
		eval_expression(out,left)
		eval_expression(out,right)
		print >>out, "! menor_igual"
	elif expr.name == '=':
		left = expr.children[0]
		right = expr.children[1]
		eval_expression(out,left)
		eval_expression(out,right)
		print >>out, "! igual"
	elif expr.name == '!=':
		left = expr.children[0]
		right = expr.children[1]
		eval_expression(out,left)
		eval_expression(out,right)
		print >>out, "! no_igual"
	elif expr.name == 'or':
		left = expr.children[0]
		right = expr.children[1]
		eval_expression(out,left)
		eval_expression(out,right)
		print >>out, "! or"
	elif expr.name == 'and':
		left = expr.children[0]
		right = expr.children[1]
		eval_expression(out,left)
		eval_expression(out,right)
		print >>out, "! and"

#-------------------  EMITS  ----------------------------

def emit_program(out,top):
	print >>out,"\n! program"
	funclist = anexo_get_tipo(top,"funcion")
	for f in funclist:
		emit_function(out,f)

def emit_function(out,func):
	print >>out,"\n! function: %s (start) " % func.leaf
	emit_statementsinter(out,func)
	print >>out,"! function: %s (end) " % func.leaf

def emit_statementsinter(out,statements):
	statements = anexo_get_tipo(statements,"lineas")
	if len(statements)>0:
		statements = statements[0].children
		emit_statements(out,statements)

def emit_statements(out,statements):
	for s in statements:
		emit_statement(out,s)

def emit_statement(out,s):
	if s.name == 'print':
		emit_print(out,s)
	elif s.name == 'read':
		emit_read(out,s)
	elif s.name == 'write':
		emit_write(out,s)
	elif s.name == 'while':
		emit_while(out,s)
	elif s.name == 'skip':
		emit_skip(out,s)
	elif s.name == 'break':
		emit_break(out,s)
	elif s.name == 'if':
		emit_if(out,s)
	elif s.name == 'return':
		emit_return(out,s)
	elif s.name == ':=':
		emit_asig(out,s)
	elif s.name == 'else':
		emit_else(out,s)	
	else : pass

def emit_print(out,s):
	print >>out, "\n! print (start)"
	print >>out, "! print (end)"

def emit_read(out,s):
	print >>out, "\n! read (start)"
	print >>out, "! read (end)"

def emit_write(out,s):
	print >>out, "\n! write (start)"
	expr = anexo_get_expr(s)
	eval_expressions(out,expr)
	print >>out, "! expr := pop"
	print >>out, "! write(expr)"
	print >>out, "! write (end)"

def emit_while(out,s):
	print >>out, "\n! while (start)"
	expr = anexo_get_expr(s)
	eval_expressions(out,expr)
	emit_statementsinter(out,s)
	print >>out, "! while (end)"

def emit_skip(out,s):
	print >>out, "\n! skip (start)"
	print >>out, "! skip (end)"

def emit_break(out,s):
	print >>out, "\n! break (start)"
	print >>out, "! break (end)"

def emit_if(out,s):
	print >>out, "\n! if (start)"
	expr = anexo_get_expr(s)
	eval_expressions(out,expr)
	emit_statements(out,s.children)
	print >>out, "! if (end)"

def emit_return(out,s):
	print >>out, "\n! return (start)"
	expr = anexo_get_expr(s)
	eval_expressions(out,expr)
	print >>out, "! return (end)"

def emit_asig(out,s):
	print >>out, "\n! asig (start)"
	expr = anexo_get_expr(s)
	eval_expressions(out,expr)
	print >>out, "! expr := pop"
	print >>out, "! asig (end)"

def emit_else(out,s):
	print >>out, "\n! else (start)"
	if len(s.children)>0:
		expr = anexo_get_expr(s)
		eval_expressions(out,expr)
		emit_statements(out,s.children)
	print >>out, "! else (end)"