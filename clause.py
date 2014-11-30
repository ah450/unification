from parser import Parser
from nodes import (Equivalence, Implication, And, Node, Not, Or, Exists, ForAll,
    Term, Quantifier, symbol_table, Predicate, Func)
import copy
import logging
from colorama import Fore, init



class Enumerator(object):

    def __init__(self):
        self.token = ['a']

    def get_token(self):
        while "".join(self.token) in symbol_table:
            self.increment_token()
        token = "".join(self.token)
        symbol_table.add(token)
        self.increment_token()
        return token

    def increment_token(self):
        if self.token[-1] != 'z':
            self.token[-1] = chr(ord(self.token[-1]) + 1)
        elif len(self.token) == 1:
            self.token = ['a', 'a']
        else:
            # Either all chars are 'z' or one can be     
            if all([x == 'z' for x in self.token]):
                self.token.append('a')
            else:
                # Go back recursively
                self.increment_helper()

    def increment_helper(self):
        if self.token[-1] != 'z':
            self.token[-1] = chr(ord(self.token[-1]) + 1)
            self.token.append('a')
        else:
            self.token = self.token[:-1]
            self.increment_helper()



enumerator = Enumerator()




class Tree(object):
    def __init__(self, root):
        super(Tree, self).__init__()
        self.root = root

def replace_node(node, new_node):
    """Used to update child"""
    new_node.parent = node.parent
    if node.parent.lhs == node:
        node.parent.lhs = new_node
    else:
        node.parent.rhs = new_node

def make_parent_of_children(node):
    """Used to update children's parent backref"""
    if node.lhs is not None:
        node.lhs.parent = node    
    if node.rhs is not None:
        node.rhs.parent = node
        
def equiv_elimination(node, tree):
    if isinstance(node, Equivalence):
        logging.info("Eliminating {0}".format(color_brackets(str(node))))
        lhs = Implication(copy.deepcopy(node.lhs), copy.deepcopy(node.rhs))
        make_parent_of_children(lhs)
        rhs = Implication(node.rhs, node.lhs)
        make_parent_of_children(rhs)
        new_node = And(lhs, rhs)
        make_parent_of_children(new_node)
        logging.info("Replaced with {0}".format(color_brackets(str(new_node))))
        if node.parent is not None:
            replace_node(node, new_node)
        else:
            tree.root = new_node
            new_node.parent = None
        node = new_node
    if isinstance(node, Node):
        if node.lhs is not None:
            equiv_elimination(node.lhs, tree)    
        if node.rhs is not None:
            equiv_elimination(node.rhs, tree)
  


def implic_elimination(node, tree):
    if isinstance(node, Implication):
        # Eliminate
        logging.info("Eliminating {0}".format(color_brackets(str(node))))
        lhs = Not(node.lhs)
        make_parent_of_children(lhs)
        new_node = Or(lhs, node.rhs)
        make_parent_of_children(new_node)
        logging.info("Replaced with {0}".format(color_brackets(str(new_node))))
        if node.parent is not None:
            replace_node(node, new_node)
        else:
            tree.root = new_node
            new_node.parent = None        
        node = new_node
    if isinstance(node, Node):
        if node.lhs is not None:
            implic_elimination(node.lhs, tree)    
        if node.rhs is not None:
            implic_elimination(node.rhs, tree)


def push_negation(node, tree):
    if isinstance(node, Not):
        logging.info("Attempting to push Not {0}".format(color_brackets(str(node))))
        if isinstance(node.lhs, Not):
            logging.info("Simplifying not not")
            # Not not case
            new_node = node.lhs.lhs
            if node.parent is not None:
                replace_node(node, new_node)
            else:
                tree.root = new_node
                new_node.parent = None
            logging.info("Replaced with {0}".format(color_brackets(str(new_node))))
            node = new_node
        elif isinstance(node.lhs, And):
            logging.info("Converting not conjuction to disjunction of negation")
            lhs = Not(node.lhs.lhs)
            make_parent_of_children(lhs)
            rhs = Not(node.lhs.rhs)
            make_parent_of_children(rhs)
            new_node = Or(lhs, rhs)
            make_parent_of_children(new_node)
            if node.parent is not None:
                replace_node(node, new_node)
            else:
                new_node.parent = None
                tree.root = new_node
            logging.info("Replaced with {0}".format(color_brackets(str(new_node))))
            node = new_node
        elif isinstance(node.lhs, Or):
            logging.info("Converting not disjunction to conjuction of negation")
            # convert to conjuction of negation
            lhs = Not(node.lhs.lhs)
            make_parent_of_children(lhs)
            rhs = Not(node.lhs.rhs)
            make_parent_of_children(rhs)
            new_node = And(lhs, rhs)
            make_parent_of_children(new_node)
            if node.parent is not None:
                replace_node(node, new_node)
            else:
                tree.root = new_node
                new_node.parent = None
            logging.info("Replaced with {0}".format(color_brackets(str(new_node))))
            node = new_node
        elif isinstance(node.lhs, Exists):
            logging.info("Converting not there exists to for all not")
            # convert to for all not
            formula = Not(node.lhs.lhs)
            make_parent_of_children(formula)
            new_node = ForAll(node.lhs.var_list, formula)
            make_parent_of_children(new_node)
            if node.parent is not None:
                replace_node(node, new_node)
            else:
                tree.root = new_node
                new_node.parent = None
            logging.info("Replaced with {0}".format(color_brackets(str(new_node))))
            node = new_node
        elif isinstance(node.lhs, ForAll):
            logging.info("Converting not for all to there exists not")
            # Convert to exists not.
            formula = Not(node.lhs.lhs)
            make_parent_of_children(formula)
            new_node = Exists(node.lhs.var_list, formula)
            make_parent_of_children(new_node)
            if node.parent is not None:
                replace_node(node, new_node)
            else:
                tree.root = new_node
                new_node.parent = None
            logging.info("Replaced with {0}".format(color_brackets(str(new_node))))
            node = new_node
        else:
            logging.info("Can not push negation any further")
    if isinstance(node, Node):
        if node.lhs is not None:
            push_negation(node.lhs, tree)    
        if node.rhs is not None:
            push_negation(node.rhs, tree)

def rename_vars(node, subst):
    if isinstance(node, Term):
        node.name = subst.get(node.name, node.name)
    elif isinstance(node, Predicate):
        for term in node.terms:
            if isinstance(term, Func):
                term.rename_args(subst)
            else:
                term.name = subst.get(term.name, term.name)
    elif isinstance(node, Func):
        node.rename_args(subst)
    elif isinstance(node, Quantifier):
        for term in node.var_list:
            if subst.has_key(term.name):
                subst[term.name] = enumerator.get_token()
                logging.info("Will replace {0} with {1}".format(color_brackets(str(term.name)),
                            color_brackets(str(subst[term.name]))))
        node.var_list = [Term(subst.get(term.name, term.name)) for term in node.var_list]
    if isinstance(node, Node):
        if node.lhs is not None:
            rename_vars(node.lhs, subst)    
        if node.rhs is not None:
            rename_vars(node.rhs, subst)    

def standarize_apart(node):
    if isinstance(node, Quantifier):
        subst = {}
        for name in [t.name for t in node.var_list]:
            subst[name] = name
        rename_vars(node.lhs, subst)
    elif isinstance(node, Node):
        if node.lhs is not None:
            standarize_apart(node.lhs)    
        if node.rhs is not None:
            standarize_apart(node.rhs)

def skolemize(node, dependencies, subst, tree):
    if isinstance(node, Quantifier):
        if isinstance(node, Exists):
            for name in [v.name for v in node.var_list]:
                skolem_name = enumerator.get_token()
                subst[name] = skolem_name + "(" + ",".join([str(e) for e in dependencies]) + ")"
            # Remove Quantifier
            if node.parent is not None:
                replace_node(node, node.lhs)
            else:
                tree.root = node.lhs
                node.lhs.parent = None
            skolemize(node.lhs, dependencies, subst, tree)
        elif isinstance(node, ForAll):
            dependencies = dependencies.union({t.name for t in node.var_list})
            skolemize(node.lhs, dependencies, subst, tree)
    elif isinstance(node, Term):
        node.name = subst.get(node.name, node.name)
    elif isinstance(node, Predicate):
        for term in node.terms:
            skolemize(term, dependencies, subst, tree)
    elif isinstance(node, Func):
        node.rename_args(subst)
    elif isinstance(node, Node):
        if node.lhs is not None:
            skolemize(node.lhs, dependencies, subst, tree)
        if node.rhs is not None:
            skolemize(node.rhs, dependencies, subst, tree)


def discard_for_all(node, tree):
    if isinstance(node, ForAll):
        if node.parent is not None:
            replace_node(node, node.lhs)
        else:
            node.lhs.parent = None
            tree.root = node.lhs
        discard_for_all(node.lhs, tree)
    elif isinstance(node, Node):
        if node.lhs is not None:
            discard_for_all(node.lhs, tree)
        if node.rhs is not None:
            discard_for_all(node.rhs, tree)

def distribute(node, tree, transform_and):
    if isinstance(node, Or):
        if isinstance(node.rhs, And):
            and_node = node.rhs
            lhs = Or(node.lhs, and_node.lhs)
            make_parent_of_children(lhs)
            rhs = Or(node.lhs, and_node.rhs)
            make_parent_of_children(rhs)
            new_node = And(lhs, rhs)
            make_parent_of_children(new_node)
            if node.parent is None:
                tree.root = new_node
                new_node.parent = None
            else:
                replace_node(node, new_node)
            node = new_node
        elif isinstance(node.lhs, And) and transform_and:
            and_node = node.lhs
            lhs = Or(node.rhs, and_node.lhs)
            make_parent_of_children(lhs)
            rhs = Or(node.rhs, and_node.rhs)
            make_parent_of_children(rhs)
            new_node = And(lhs, rhs)
            make_parent_of_children(new_node)
            if node.parent is None:
                tree.root = new_node
                new_node.parent = None
            else:
                replace_node(node, new_node)
            node = new_node
    elif isinstance(node, And):
        if isinstance(node.rhs, Or):
            or_node = node.rhs
            lhs = And(node.lhs, or_node.lhs)
            make_parent_of_children(lhs)
            rhs = And(node.lhs, or_node.rhs)
            make_parent_of_children(rhs)
            new_node = Or(lhs, rhs)
            make_parent_of_children(new_node)
            if node.parent is None:
                tree.root = new_node
                new_node.parent = None
            else:
                replace_node(node, new_node)
            node = new_node
        elif isinstance(node.lhs, Or):
            or_node = node.lhs
            lhs = And(node.rhs, or_node.lhs)
            make_parent_of_children(lhs)
            rhs = And(node.rhs, or_node.rhs)
            make_parent_of_children(rhs)
            new_node = Or(lhs, rhs)
            make_parent_of_children(new_node)
            if node.parent is None:
                tree.root = new_node
                new_node.parent = None
            else:
                replace_node(node, new_node)
            node = new_node
    if isinstance(node, Node):
        if node.lhs is not None:
            distribute(node.lhs, tree, transform_and)
        if node.rhs is not None:
            distribute(node.rhs, tree, transform_and)

def clause_form(in_string, trace=False):
    parser = Parser()
    parser.build()
    tree = Tree(parser.parse(in_string))
    print tree.root
    if trace:
        [h_weak_ref().flush() for h_weak_ref in logging._handlerList]
        logging.getLogger().setLevel(logging.INFO)
    else:
        [h_weak_ref().flush() for h_weak_ref in logging._handlerList]
        logging.getLogger().setLevel(logging.ERROR)
    if tree is not None:
        
        logging.info("Eliminating equivalence")
        equiv_elimination(tree.root, tree)
        logging.info("Eliminating implication")
        implic_elimination(tree.root, tree)
        logging.info("Pushing negation")
        push_negation(tree.root, tree)
        logging.info("Standarize Apart")
        standarize_apart(tree.root)
        logging.info("Skolemizing")
        skolemize(tree.root, set(), dict(), tree)
        logging.info("Discarding ForAll quantifiers")
        discard_for_all(tree.root, tree)
        logging.info("Distributing ands and ors")
        distribute(tree.root, tree, transform_and=True)
        distribute(tree.root, tree, transform_and=False)

        return tree.root
    


def color_brackets(text):
    ts  = []
    colors = [Fore.GREEN, Fore.RED, Fore.YELLOW, Fore.MAGENTA]
    color_i = 0
    for c in text.decode('utf-8'):
        if c == '(' or c == '[':
            ts.append(colors[color_i])
            color_i = (color_i + 1) % len(colors)
            ts.append(c)
        elif c == ')' or c == ']':
            color_i = (color_i - 1) % len(colors)
            ts.append(colors[color_i])
            ts.append(c)
        else:
            ts.append(Fore.WHITE)
            ts.append(c)
    return u"".join(ts).encode('utf-8')

if __name__ == '__main__':
    # ∃x[P (x) ∧ ∀x[Q(x) ⇒ ¬P (x)]]
    init(autoreset=True)
    test_1 = u'∃x[P (x) ∧ ∀x[Q(x) ⇒ ¬P (x)]]'
    print 'Running test case one'
    print color_brackets(str(clause_form(test_1, False)))
    test_2 =  u'∀x[P (x) ⇔ (Q(x) ∧ ∃y[Q(y) ∧ R(y, x))]]'
    print 'Running test case two'
    print color_brackets(str(clause_form(test_2, False)))
