"""
V++ Programming Language - Lexer / Tokenizer
"""

from typing import List, Optional
from .tokens import Token, TokenType, KEYWORDS

class LexerError(Exception):
    def __init__(self, message: str, line: int, column: int):
        super().__init__(message)
        self.message = message
        self.line = line
        self.column = column

class Lexer:
    def __init__(self, source_code: str, filename: str = "<truc_tiep>"):
        self.source = source_code
        self.filename = filename
        self.length = len(source_code)
        self.pos = 0
        self.line = 1
        self.column = 1

    def _peek(self, offset: int = 0) -> str:
        target = self.pos + offset
        if target < self.length:
            return self.source[target]
        return '\0'

    def _advance(self) -> str:
        if self.pos >= self.length:
            return '\0'
        ch = self.source[self.pos]
        self.pos += 1
        if ch == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return ch

    def _match(self, expected: str) -> bool:
        if self._peek() == expected:
            self._advance()
            return True
        return False

    def tokenize(self) -> List[Token]:
        tokens: List[Token] = []
        while self.pos < self.length:
            ch = self._peek()

            # Skip whitespace (except newlines if we want semicolons/newlines)
            if ch in ' \t\r':
                self._advance()
                continue

            # Newlines
            if ch == '\n':
                start_line, start_col = self.line, self.column
                self._advance()
                tokens.append(Token(TokenType.NEWLINE, '\n', start_line, start_col))
                continue

            # Single-line comment // or #
            if ch == '#' or (ch == '/' and self._peek(1) == '/'):
                while self._peek() != '\n' and self._peek() != '\0':
                    self._advance()
                continue

            # Multi-line comment /* ... */
            if ch == '/' and self._peek(1) == '*':
                start_line, start_col = self.line, self.column
                self._advance() # /
                self._advance() # *
                while True:
                    if self._peek() == '\0':
                        raise LexerError("Chu thich nhieu dong chua duoc dong '*/'", start_line, start_col)
                    if self._peek() == '*' and self._peek(1) == '/':
                        self._advance() # *
                        self._advance() # /
                        break
                    self._advance()
                continue

            start_line, start_col = self.line, self.column

            # Numbers
            if ch.isdigit():
                tokens.append(self._read_number(start_line, start_col))
                continue

            # String literal
            if ch in ('"', "'"):
                tokens.append(self._read_string(ch, start_line, start_col))
                continue

            # Identifiers and keywords
            if ch.isalpha() or ch == '_':
                tokens.append(self._read_identifier(start_line, start_col))
                continue

            # Operators and Delimiters
            self._advance()

            if ch == '+':
                if self._match('+'):
                    tokens.append(Token(TokenType.PLUS_PLUS, '++', start_line, start_col, 2))
                elif self._match('='):
                    tokens.append(Token(TokenType.PLUS_ASSIGN, '+=', start_line, start_col, 2))
                else:
                    tokens.append(Token(TokenType.PLUS, '+', start_line, start_col, 1))
            elif ch == '-':
                if self._match('-'):
                    tokens.append(Token(TokenType.MINUS_MINUS, '--', start_line, start_col, 2))
                elif self._match('='):
                    tokens.append(Token(TokenType.MINUS_ASSIGN, '-=', start_line, start_col, 2))
                elif self._match('>'):
                    tokens.append(Token(TokenType.ARROW, '->', start_line, start_col, 2))
                else:
                    tokens.append(Token(TokenType.MINUS, '-', start_line, start_col, 1))
            elif ch == '*':
                if self._match('*'):
                    tokens.append(Token(TokenType.POWER, '**', start_line, start_col, 2))
                elif self._match('='):
                    tokens.append(Token(TokenType.STAR_ASSIGN, '*=', start_line, start_col, 2))
                else:
                    tokens.append(Token(TokenType.STAR, '*', start_line, start_col, 1))
            elif ch == '/':
                if self._match('='):
                    tokens.append(Token(TokenType.SLASH_ASSIGN, '/=', start_line, start_col, 2))
                else:
                    tokens.append(Token(TokenType.SLASH, '/', start_line, start_col, 1))
            elif ch == '%':
                if self._match('='):
                    tokens.append(Token(TokenType.PERCENT_ASSIGN, '%=', start_line, start_col, 2))
                else:
                    tokens.append(Token(TokenType.PERCENT, '%', start_line, start_col, 1))
            elif ch == '^':
                tokens.append(Token(TokenType.POWER, '^', start_line, start_col, 1))
            elif ch == '=':
                if self._match('='):
                    tokens.append(Token(TokenType.EQ, '==', start_line, start_col, 2))
                elif self._match('>'):
                    tokens.append(Token(TokenType.ARROW, '=>', start_line, start_col, 2))
                else:
                    tokens.append(Token(TokenType.ASSIGN, '=', start_line, start_col, 1))
            elif ch == '!':
                if self._match('='):
                    tokens.append(Token(TokenType.NOT_EQ, '!=', start_line, start_col, 2))
                else:
                    tokens.append(Token(TokenType.NOT, '!', start_line, start_col, 1))
            elif ch == '<':
                if self._match('='):
                    tokens.append(Token(TokenType.LTE, '<=', start_line, start_col, 2))
                else:
                    tokens.append(Token(TokenType.LT, '<', start_line, start_col, 1))
            elif ch == '>':
                if self._match('='):
                    tokens.append(Token(TokenType.GTE, '>=', start_line, start_col, 2))
                else:
                    tokens.append(Token(TokenType.GT, '>', start_line, start_col, 1))
            elif ch == '&':
                if self._match('&'):
                    tokens.append(Token(TokenType.AND, '&&', start_line, start_col, 2))
                else:
                    raise LexerError(f"Ky tu '&' khong hop le, ban co muon dung '&&' hoac 'va'?", start_line, start_col)
            elif ch == '|':
                if self._match('|'):
                    tokens.append(Token(TokenType.OR, '||', start_line, start_col, 2))
                else:
                    raise LexerError(f"Ky tu '|' khong hop le, ban co muon dung '||' hoac 'hoac'?", start_line, start_col)
            elif ch == '(':
                tokens.append(Token(TokenType.LPAREN, '(', start_line, start_col, 1))
            elif ch == ')':
                tokens.append(Token(TokenType.RPAREN, ')', start_line, start_col, 1))
            elif ch == '[':
                tokens.append(Token(TokenType.LBRACKET, '[', start_line, start_col, 1))
            elif ch == ']':
                tokens.append(Token(TokenType.RBRACKET, ']', start_line, start_col, 1))
            elif ch == '{':
                tokens.append(Token(TokenType.LBRACE, '{', start_line, start_col, 1))
            elif ch == '}':
                tokens.append(Token(TokenType.RBRACE, '}', start_line, start_col, 1))
            elif ch == ',':
                tokens.append(Token(TokenType.COMMA, ',', start_line, start_col, 1))
            elif ch == '.':
                tokens.append(Token(TokenType.DOT, '.', start_line, start_col, 1))
            elif ch == ':':
                tokens.append(Token(TokenType.COLON, ':', start_line, start_col, 1))
            elif ch == ';':
                tokens.append(Token(TokenType.SEMICOLON, ';', start_line, start_col, 1))
            else:
                raise LexerError(f"Ky tu la khong xac dinh: '{ch}'", start_line, start_col)

        tokens.append(Token(TokenType.EOF, '', self.line, self.column, 0))
        return tokens

    def _read_number(self, start_line: int, start_col: int) -> Token:
        num_str = ""
        # Check for 0x, 0b, 0o
        if self._peek() == '0' and self._peek(1) in ('x', 'X', 'b', 'B', 'o', 'O'):
            num_str += self._advance() # '0'
            num_str += self._advance() # 'x', etc.
            while self._peek().isalnum() or self._peek() == '_':
                if self._peek() != '_':
                    num_str += self._peek()
                self._advance()
            try:
                val = int(num_str, 0)
                return Token(TokenType.INT, val, start_line, start_col, len(num_str))
            except ValueError:
                raise LexerError(f"So he dem khong hop le: {num_str}", start_line, start_col)

        is_float = False
        while self._peek().isdigit() or self._peek() == '_':
            if self._peek() != '_':
                num_str += self._peek()
            self._advance()

        if self._peek() == '.' and self._peek(1).isdigit():
            is_float = True
            num_str += self._advance() # '.'
            while self._peek().isdigit() or self._peek() == '_':
                if self._peek() != '_':
                    num_str += self._peek()
                self._advance()

        if self._peek() in ('e', 'E'):
            is_float = True
            num_str += self._advance()
            if self._peek() in ('+', '-'):
                num_str += self._advance()
            while self._peek().isdigit() or self._peek() == '_':
                if self._peek() != '_':
                    num_str += self._peek()
                self._advance()

        if is_float:
            return Token(TokenType.FLOAT, float(num_str), start_line, start_col, len(num_str))
        else:
            return Token(TokenType.INT, int(num_str), start_line, start_col, len(num_str))

    def _read_string(self, quote_char: str, start_line: int, start_col: int) -> Token:
        self._advance() # opening quote
        chars = []
        while True:
            ch = self._peek()
            if ch == '\0':
                raise LexerError(f"Chuoi chua duoc dong bang dau ngoac {quote_char}", start_line, start_col)
            if ch == quote_char:
                self._advance()
                break
            if ch == '\\':
                self._advance()
                esc = self._advance()
                if esc == 'n': chars.append('\n')
                elif esc == 't': chars.append('\t')
                elif esc == 'r': chars.append('\r')
                elif esc == '\\': chars.append('\\')
                elif esc == '"': chars.append('"')
                elif esc == "'": chars.append("'")
                elif esc == '0': chars.append('\0')
                else: chars.append(esc)
            else:
                chars.append(self._advance())
        
        result_str = "".join(chars)
        return Token(TokenType.STRING, result_str, start_line, start_col, len(result_str) + 2)

    def _read_identifier(self, start_line: int, start_col: int) -> Token:
        ident = ""
        while self._peek().isalnum() or self._peek() == '_':
            ident += self._advance()

        # Check if keyword
        token_type = KEYWORDS.get(ident, TokenType.IDENTIFIER)
        value = ident
        if token_type == TokenType.DUNG:
            value = True
        elif token_type == TokenType.SAI:
            value = False
        elif token_type == TokenType.RONG:
            value = None

        return Token(token_type, value, start_line, start_col, len(ident))
