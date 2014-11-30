from ply import lex
import re

class Lexer(object):
    """ Lexer for FOPL formulas """
    tokens = [
        'VAR_OR_FUNC', 'PREDICATE', 'BINARY_OP',
        'UNARY_OP', 'LB', 'RB', 'FOR_ALL', 'EXISTS'
    ]

    def t_EXISTS(self, t):
        ur'\u2203'
        return t

    def t_FOR_ALL(self, t):
        ur'\u2200'
        return t

    def t_UNARY_OP(self, t):
        ur'\u00AC'
        return t

    def t_BINARY_OP(self, t):
        ur'\u21D4|\u21D2|\u2227|\u2228'
        return t

    def t_LB(self, t):
        r'\(|\['
        return t

    def t_RB(self, t):
        r'\)|\]'
        return t

    def t_PREDICATE(self, t):
        r'[A-Z][a-zA-Z]*'
        return t

    def t_VAR_OR_FUNC(self, t):
        r'[a-z][A-Za-z]*'
        return t
       
    def build(self):
        """Builds the parser, must be called before use"""
        self.lexer = lex.lex(module=self, reflags=re.UNICODE)

    def input(self, data):
        """Sets parser input"""
        self.lexer.input(data)

    def token(self):
        """Gets next token or None"""
        return self.lexer.token()

    def t_whitespace(self, t):
        r'\s+'
        pass

    def t_comma(self, t):
        r','
        pass

    def t_error(self, t):
        pass
