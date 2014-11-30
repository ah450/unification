from enum import Enum

class ET(Enum):
	"""an enum for expression type"""
	var = 1
	atm = 2
	prd = 3

class Expr(object):
	"""represents a FOPL expression"""
	def __init__(self, type, value, params=None):
		self.type = type
		self.value = value
		self.params = params

	def __str__(self):
		if self.type == ET.var:
			return self.value
		elif self.type == ET.atm:
			return str(self.value)
		elif self.type == ET.prd:
			val = ','.join([x.__str__() for x in self.params])
			return self.value + "(" + val+")"

	def __repr__(self):
		return str(self)

	def __eq__(self, other):
		if type(other) == Expr:
			if self.type == self.type:
				if self.params in [None, []]:
					return self.value == other.value
		return False

class Sub(object):
	"""represents a substitution"""
	def __init__(self, name, value):
		self.name = name
		self.value = value
	def __eq__(self,other):
		if type(other) == Sub:
			if self.name == other.name and self.value == other.value:
				return True
			if self.name == other.value and self.value == other.name:
				return True
		return False
	def __str__(self):
		return "{ " +str(self.value) + "/"+str(self.name)+"}"
	def __repr__(self):
		return self.__str__()

def subst(subs, e):
	if len(subs) == 0:
		return e
	for s in subs:
		e = subst1(s, e)
	return e

def subst1(sub, e):
	if type(e) == Expr:
		if e.type == ET.var and e == sub.name:
			e = sub.value
		return e
	#if it is an array apply recursively
	return [subst1(sub,x) for x in e]

def listify(E):
	if type(E) == Expr:
		if E.type == ET.prd:
			new_params = [listify(x) for x in E.params]
			return [Expr(ET.atm,E.value)] + new_params
	return E

def delistify(E):
	if type(E) == list and len(E) > 1:
		rest = [delistify(x) for x in E[1:]]
		return(Expr(ET.prd,E[0].value,rest))
	return E

def exists(x, e):
	if type(e) == Expr :
		return x == e
	return any([exists(x,y) for y in e])
