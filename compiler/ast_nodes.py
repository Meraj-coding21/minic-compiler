class Node:
    def __repr__(self):
        # A simple way to represent nodes for debugging
        return f"<{self.__class__.__name__}>"

class Program(Node):
    def __init__(self, functions):
        self.functions = functions

class Function(Node):
    def __init__(self, name, body):
        self.name = name
        self.body = body

class ReturnStmt(Node):
    def __init__(self, expr):
        self.expr = expr

class BinOp(Node):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Num(Node):
    def __init__(self, value):
        self.value = value

class VarDeclare(Node):
    def __init__(self, var_type, var_name):
        self.var_type = var_type
        self.var_name = var_name

class VarAssign(Node):
    def __init__(self, var_name, expr):
        self.var_name = var_name
        self.expr = expr

class VarRef(Node):
    def __init__(self, var_name):
        self.var_name = var_name

class IfStmt(Node):
    def __init__(self, condition, if_body, else_body):
        self.condition = condition
        self.if_body = if_body
        self.else_body = else_body

class FuncCall(Node):
    def __init__(self, name, args):
        self.name = name
        self.args = args