"""
V++ Programming Language - Tree-walking AST Interpreter
"""

import os
from typing import Any, List, Optional
from .tokens import Token, TokenType
from .ast_nodes import (
    ASTNode, Program, Block, VarDecl, IfStmt, WhileStmt, ForInStmt,
    BreakStmt, ContinueStmt, ReturnStmt, FunctionDecl, ClassDecl,
    TryCatchStmt, ThrowStmt, ImportStmt, ExprStmt,
    NumberLiteral, StringLiteral, BooleanLiteral, NullLiteral,
    Identifier, SelfExpr, ListLiteral, DictLiteral,
    UnaryOp, BinaryOp, Assign, CallExpr, IndexExpr, MemberExpr,
    AnonymousFunction, TernaryExpr
)
from .objects import (
    VppObject, VppNumber, VppString, VppBoolean, VppNull,
    VppList, VppDict, VppFunction, VppBuiltinFunction,
    VppClass, VppInstance, ReturnSignal, BreakSignal, ContinueSignal,
    VppRuntimeError, VPP_DUNG, VPP_SAI, VPP_RONG
)
from .environment import Environment
from .builtins import get_builtin_scope, py_to_vpp

class Interpreter:
    def __init__(self, base_dir: str = "."):
        self.base_dir = base_dir
        self.global_env = Environment()
        self._init_builtins()

    def _init_builtins(self):
        builtins = get_builtin_scope()
        for name, fn in builtins.items():
            self.global_env.define(name, fn, is_const=True)

    def eval(self, node: Optional[ASTNode], env: Optional[Environment] = None) -> VppObject:
        if node is None:
            return VPP_RONG
        if env is None:
            env = self.global_env

        # Statements
        if isinstance(node, Program):
            return self._eval_program(node, env)
        elif isinstance(node, Block):
            return self._eval_block(node, env)
        elif isinstance(node, VarDecl):
            return self._eval_var_decl(node, env)
        elif isinstance(node, IfStmt):
            return self._eval_if_stmt(node, env)
        elif isinstance(node, WhileStmt):
            return self._eval_while_stmt(node, env)
        elif isinstance(node, ForInStmt):
            return self._eval_for_in_stmt(node, env)
        elif isinstance(node, BreakStmt):
            raise BreakSignal()
        elif isinstance(node, ContinueStmt):
            raise ContinueSignal()
        elif isinstance(node, ReturnStmt):
            val = self.eval(node.value, env) if node.value is not None else VPP_RONG
            raise ReturnSignal(val)
        elif isinstance(node, FunctionDecl):
            return self._eval_function_decl(node, env)
        elif isinstance(node, ClassDecl):
            return self._eval_class_decl(node, env)
        elif isinstance(node, TryCatchStmt):
            return self._eval_try_catch_stmt(node, env)
        elif isinstance(node, ThrowStmt):
            val = self.eval(node.expr, env)
            msg = val.to_string() if val is not None else "Ngoai le khong ro"
            raise VppRuntimeError(msg, node.line, node.column)
        elif isinstance(node, ImportStmt):
            return self._eval_import_stmt(node, env)
        elif isinstance(node, ExprStmt):
            return self.eval(node.expr, env)

        # Expressions
        elif isinstance(node, NumberLiteral):
            return VppNumber(node.value)
        elif isinstance(node, StringLiteral):
            return VppString(node.value)
        elif isinstance(node, BooleanLiteral):
            return VPP_DUNG if node.value else VPP_SAI
        elif isinstance(node, NullLiteral):
            return VPP_RONG
        elif isinstance(node, Identifier):
            return env.get(node.name, node.line, node.column)
        elif isinstance(node, SelfExpr):
            return env.get("ban_than", node.line, node.column)
        elif isinstance(node, ListLiteral):
            elements = [self.eval(elem, env) for elem in node.elements]
            return VppList(elements)
        elif isinstance(node, DictLiteral):
            pairs = {}
            for k_node, v_node in node.pairs:
                k = self.eval(k_node, env)
                v = self.eval(v_node, env)
                pairs[k] = v
            return VppDict(pairs)
        elif isinstance(node, AnonymousFunction):
            return VppFunction("<an_danh>", node.params, node.body, env)
        elif isinstance(node, UnaryOp):
            return self._eval_unary(node, env)
        elif isinstance(node, BinaryOp):
            return self._eval_binary(node, env)
        elif isinstance(node, Assign):
            return self._eval_assign(node, env)
        elif isinstance(node, CallExpr):
            return self._eval_call(node, env)
        elif isinstance(node, IndexExpr):
            return self._eval_index(node, env)
        elif isinstance(node, MemberExpr):
            return self._eval_member(node, env)
        elif isinstance(node, TernaryExpr):
            cond = self.eval(node.condition, env)
            if cond.is_truthy():
                return self.eval(node.true_expr, env)
            else:
                return self.eval(node.false_expr, env)

        raise VppRuntimeError(f"Node AST khong xac dinh: {type(node).__name__}", node.line, node.column)

    def _eval_program(self, node: Program, env: Environment) -> VppObject:
        result = VPP_RONG
        for stmt in node.statements:
            result = self.eval(stmt, env)
        return result

    def _eval_block(self, node: Block, env: Environment, new_scope: bool = True) -> VppObject:
        block_env = Environment(parent=env) if new_scope else env
        result = VPP_RONG
        for stmt in node.statements:
            result = self.eval(stmt, block_env)
        return result

    def _eval_var_decl(self, node: VarDecl, env: Environment) -> VppObject:
        val = self.eval(node.initializer, env) if node.initializer is not None else VPP_RONG
        env.define(node.name, val, is_const=node.is_const)
        return val

    def _eval_if_stmt(self, node: IfStmt, env: Environment) -> VppObject:
        cond_val = self.eval(node.condition, env)
        if cond_val.is_truthy():
            return self.eval(node.then_branch, env)

        for elif_cond, elif_branch in node.elif_branches:
            if self.eval(elif_cond, env).is_truthy():
                return self.eval(elif_branch, env)

        if node.else_branch is not None:
            return self.eval(node.else_branch, env)

        return VPP_RONG

    def _eval_while_stmt(self, node: WhileStmt, env: Environment) -> VppObject:
        result = VPP_RONG
        while self.eval(node.condition, env).is_truthy():
            try:
                result = self.eval(node.body, env)
            except BreakSignal:
                break
            except ContinueSignal:
                continue
        return result

    def _eval_for_in_stmt(self, node: ForInStmt, env: Environment) -> VppObject:
        iterable = self.eval(node.iterable, env)
        items = []

        if isinstance(iterable, VppList):
            items = iterable.elements
        elif isinstance(iterable, VppString):
            items = [VppString(ch) for ch in iterable.value]
        elif isinstance(iterable, VppDict):
            items = list(iterable.pairs.keys())
        else:
            raise VppRuntimeError(f"Doi tuong kieu '{iterable.type_name()}' khong the lap qua", node.line, node.column)

        loop_env = Environment(parent=env)
        result = VPP_RONG

        for item in items:
            loop_env.define(node.var_name, item)
            try:
                result = self.eval(node.body, loop_env)
            except BreakSignal:
                break
            except ContinueSignal:
                continue

        return result

    def _eval_function_decl(self, node: FunctionDecl, env: Environment) -> VppObject:
        fn = VppFunction(node.name, node.params, node.body, env)
        env.define(node.name, fn)
        return fn

    def _eval_class_decl(self, node: ClassDecl, env: Environment) -> VppObject:
        parent_class = None
        if node.parent_name:
            parent_obj = env.get(node.parent_name, node.line, node.column)
            if not isinstance(parent_obj, VppClass):
                raise VppRuntimeError(f"Lop cha '{node.parent_name}' phai la mot lop hop le", node.line, node.column)
            parent_class = parent_obj

        methods = {}
        for m_decl in node.methods:
            methods[m_decl.name] = VppFunction(m_decl.name, m_decl.params, m_decl.body, env)

        klass = VppClass(node.name, parent_class, methods)
        env.define(node.name, klass)
        return klass

    def _eval_try_catch_stmt(self, node: TryCatchStmt, env: Environment) -> VppObject:
        try:
            return self.eval(node.try_block, env)
        except VppRuntimeError as e:
            if node.catch_block is not None:
                catch_env = Environment(parent=env)
                if node.error_var:
                    catch_env.define(node.error_var, VppString(e.message))
                return self.eval(node.catch_block, catch_env)
            raise e
        finally:
            if node.finally_block is not None:
                self.eval(node.finally_block, env)

    def _eval_import_stmt(self, node: ImportStmt, env: Environment) -> VppObject:
        from .lexer import Lexer
        from .parser import Parser

        target_path = node.module_path
        if not os.path.isabs(target_path):
            target_path = os.path.join(self.base_dir, target_path)

        if not target_path.endswith(".vpp"):
            target_path += ".vpp"

        if not os.path.exists(target_path):
            raise VppRuntimeError(f"Khong tim thay tep thu vien: '{node.module_path}'", node.line, node.column)

        with open(target_path, "r", encoding="utf-8") as f:
            code = f.read()

        lexer = Lexer(code, filename=target_path)
        tokens = lexer.tokenize()
        parser = Parser(tokens, filename=target_path)
        ast = parser.parse()

        # Execute in a new module environment
        mod_env = Environment(parent=self.global_env)
        self.eval(ast, mod_env)

        if node.alias:
            # Package exported variables into a dict
            exports = {}
            for k, v in mod_env.values.items():
                exports[VppString(k)] = v
            env.define(node.alias, VppDict(exports))
        else:
            # Export everything into current env
            for k, v in mod_env.values.items():
                env.define(k, v)

        return VPP_DUNG

    def _eval_unary(self, node: UnaryOp, env: Environment) -> VppObject:
        # Check postfix ++ / --
        if node.is_postfix:
            if isinstance(node.operand, Identifier):
                cur = env.get(node.operand.name, node.line, node.column)
                if not isinstance(cur, VppNumber):
                    raise VppRuntimeError(f"Toan tu '{node.op}' chi ap dung cho so", node.line, node.column)
                new_val = VppNumber(cur.value + 1 if node.op == "++" else cur.value - 1)
                env.assign(node.operand.name, new_val, node.line, node.column)
                return cur
            raise VppRuntimeError("Toan tu ++ hoac -- chi ap dung cho bien", node.line, node.column)

        # Prefix operators
        if node.op == "++":
            if isinstance(node.operand, Identifier):
                cur = env.get(node.operand.name, node.line, node.column)
                if not isinstance(cur, VppNumber):
                    raise VppRuntimeError("Toan tu '++' chi ap dung cho so", node.line, node.column)
                new_val = VppNumber(cur.value + 1)
                env.assign(node.operand.name, new_val, node.line, node.column)
                return new_val
            raise VppRuntimeError("Toan tu '++' chi ap dung cho bien", node.line, node.column)

        if node.op == "--":
            if isinstance(node.operand, Identifier):
                cur = env.get(node.operand.name, node.line, node.column)
                if not isinstance(cur, VppNumber):
                    raise VppRuntimeError("Toan tu '--' chi ap dung cho so", node.line, node.column)
                new_val = VppNumber(cur.value - 1)
                env.assign(node.operand.name, new_val, node.line, node.column)
                return new_val
            raise VppRuntimeError("Toan tu '--' chi ap dung cho bien", node.line, node.column)

        val = self.eval(node.operand, env)
        if node.op == "-":
            if isinstance(val, VppNumber):
                return VppNumber(-val.value)
            raise VppRuntimeError("Dau '-' chi ap dung cho so", node.line, node.column)
        elif node.op == "+":
            if isinstance(val, VppNumber):
                return val
            raise VppRuntimeError("Dau '+' chi ap dung cho so", node.line, node.column)
        elif node.op in ("!", "phu_dinh"):
            return VPP_SAI if val.is_truthy() else VPP_DUNG

        raise VppRuntimeError(f"Toan tu mot ngoi khong hop le: '{node.op}'", node.line, node.column)

    def _eval_binary(self, node: BinaryOp, env: Environment) -> VppObject:
        # Short-circuit logical operators
        if node.op in ("va", "&&"):
            left_val = self.eval(node.left, env)
            if not left_val.is_truthy():
                return left_val
            return self.eval(node.right, env)

        if node.op in ("hoac", "||"):
            left_val = self.eval(node.left, env)
            if left_val.is_truthy():
                return left_val
            return self.eval(node.right, env)

        left = self.eval(node.left, env)
        right = self.eval(node.right, env)

        # Equality
        if node.op == "==":
            return VPP_DUNG if left == right else VPP_SAI
        if node.op == "!=":
            return VPP_DUNG if left != right else VPP_SAI

        # Numbers math
        if isinstance(left, VppNumber) and isinstance(right, VppNumber):
            if node.op == "+": return VppNumber(left.value + right.value)
            if node.op == "-": return VppNumber(left.value - right.value)
            if node.op == "*": return VppNumber(left.value * right.value)
            if node.op == "/":
                if right.value == 0:
                    raise VppRuntimeError("Loi chia cho 0", node.line, node.column)
                return VppNumber(left.value / right.value)
            if node.op == "%":
                if right.value == 0:
                    raise VppRuntimeError("Loi chia lay du cho 0", node.line, node.column)
                return VppNumber(left.value % right.value)
            if node.op in ("^", "**"): return VppNumber(left.value ** right.value)
            if node.op == "<": return VPP_DUNG if left.value < right.value else VPP_SAI
            if node.op == "<=": return VPP_DUNG if left.value <= right.value else VPP_SAI
            if node.op == ">": return VPP_DUNG if left.value > right.value else VPP_SAI
            if node.op == ">=": return VPP_DUNG if left.value >= right.value else VPP_SAI

        # String operations
        if isinstance(left, VppString) or isinstance(right, VppString):
            if node.op == "+":
                return VppString(left.to_string() + right.to_string())
            if isinstance(left, VppString) and isinstance(right, VppNumber) and node.op == "*":
                return VppString(left.value * int(right.value))
            if isinstance(left, VppString) and isinstance(right, VppString):
                if node.op == "<": return VPP_DUNG if left.value < right.value else VPP_SAI
                if node.op == "<=": return VPP_DUNG if left.value <= right.value else VPP_SAI
                if node.op == ">": return VPP_DUNG if left.value > right.value else VPP_SAI
                if node.op == ">=": return VPP_DUNG if left.value >= right.value else VPP_SAI

        # List concatenation & replication
        if isinstance(left, VppList):
            if node.op == "+" and isinstance(right, VppList):
                return VppList(left.elements + right.elements)
            if node.op == "*" and isinstance(right, VppNumber):
                return VppList(left.elements * int(right.value))

        raise VppRuntimeError(f"Khong the ap dung toan tu '{node.op}' giua kieu '{left.type_name()}' va '{right.type_name()}'", node.line, node.column)

    def _eval_assign(self, node: Assign, env: Environment) -> VppObject:
        val = self.eval(node.value, env)

        if isinstance(node.target, Identifier):
            if node.op == "=":
                env.assign(node.target.name, val, node.line, node.column)
                return val
            else:
                cur = env.get(node.target.name, node.line, node.column)
                bin_op = node.op[:-1] # e.g. += -> +
                calc_val = self._apply_binary_op(cur, bin_op, val, node.line, node.column)
                env.assign(node.target.name, calc_val, node.line, node.column)
                return calc_val

        elif isinstance(node.target, IndexExpr):
            container = self.eval(node.target.target, env)
            idx = self.eval(node.target.index, env)

            if isinstance(container, VppList):
                if not isinstance(idx, VppNumber):
                    raise VppRuntimeError("Chi muc danh sach phai la so", node.line, node.column)
                i = int(idx.value)
                if i < 0:
                    i = len(container.elements) + i
                if 0 <= i < len(container.elements):
                    if node.op == "=":
                        container.elements[i] = val
                        return val
                    else:
                        cur = container.elements[i]
                        bin_op = node.op[:-1]
                        calc_val = self._apply_binary_op(cur, bin_op, val, node.line, node.column)
                        container.elements[i] = calc_val
                        return calc_val
                raise VppRuntimeError(f"Chi muc vuot ngoai pham vi: {i}", node.line, node.column)

            elif isinstance(container, VppDict):
                if node.op == "=":
                    container.pairs[idx] = val
                    return val
                else:
                    cur = container.pairs.get(idx, VPP_RONG)
                    bin_op = node.op[:-1]
                    calc_val = self._apply_binary_op(cur, bin_op, val, node.line, node.column)
                    container.pairs[idx] = calc_val
                    return calc_val

            raise VppRuntimeError(f"Khong the gan chi muc cho kieu '{container.type_name()}'", node.line, node.column)

        elif isinstance(node.target, MemberExpr):
            obj = self.eval(node.target.target, env)
            if isinstance(obj, VppInstance):
                if node.op == "=":
                    obj.set_property(node.target.member, val)
                    return val
                else:
                    cur = obj.get_property(node.target.member)
                    bin_op = node.op[:-1]
                    calc_val = self._apply_binary_op(cur, bin_op, val, node.line, node.column)
                    obj.set_property(node.target.member, calc_val)
                    return calc_val
            raise VppRuntimeError(f"Khong the gan thuoc tinh cho doi tuong kieu '{obj.type_name()}'", node.line, node.column)

        raise VppRuntimeError("Dich den phep gan khong hop le", node.line, node.column)

    def _apply_binary_op(self, left: VppObject, op: str, right: VppObject, line: int, col: int) -> VppObject:
        fake_node = BinaryOp(left=None, op=op, right=None, line=line, column=col)
        # Direct evaluation helper
        if isinstance(left, VppNumber) and isinstance(right, VppNumber):
            if op == "+": return VppNumber(left.value + right.value)
            if op == "-": return VppNumber(left.value - right.value)
            if op == "*": return VppNumber(left.value * right.value)
            if op == "/":
                if right.value == 0: raise VppRuntimeError("Loi chia cho 0", line, col)
                return VppNumber(left.value / right.value)
            if op == "%":
                if right.value == 0: raise VppRuntimeError("Loi chia lay du cho 0", line, col)
                return VppNumber(left.value % right.value)
            if op in ("^", "**"): return VppNumber(left.value ** right.value)
        if isinstance(left, VppString) or isinstance(right, VppString):
            if op == "+": return VppString(left.to_string() + right.to_string())
        if isinstance(left, VppList) and isinstance(right, VppList) and op == "+":
            return VppList(left.elements + right.elements)
        raise VppRuntimeError(f"Khong the thuc hien '{op}' giua '{left.type_name()}' va '{right.type_name()}'", line, col)

    def _eval_call(self, node: CallExpr, env: Environment) -> VppObject:
        callee = self.eval(node.callee, env)
        args = [self.eval(arg, env) for arg in node.args]

        if isinstance(callee, VppBuiltinFunction):
            return callee.fn(args)

        elif isinstance(callee, VppFunction):
            return self._call_vpp_function(callee, args, node.line, node.column)

        elif isinstance(callee, VppClass):
            # Class instantiation -> create new instance and run constructor if exists
            instance = VppInstance(callee)
            init_method = callee.find_method("khoi_tao")
            if init_method is not None:
                self._call_vpp_function(init_method, args, node.line, node.column, instance=instance)
            return instance

        raise VppRuntimeError(f"Doi tuong kieu '{callee.type_name()}' khong the goi nhu mot ham", node.line, node.column)

    def _call_vpp_function(self, fn: VppFunction, args: List[VppObject], line: int, col: int, instance: Optional[VppInstance] = None) -> VppObject:
        fn_env = Environment(parent=fn.env)

        if instance is not None:
            fn_env.define("ban_than", instance)

        if len(args) != len(fn.params):
            raise VppRuntimeError(
                f"Ham '{fn.name}' yeu cau {len(fn.params)} tham so nhung nhan duoc {len(args)}",
                line, col
            )

        for param_name, arg_val in zip(fn.params, args):
            fn_env.define(param_name, arg_val)

        try:
            self.eval(fn.body, fn_env)
            return VPP_RONG
        except ReturnSignal as ret:
            return ret.value

    def _eval_index(self, node: IndexExpr, env: Environment) -> VppObject:
        target = self.eval(node.target, env)

        if node.is_slice:
            # Slicing
            start_idx = 0
            if node.index is not None:
                s_val = self.eval(node.index, env)
                if not isinstance(s_val, VppNumber):
                    raise VppRuntimeError("Chi muc cat phai la so", node.line, node.column)
                start_idx = int(s_val.value)

            end_idx = None
            if node.end_index is not None:
                e_val = self.eval(node.end_index, env)
                if not isinstance(e_val, VppNumber):
                    raise VppRuntimeError("Chi muc cat phai la so", node.line, node.column)
                end_idx = int(e_val.value)

            if isinstance(target, VppList):
                sliced = target.elements[start_idx:end_idx]
                return VppList(sliced)
            elif isinstance(target, VppString):
                sliced = target.value[start_idx:end_idx]
                return VppString(sliced)
            raise VppRuntimeError(f"Kieu '{target.type_name()}' khong ho tro cat lat (slice)", node.line, node.column)

        # Single index
        idx = self.eval(node.index, env)

        if isinstance(target, VppList):
            if not isinstance(idx, VppNumber):
                raise VppRuntimeError("Chi muc danh sach phai la so", node.line, node.column)
            i = int(idx.value)
            if i < 0:
                i = len(target.elements) + i
            if 0 <= i < len(target.elements):
                return target.elements[i]
            raise VppRuntimeError(f"Chi muc danh sach vuot ngoai pham vi: {i} (do dai: {len(target.elements)})", node.line, node.column)

        elif isinstance(target, VppString):
            if not isinstance(idx, VppNumber):
                raise VppRuntimeError("Chi muc chuoi phai la so", node.line, node.column)
            i = int(idx.value)
            if i < 0:
                i = len(target.value) + i
            if 0 <= i < len(target.value):
                return VppString(target.value[i])
            raise VppRuntimeError(f"Chi muc chuoi vuot ngoai pham vi: {i} (do dai: {len(target.value)})", node.line, node.column)

        elif isinstance(target, VppDict):
            if idx in target.pairs:
                return target.pairs[idx]
            return VPP_RONG

        raise VppRuntimeError(f"Kieu '{target.type_name()}' khong ho tro truy cap chi muc", node.line, node.column)

    def _eval_member(self, node: MemberExpr, env: Environment) -> VppObject:
        target = self.eval(node.target, env)

        if isinstance(target, VppInstance):
            # Check fields or methods
            if node.member in target.fields:
                return target.fields[node.member]
            method = target.klass.find_method(node.member)
            if method is not None:
                # Bind method to instance
                def bound_method(args: List[VppObject]) -> VppObject:
                    return self._call_vpp_function(method, args, node.line, node.column, instance=target)
                return VppBuiltinFunction(f"{target.klass.name}.{node.member}", bound_method)
            return VPP_RONG

        elif isinstance(target, VppDict):
            # Allow obj.prop syntax for dict string keys
            key_str = VppString(node.member)
            if key_str in target.pairs:
                return target.pairs[key_str]
            return VPP_RONG

        # Built-in object methods
        if isinstance(target, VppList):
            if node.member == "them":
                return VppBuiltinFunction("them", lambda args: (target.elements.append(args[0]), target)[1])
            if node.member == "do_dai":
                return VppBuiltinFunction("do_dai", lambda args: VppNumber(len(target.elements)))
            if node.member == "xoa":
                return VppBuiltinFunction("xoa", lambda args: target.elements.pop(int(args[0].value) if args else -1))

        if isinstance(target, VppString):
            if node.member == "do_dai":
                return VppBuiltinFunction("do_dai", lambda args: VppNumber(len(target.value)))
            if node.member == "viet_hoa":
                return VppBuiltinFunction("viet_hoa", lambda args: VppString(target.value.upper()))
            if node.member == "viet_thuong":
                return VppBuiltinFunction("viet_thuong", lambda args: VppString(target.value.lower()))

        raise VppRuntimeError(f"Doi tuong kieu '{target.type_name()}' khong co thuoc tinh '{node.member}'", node.line, node.column)
