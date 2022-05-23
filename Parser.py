# all Token types
(LITERAL, PLUS, MINUS, MUL, LPAREN, RPAREN, ID, ASSIGN, SEMI, EOF) = (
    'LITERAL', 'PLUS', 'MINUS', 'MUL', '(', ')', 'ID', 'ASSIGN', 'SEMI', 'EOF'
)

class AST(object):
    pass

class BinOp(AST):
    """
    Represents a binary operator
    """
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right


class Num(AST):
    """
    Represents a number
    """
    def __init__(self, token):
        self.token = token
        self.value = token.value


class UnaryOp(AST):
    """
    Represents a unary operator
    """
    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr


class CodeBlock(AST):
    """
    Represents the program block
    """
    def __init__(self):
        self.children = []


class Assign(AST):
    """
    Represents an assignment statement
    """
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right


class Var(AST):
    """The Var node is constructed out of ID token."""
    def __init__(self, token):
        self.token = token
        self.value = token.value


class NoOp(AST):
    pass


class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        # set current token to the first token taken from the input
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def program(self):
        """
        program : Assignment*
        """
        node = self.assignment_statement()

        nodes = [node]

        while self.current_token.type == SEMI:
            self.eat(SEMI)
            nodes.append(self.assignment_statement())

        if self.current_token.type == ID:
            self.error()

        root = CodeBlock()
        for node in nodes:
            root.children.append(node)

        return root


    def assignment_statement(self):
        """
        asignment : Identifier = Exp;
        """
        if self.current_token.type == ID:
            left = self.identifier()
            token = self.current_token
            self.eat(ASSIGN)
            right = self.expr()
            node = Assign(left, token, right)
        else:
            # empty production
            node = NoOp()
        return node

    def identifier(self):
        """
        Identifier: Letter [Letter | Digit]*
        (handled in lexer)
        """
        node = Var(self.current_token)
        self.eat(ID)
        return node

    # def empty(self):
    #     """An empty production"""
    #     return NoOp()

    def expr(self):
        """
        expr : term ((PLUS | MINUS) term)*
        (after removing left recursion)
        """
        node = self.term()

        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
            elif token.type == MINUS:
                self.eat(MINUS)

            node = BinOp(left=node, op=token, right=self.term())

        return node

    def term(self):
        """
        term : factor (MUL factor)*
        (after removing left recursion)
        """
        node = self.factor()

        while self.current_token.type == MUL:
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)

            node = BinOp(left=node, op=token, right=self.factor())

        return node

    def factor(self):
        """
        factor : LPAREN expr RPAREN 
                  | PLUS factor
                  | MINUS factor
                  | LITERAL
                  | Identifier
        """
        token = self.current_token
        if token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node
        elif token.type == PLUS:
            self.eat(PLUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == MINUS:
            self.eat(MINUS)
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == LITERAL:
            self.eat(LITERAL)
            return Num(token)
        else:
            node = self.identifier()
            return node

    def parse(self):
        """
        program : Assignment*

        asignment : Identifier = Exp;

        expr : term ((PLUS | MINUS) term)*
        (after removing left recursion)

        term : factor (MUL factor)*
        (after removing left recursion)

        factor : LPAREN expr RPAREN 
              | PLUS factor
              | MINUS factor
              | LITERAL
              | Identifier
        
        Identifier: Letter [Letter | Digit]*

        """
        node = self.program()
        if self.current_token.type != EOF:
            self.error()

        return node
