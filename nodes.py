class EqualityMixin(object):

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
            and self.__dict__ == other.__dict__)

    def __ne__(self, other):
        return not self.__eq__(other)


class Node(EqualityMixin):
    """Parse tree Node"""
    def __init__(self, lhs, rhs):
        super(Node, self).__init__()
        self.lhs = lhs
        self.rhs = rhs
        self.parent = None

    def __str__(self):
        return unicode(self).encode('utf-8')

class Quantifier(Node):
    def __init__(self, var_list, form):
        super(Quantifier, self).__init__(form, None)
        self.var_list = var_list


class And(Node):
    def __init__(self, lhs, rhs):
        super(And, self).__init__(lhs, rhs)

    def __unicode__(self):
        if (isinstance(self.lhs, Node) and isinstance(self.rhs, Node) and
            not (isinstance(self.lhs, Quantifier) or isinstance(self.rhs, Quantifier))):
            return u'({0}) \u2227 ({1})'.format(self.lhs, self.rhs)
        else:
            return u'{0} \u2227 {1}'.format(self.lhs, self.rhs)




class Not(Node):
    """Apply not operator"""
    def __init__(self, form):
        super(Not, self).__init__(form, None)

    def __unicode__(self):
        if isinstance(self.lhs, Node) and not isinstance(self.lhs, Quantifier):
            return u'\u00AC( {0} )'.format(self.lhs)
        else:
            return u'\u00AC{0}'.format(self.lhs)


class ForAll(Quantifier):
    def __init__(self, var_list, form):
        super(ForAll, self).__init__(var_list, form)

    def __unicode__(self):
        var_lst = ','.join(map(str, self.var_list))
        return u'\u2200{0}[ {1} ]'.format(var_lst, self.lhs)


class Exists(Quantifier):
    def __init__(self, var_list, form):
        super(Exists, self).__init__(var_list, form)

    def __unicode__(self):
        var_lst = ','.join(map(str, self.var_list))
        return u'\u2203{0}[ {1} ]'.format(var_lst, self.lhs)


class Implication(Node):
    """Material Implication"""
    def __init__(self, lhs, rhs):
        super(Implication, self).__init__(lhs, rhs)

    def __unicode__(self):
        return u'({0}) \u21D2 ({1})'.format(self.lhs, self.rhs)


class Or(Node):
    """Disjunction"""
    def __init__(self, lhs, rhs):
        super(Or, self).__init__(lhs, rhs)

    def __unicode__(self):
        return u'({0}) \u2228 ({1})'.format(self.lhs, self.rhs)


class Equivalence(Node):
    def __init__(self, lhs, rhs):
        super(Equivalence, self).__init__(lhs, rhs)

    def __unicode__(self):
        return u'({0}) \u21D4 ({1})'.format(self.lhs, self.rhs)   


class Predicate(object):
    def __init__(self, name, terms):
        self.name = name
        self.terms = terms

    def __unicode__(self):
        if len(self.terms) > 1:
            term_list = ','.join(map(str, self.terms))
        else:
            term_list = str(self.terms[0])
        return u'{0}( {1} )'.format(self.name, term_list)

    def __str__(self):
        return unicode(self).encode('utf-8')

symbol_table = set()

class Term(object):
    def __init__(self, name):
        self.name = name
        symbol_table.add(name)
    def __str__(self):
        return self.name


class Func(object):
    def __init__(self, name, arg_list):
        self.name = name
        self.arg_list = arg_list
        symbol_table.add(name)

    def __unicode__(self):
        if len(self.arg_list) > 1:
            arg_list = ','.join(map(str, self.arg_list))
        else:
            arg_list = str(self.arg_list[0])
        return u'{0}( {1} )'.format(self.name, arg_list)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def rename_args(self, subst):
        for arg in self.arg_list:
            if isinstance(arg, Func):
                arg.rename_args(subst)
            else:
                arg.name = subst.get(arg.name, arg.name)


