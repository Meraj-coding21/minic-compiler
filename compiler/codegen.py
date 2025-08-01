from llvmlite import ir, binding
from .ast_nodes import Program, Function, ReturnStmt, BinOp, Num, VarDeclare, VarAssign, VarRef, IfStmt, FuncCall

class CodeGen:
    def __init__(self):
        self.binding = binding
        self.binding.initialize()
        self.binding.initialize_native_target()
        self.binding.initialize_native_asmprinter()
        self.module = ir.Module(name=__file__)
        self.builder = None
        self.symbol_table = {}

        # Declare external functions like print_int
        self._declare_print_function()

    def _declare_print_function(self):
        # Declare C function: void print_int(int)
        int_type = ir.IntType(32)
        func_type = ir.FunctionType(ir.VoidType(), [int_type], var_arg=False)
        self.print_int = ir.Function(self.module, func_type, name="print_int")

    def generate_code(self, node):
        return self._visit(node)

    def _visit(self, node):
        method_name = f'_visit_{node.__class__.__name__}'
        visitor = getattr(self, method_name, self._generic_visit)
        return visitor(node)

    def _generic_visit(self, node):
        raise Exception(f'No _visit_{node.__class__.__name__} method')

    def _visit_Program(self, node: Program):
        for func in node.functions:
            self._visit(func)
        return str(self.module)

    def _visit_Function(self, node: Function):
        func_name = node.name
        func_type = ir.FunctionType(ir.IntType(32), [])
        func = ir.Function(self.module, func_type, name=func_name)
        
        block = func.append_basic_block(name="entry")
        self.builder = ir.IRBuilder(block)
        
        self.symbol_table = {} # Clear symbol table for new function scope

        for stmt in node.body:
            self._visit(stmt)

    def _visit_VarDeclare(self, node: VarDeclare):
        var_address = self.builder.alloca(ir.IntType(32), name=node.var_name)
        self.symbol_table[node.var_name] = var_address

    def _visit_VarAssign(self, node: VarAssign):
        value = self._visit(node.expr)
        var_address = self.symbol_table[node.var_name]
        self.builder.store(value, var_address)

    def _visit_ReturnStmt(self, node: ReturnStmt):
        value = self._visit(node.expr)
        self.builder.ret(value)
        
    def _visit_IfStmt(self, node: IfStmt):
        condition_val = self._visit(node.condition)

        then_block = self.builder.function.append_basic_block('then')
        merge_block = self.builder.function.append_basic_block('merge')
        
        if node.else_body:
            else_block = self.builder.function.append_basic_block('else')
            self.builder.cbranch(condition_val, then_block, else_block)
        else:
            self.builder.cbranch(condition_val, then_block, merge_block)

        # Then Block
        self.builder.position_at_end(then_block)
        for stmt in node.if_body:
            self._visit(stmt)
        if not self.builder.block.is_terminated:
            self.builder.branch(merge_block)

        # Else Block
        if node.else_body:
            self.builder.position_at_end(else_block)
            for stmt in node.else_body:
                self._visit(stmt)
            if not self.builder.block.is_terminated:
                self.builder.branch(merge_block)

        # Merge Block
        self.builder.position_at_end(merge_block)

    def _visit_FuncCall(self, node: FuncCall):
        if node.name == "print_int":
            arg_value = self._visit(node.args[0])
            self.builder.call(self.print_int, [arg_value])
        else:
            raise Exception(f"Undefined function call: {node.name}")

    def _visit_BinOp(self, node: BinOp):
        lhs = self._visit(node.left)
        rhs = self._visit(node.right)
        op = node.op

        if op == '+':
            return self.builder.add(lhs, rhs, 'addtmp')
        elif op == '-':
            return self.builder.sub(lhs, rhs, 'subtmp')
        elif op == '*':
            return self.builder.mul(lhs, rhs, 'multmp')
        elif op == '/':
            return self.builder.sdiv(lhs, rhs, 'divtmp')
        elif op in ['==', '!=', '<', '>']:
            return self.builder.icmp_signed(op, lhs, rhs, 'cmptmp')
        else:
            raise Exception(f'Unknown binary operator: {op}')

    def _visit_Num(self, node: Num):
        return ir.Constant(ir.IntType(32), node.value)

    def _visit_VarRef(self, node: VarRef):
        var_address = self.symbol_table[node.var_name]
        return self.builder.load(var_address, name=node.var_name)