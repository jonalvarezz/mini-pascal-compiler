import symtab
listaf = []


def generate(file,top):
	print >>file, "! Creado por mpascal.py"
	print >>file, "! Daniel Bernal Jona Alvarez, IS744 (2012-2)"
	fun = anexo_get_tipo(top,"funcion")
	print fun
	fun = anexo_get_tipo(top,"type_int")
	print fun
def get_tipo(top,tipo):
    funciones = top.children
    global listaf
    for f in funciones:
    	if f.name == tipo:
    		listaf.append(f.leaf)
    	get_tipo(f,tipo)

def anexo_get_tipo(rea,tipo):
	global listaf
	listaf = []
	get_tipo(rea,tipo)
	return listaf    

