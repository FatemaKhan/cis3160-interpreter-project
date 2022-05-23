# all Token types
(LITERAL, PLUS, MINUS, MUL, LPAREN, RPAREN, ID, ASSIGN, SEMI, EOF) = (
    'LITERAL', 'PLUS', 'MINUS', 'MUL', '(', ')', 'ID', 'ASSIGN', 'SEMI', 'EOF'
)

from Lexer import Lexer
from Parser import Parser
from NodeVisitor import NodeVisitor

class Interpreter(NodeVisitor):

    GLOBAL_SCOPE = {}

    def __init__(self, parser):
        self.parser = parser

    def visit_BinOp(self, node):
        """
        visit a BinOp node of the AST
        """
        if node.op.type == PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == MUL:
            return self.visit(node.left) * self.visit(node.right)

    def visit_Num(self, node):
        """
        visit a Num node of the AST
        """
        return node.value

    def visit_UnaryOp(self, node):
        """
        visit a UnaryOp node of the AST
        """
        op = node.op.type
        if op == PLUS:
            return +self.visit(node.expr)
        elif op == MINUS:
            return -self.visit(node.expr)

    def visit_CodeBlock(self, node):
        """
        visit the full CodeBlock node of the AST
        """
        for child in node.children:
            self.visit(child)

    def visit_Assign(self, node):
        """
        visit an Assign node of the AST
        """
        var_name = node.left.value
        self.GLOBAL_SCOPE[var_name] = self.visit(node.right)

    def visit_Var(self, node):
        """
        visit a Var node of the AST
        """
        var_name = node.value
        val = self.GLOBAL_SCOPE.get(var_name)
        if val is None:
            raise NameError(f"{repr(var_name)} variable is not defined")
        else:
            return val

    def visit_NoOp(self, node):
        pass

    def interpret(self):
        tree = self.parser.parse()
        if tree is None:
            return ''
        return self.visit(tree)

def print_Global_Scope():
    """
    print the global scope of the interpreter
    """
    for k, v in Interpreter.GLOBAL_SCOPE.items():
        print(k, v)

def main():
    # import sys
    # text = open(sys.argv[1], 'r').read()
    text = open('input.txt').read()

    lexer = Lexer(text)
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    result = interpreter.interpret()
    # print(interpreter.GLOBAL_SCOPE)
    print_Global_Scope()


if __name__ == '__main__':
    main()