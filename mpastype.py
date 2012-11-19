

class ExprType(object):

	def __init__(self, name, bin_ops = set(), un_ops = set()):

		self.name = name
		self.bin_ops = bin_ops
		self.un_ops = un_ops



int_type = ExprType("int",
	set(('MAS', 'MENOS', 'MUL', 'DIV',
		 'LE', 'LT', 'EQ', 'NE', 'GT', 'GE')),
	set(('MAS', 'MENOS')),
	)
float_type = ExprType("float",
	set(('MAS', 'MENOS', 'MUL', 'DIV',
		 'LE', 'LT', 'EQ', 'NE', 'GT', 'GE')),
	set(('MAS', 'MENOS')),
	)
string_type = ExprType("string",
	set(('MAS',)),
	set(),
	)
boolean_type = ExprType("bool",
	set(( 'EQ', 'NE')),
	set(),
	)

