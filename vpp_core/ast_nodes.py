"""
V++ Programming Language - Abstract Syntax Tree (AST) Nodes
"""

from dataclasses import dataclass, field
from typing import List, Tuple, Optional, Any

@dataclass
class ASTNode:
    line: int = 0
    column: int = 0

# --- Statements ---

@dataclass
class Program(ASTNode):
    statements: List[ASTNode] = field(default_factory=list)

@dataclass
class Block(ASTNode):
    statements: List[ASTNode] = field(default_factory=list)

@dataclass
class VarDecl(ASTNode):
    name: str = ""
    initializer: Optional[ASTNode] = None
    is_const: bool = False

@dataclass
class IfStmt(ASTNode):
    condition: ASTNode = None
    then_branch: ASTNode = None
    elif_branches: List[Tuple[ASTNode, ASTNode]] = field(default_factory=list)
    else_branch: Optional[ASTNode] = None

@dataclass
class WhileStmt(ASTNode):
    condition: ASTNode = None
    body: ASTNode = None

@dataclass
class ForInStmt(ASTNode):
    var_name: str = ""
    iterable: ASTNode = None
    body: ASTNode = None

@dataclass
class BreakStmt(ASTNode):
    pass

@dataclass
class ContinueStmt(ASTNode):
    pass

@dataclass
class ReturnStmt(ASTNode):
    value: Optional[ASTNode] = None

@dataclass
class FunctionDecl(ASTNode):
    name: str = ""
    params: List[str] = field(default_factory=list)
    body: ASTNode = None

@dataclass
class ClassDecl(ASTNode):
    name: str = ""
    parent_name: Optional[str] = None
    methods: List[FunctionDecl] = field(default_factory=list)

@dataclass
class TryCatchStmt(ASTNode):
    try_block: ASTNode = None
    error_var: Optional[str] = None
    catch_block: Optional[ASTNode] = None
    finally_block: Optional[ASTNode] = None

@dataclass
class ThrowStmt(ASTNode):
    expr: ASTNode = None

@dataclass
class ImportStmt(ASTNode):
    module_path: str = ""
    alias: Optional[str] = None

@dataclass
class ExprStmt(ASTNode):
    expr: ASTNode = None

# --- Expressions ---

@dataclass
class NumberLiteral(ASTNode):
    value: Any = 0

@dataclass
class StringLiteral(ASTNode):
    value: str = ""

@dataclass
class BooleanLiteral(ASTNode):
    value: bool = False

@dataclass
class NullLiteral(ASTNode):
    pass

@dataclass
class Identifier(ASTNode):
    name: str = ""

@dataclass
class SelfExpr(ASTNode):
    pass

@dataclass
class ListLiteral(ASTNode):
    elements: List[ASTNode] = field(default_factory=list)

@dataclass
class DictLiteral(ASTNode):
    pairs: List[Tuple[ASTNode, ASTNode]] = field(default_factory=list)

@dataclass
class UnaryOp(ASTNode):
    op: str = ""
    operand: ASTNode = None
    is_postfix: bool = False

@dataclass
class BinaryOp(ASTNode):
    left: ASTNode = None
    op: str = ""
    right: ASTNode = None

@dataclass
class Assign(ASTNode):
    target: ASTNode = None
    op: str = "="  # =, +=, -=, *=, /=, %=
    value: ASTNode = None

@dataclass
class CallExpr(ASTNode):
    callee: ASTNode = None
    args: List[ASTNode] = field(default_factory=list)

@dataclass
class IndexExpr(ASTNode):
    target: ASTNode = None
    index: ASTNode = None
    end_index: Optional[ASTNode] = None  # for slicing: target[start:end]
    is_slice: bool = False

@dataclass
class MemberExpr(ASTNode):
    target: ASTNode = None
    member: str = ""

@dataclass
class AnonymousFunction(ASTNode):
    params: List[str] = field(default_factory=list)
    body: ASTNode = None

@dataclass
class TernaryExpr(ASTNode):
    condition: ASTNode = None
    true_expr: ASTNode = None
    false_expr: ASTNode = None
