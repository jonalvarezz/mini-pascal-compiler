_scopes = []
current = None

class Symbol:
    def __init__(self,name):
        self.name=name
        self.numpar=[]

    def __repr__(self):
        a= self.name
        return a

    def __str__(self):
        return self.name

    def append(self,num):
        self.numpar.append(num)

# Crea un nueva tabla
def new_scope():
	global current
	current = {}
	_scopes.append(current)
	return current

# Elimina la tabla actual y restaura la anterior.
def pop_scope():
	global current
	r = _scopes.pop()
	current = _scopes[-1]
	return r

# Busca un simbolo en la tabla actual
def is_symbol( name ) :
    if current.get( name, False ):
        return True
    return False

# Busca un simbolo en todas las tablas de simbolos
def get_symbol(name, level = 0, attr = None ):
    for i in range( len(_scopes) - (level+1), -1, -1 ):
        s = _scopes[i]
        try:
            sym = s[name]
            if attr:
                if hasattr(sym,attr):
                    return sym
            else:
                return sym
        except KeyError:
            pass
    return None

# Agrega un nuevo simbolo
def add_symbol(name):
    s = Symbol()
    s.name = name
    s.scope = current
    s.level = len(_scopes) - 1
    current[name] = s
    return s

# Instala un simbol en el ambito actual
def set_symbol(s):
    current[s.name] = s

# adjunta una entrada de tabla de simbol al token t
def attach_symbol(t):
    s = current.get(t.value)
    if not s:
        s = add_symbol(t.value)
        s.lineno = t.lineno
    t.symtab = s