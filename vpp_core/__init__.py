"""
V++ Programming Language Package
"""

__version__ = "1.0.0"
__author__ = "V++ Language Core Team"

from .tokens import Token, TokenType
from .lexer import Lexer, LexerError
from .ast_nodes import ASTNode, Program
from .parser import Parser, ParserError
from .objects import VppObject, VppRuntimeError
from .environment import Environment
from .evaluator import Interpreter
from .transpiler import Transpiler

def run_code(code: str, filename: str = "<truc_tiep>", base_dir: str = ".") -> VppObject:
    lexer = Lexer(code, filename=filename)
    tokens = lexer.tokenize()
    parser = Parser(tokens, filename=filename)
    ast = parser.parse()
    interpreter = Interpreter(base_dir=base_dir)
    return interpreter.eval(ast)
