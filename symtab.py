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
    #    print "\n* %s *\n" % dir(_scopes)
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
    s = Symbol(name)
    s.name = name
    s.scope = current
    s.level = len(_scopes) - 1
    current[name] = s
    print (s.name)
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

    
#......................................funciones Propias..............................


# Busca identificador en la tabla actual de simbolos
#def findl(name):
#    for n in range(len(scopes)-1,-1,-1):
#        for s in scopes[n]:
#            if s.name==name and (hasattr(s,'typ') or hasattr(s,'clase')):
#                return None
#    return last[-1]



# Busca identificador en las tabla de simbolos
def find(name):
    for n in range(len(_scopes)-1,-1,-1):
        for s in _scopes[n]:
            if s.name==name and (hasattr(s,'typ') or hasattr(s,'clase')):
                return s
    return None
#..........................................................................
# Para ponerle el atributo 'class'=ident y 'typ' a cada identificador que no sea una funcion
def banf(name,typ=None):
    for s in current:
        if s.name == name:
            if not (hasattr(s,'clase') or hasattr(s,'typ')):
                s.clase = 'ident'
                s.typ=typ
                return None
            else:
                #print "#REDECLARADO# %s" % s.name
                return s

# Para ponerle el atributo 'class'=ident y 'typ' a cada identificador que no sea una funcion
def banf2(name,typ=None):
    for s in current:
        if s.name == name:
            if not (hasattr(s,'clase') or hasattr(s,'typ')):
                s.clase = 'ident'
                s.typ=typ
            if hasattr(s,'typ'):
                if s.typ != typ:
                    return None
            return s



#-----------------------------------inecesarios con banf------------------

# Busca identificador de un simbolo en todas las tablas de simbolos
def get_type(name, level = 0, attr = None ):
    for i in range( len(_scopes) - (level+1), -1, -1 ):
        s = _scopes[i]
        try:
            sym = s[name]
            if attr:
                if hasattr(sym,attr):
                    ty = s[type]
                    return ty
            else:
                return ty
        except KeyError:
            pass
    return None

# buscar linea 
def get_linea(name, level = 0, attr = None ):
    for i in range( len(_scopes) - (level+1), -1, -1 ):
        s = _scopes[i]
        try:
            sym = s[name]
            if attr:
                if hasattr(sym,attr):
                    ly = s[lineno]
                    return ly
            else:
                return ly
        except KeyError:
            pass
    return None 

