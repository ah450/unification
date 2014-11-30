from ply import yacc
from lexer import Lexer
from nodes import Not, ForAll, Exists, Predicate, Func, And, Or, Term, Implication, Equivalence

class Parser(object):
    """FOPL formula parser"""

    def __init__(self):
        self.tokens = Lexer.tokens

    def p_start_1(self, p):
        'start : atom'
        p[0] = p[1]

    def p_start_2(self, p):
        'start : start BINARY_OP start'
        token = p[2]
        if token == ur'\u21D2': # Material Implication
            p[0] = Implication(p[1], p[3])
        elif token == ur'\u21D4': # Material Equivalence
            p[0] = Equivalence(p[1], p[3])
        elif token == ur'\u2227': # Conjuction
            p[0] = And(p[1], p[3])
        else: # token == ur'\u2228' Disjunction
            p[0] = Or(p[1], p[3])
        p[0].lhs.parent = p[0].rhs.parent = p[0]

    def p_start_3(self, p):
        'start : start BINARY_OP LB start RB'
        token = p[2]
        if token == ur'\u21D2': # Material Implication
            p[0] = Implication(p[1], p[4])
        elif token == ur'\u21D4': # Material Equivalence
            p[0] = Equivalence(p[1], p[4])
        elif token == ur'\u2227': # Conjuction
            p[0] = And(p[1], p[4])
        else: # token == ur'\u2228' Disjunction
            p[0] = Or(p[1], p[4])
        p[0].lhs.parent = p[0].rhs.parent = p[0]

    def p_start_4(self, p):
        'start : UNARY_OP start'
        p[0] = Not(p[2])
        p[0].lhs.parent = p[0]

    def p_start_5(self, p):
        'start : quantifier LB start RB'
        p[1].lhs = p[3]
        p[1].lhs.parent = p[1]
        p[0] = p[1]

    def p_term_1(self, p):
        'term : VAR_OR_FUNC LB term_list RB'
        p[0] = Func(p[1], p[3])
        p[0].lhs.parent = p[0].rhs.parent = p[0]

    def p_term_2(self, p):
        'term : VAR_OR_FUNC'
        p[0] = Term(p[1])

    def p_term_list_1(self, p):
        'term_list : term_list term'
        p[0] = p[1] + [p[2]]

    def p_term_list_2(self, p):
        'term_list : term'
        p[0] = [p[1]]

    def p_predicate(self, p):
        'predicate : PREDICATE LB term_list RB'
        p[0] = Predicate(p[1], p[3]) # Name and terms

    def p_atom_1(self, p):
        'atom : predicate'
        p[0] = p[1]

    # def p_atom_2(self, p):
    #     'atom : quantifier LB atom RB'
    #     p[1].lhs = p[3]
    #     p[0] = p[1]

    def p_quantifier_1(self, p):
        'quantifier : FOR_ALL var_list'
        p[0] = ForAll(p[2], None)

    def p_quantifier_2(self, p):
        'quantifier : EXISTS var_list'
        p[0] = Exists(p[2], None)

    def p_var_list_1(self, p):
        'var_list : var_list VAR_OR_FUNC'
        p[0] = p[1] + [p[2]]

    def p_var_list_2(self, p):
        'var_list : VAR_OR_FUNC'
        p[0] = [Term(p[1])]

    def build(self, **kwargs):
        self.lex = Lexer()
        self.lex.build()
        self.yacc = yacc.yacc(module=self, **kwargs)

    def parse(self, string):
        return self.yacc.parse(string, debug=0, lexer=self.lex)