import ply.yacc as yacc
from .lexer import tokens
from .ast_nodes import Program, Function, ReturnStmt, BinOp, Num, VarDeclare, VarAssign, VarRef, IfStmt, FuncCall

# Precedence rules for operators
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('nonassoc', 'EQUALS_EQUALS', 'NOT_EQUALS', 'LESS_THAN', 'GREATER_THAN'),
)

def p_program(p):
    'program : function'
    p[0] = Program([p[1]])

def p_function(p):
    'function : INT IDENTIFIER LPAREN RPAREN LBRACE statements RBRACE'
    p[0] = Function(p[2], p[6])

def p_statements(p):
    '''statements : statements statement
                  | empty'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = []

def p_statement(p):
    '''statement : declaration
                 | assignment
                 | return_statement
                 | if_statement
                 | func_call_statement'''
    p[0] = p[1]

def p_declaration(p):
    'declaration : INT IDENTIFIER SEMICOLON'
    p[0] = VarDeclare('int', p[2])

def p_assignment(p):
    'assignment : IDENTIFIER EQUALS expression SEMICOLON'
    p[0] = VarAssign(p[1], p[3])

def p_return_statement(p):
    'return_statement : RETURN expression SEMICOLON'
    p[0] = ReturnStmt(p[2])

def p_if_statement(p):
    '''if_statement : IF LPAREN expression RPAREN LBRACE statements RBRACE ELSE LBRACE statements RBRACE
                    | IF LPAREN expression RPAREN LBRACE statements RBRACE'''
    if len(p) == 11: # if-else
        p[0] = IfStmt(condition=p[3], if_body=p[6], else_body=p[10])
    else: # if only
        p[0] = IfStmt(condition=p[3], if_body=p[6], else_body=None)

def p_func_call_statement(p):
    'func_call_statement : IDENTIFIER LPAREN expression RPAREN SEMICOLON'
    p[0] = FuncCall(name=p[1], args=[p[3]])

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression EQUALS_EQUALS expression
                  | expression NOT_EQUALS expression
                  | expression LESS_THAN expression
                  | expression GREATER_THAN expression'''
    p[0] = BinOp(p[1], p[2], p[3])

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_var_ref(p):
    'expression : IDENTIFIER'
    p[0] = VarRef(p[1])

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = Num(p[1])
    
def p_empty(p):
    'empty :'
    pass

def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}'")
    else:
        print("Syntax error at EOF")

parser = yacc.yacc()