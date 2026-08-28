"""
V++ Programming Language - Parser
Recursive Descent Parser with Precedence Climbing
"""

from typing import List, Optional, Tuple, Any
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

class ParserError(Exception):
    def __init__(self, message: str, token: Token):
        super().__init__(message)
        self.message = message
        self.token = token

class Parser:
    def __init__(self, tokens: List[Token], filename: str = "<truc_tiep>"):
        self.tokens = tokens
        self.filename = filename
        self.pos = 0

    def _peek(self, offset: int = 0) -> Token:
        idx = self.pos + offset
        if idx < len(self.tokens):
            return self.tokens[idx]
        return self.tokens[-1] # EOF

    def _is_at_end(self) -> bool:
        return self._peek().type == TokenType.EOF

    def _advance(self) -> Token:
        tok = self._peek()
        if not self._is_at_end():
            self.pos += 1
        return tok

    def _check(self, token_type: TokenType) -> bool:
        if self._is_at_end():
            return False
        return self._peek().type == token_type

    def _match(self, *token_types: TokenType) -> bool:
        for tt in token_types:
            if self._check(tt):
                self._advance()
                return True
        return False

    def _consume(self, token_type: TokenType, err_msg: str) -> Token:
        if self._check(token_type):
            return self._advance()
        tok = self._peek()
        received_str = f"nhận được '{tok.value}'" if tok.value is not None and str(tok.value).strip() else "đã hết dòng lệnh"
        raise ParserError(f"{err_msg} ({received_str})", tok)

    def _skip_newlines(self):
        while self._check(TokenType.NEWLINE):
            self._advance()

    def parse(self) -> Program:
        statements = []
        self._skip_newlines()
        while not self._is_at_end():
            stmt = self._parse_statement()
            if stmt is not None:
                statements.append(stmt)
            self._skip_newlines()
        return Program(statements=statements, line=1, column=1)

    # --- Statement Parsers ---

    def _parse_statement(self) -> Optional[ASTNode]:
        self._skip_newlines()
        if self._is_at_end():
            return None

        tok = self._peek()

        if tok.type in (TokenType.BIEN, TokenType.HANG):
            return self._parse_var_decl()
        elif tok.type == TokenType.NEU:
            return self._parse_if_stmt()
        elif tok.type == TokenType.KHI:
            return self._parse_while_stmt()
        elif tok.type == TokenType.LAP:
            return self._parse_for_in_stmt()
        elif tok.type == TokenType.DUNG_LAP:
            return self._parse_break_stmt()
        elif tok.type == TokenType.TIEP_TUC:
            return self._parse_continue_stmt()
        elif tok.type == TokenType.TRA_VE:
            return self._parse_return_stmt()
        elif tok.type == TokenType.HAM:
            # Check if named function or anonymous
            if self._peek(1).type in (TokenType.IDENTIFIER, TokenType.KHOI_TAO):
                return self._parse_function_decl()
            else:
                return self._parse_expr_stmt()
        elif tok.type == TokenType.LOP:
            return self._parse_class_decl()
        elif tok.type == TokenType.THU:
            return self._parse_try_catch_stmt()
        elif tok.type == TokenType.NEM_LOI:
            return self._parse_throw_stmt()
        elif tok.type == TokenType.DUNG_THU_VIEN:
            return self._parse_import_stmt()
        elif tok.type == TokenType.LBRACE:
            return self._parse_block()
        elif tok.type == TokenType.SEMICOLON:
            self._advance()
            return None
        elif tok.type == TokenType.IDENTIFIER:
            # Check for direct function call without parens: noi "hello", x
            if tok.value in ("noi", "nói", "in", "noi_lien", "nói_liền", "in_lien"):
                next_tok = self._peek(1)
                if next_tok.type not in (TokenType.ASSIGN, TokenType.PLUS_ASSIGN, TokenType.MINUS_ASSIGN, TokenType.DOT, TokenType.LBRACKET, TokenType.LPAREN, TokenType.SEMICOLON, TokenType.NEWLINE, TokenType.RBRACE, TokenType.EOF):
                    call_tok = self._advance()
                    args = []
                    while not self._check(TokenType.SEMICOLON) and not self._check(TokenType.NEWLINE) and not self._check(TokenType.RBRACE) and not self._is_at_end():
                        args.append(self._parse_expression())
                        if not self._match(TokenType.COMMA):
                            break
                    self._match(TokenType.SEMICOLON)
                    callee = Identifier(name=str(call_tok.value), line=call_tok.line, column=call_tok.column)
                    return ExprStmt(expr=CallExpr(callee=callee, args=args, line=call_tok.line, column=call_tok.column), line=call_tok.line, column=call_tok.column)

            return self._parse_expr_stmt()
        else:
            return self._parse_expr_stmt()

    def _parse_var_decl(self) -> VarDecl:
        decl_tok = self._advance() # 'bien' or 'hang'
        is_const = (decl_tok.type == TokenType.HANG)
        
        name_tok = self._consume(TokenType.IDENTIFIER, "Cần tên biến sau 'biến' hoặc 'hằng'")
        name = str(name_tok.value)
        
        initializer = None
        if self._match(TokenType.ASSIGN):
            initializer = self._parse_expression()
        elif is_const:
            raise ParserError("Hằng số ('hằng') bắt buộc phải có giá trị khởi tạo", decl_tok)

        self._match(TokenType.SEMICOLON)
        return VarDecl(name=name, initializer=initializer, is_const=is_const, line=decl_tok.line, column=decl_tok.column)

    def _parse_block(self) -> Block:
        open_tok = self._consume(TokenType.LBRACE, "Cần '{' để bắt đầu khối lệnh")
        statements = []
        self._skip_newlines()
        while not self._check(TokenType.RBRACE) and not self._is_at_end():
            stmt = self._parse_statement()
            if stmt is not None:
                statements.append(stmt)
            self._skip_newlines()
        self._consume(TokenType.RBRACE, "Cần '}' để kết thúc khối lệnh")
        return Block(statements=statements, line=open_tok.line, column=open_tok.column)

    def _normalize_condition(self, node: ASTNode) -> ASTNode:
        if isinstance(node, Assign) and node.op == "=":
            return BinaryOp(left=node.target, op="==", right=node.value, line=node.line, column=node.column)
        return node

    def _parse_if_stmt(self) -> IfStmt:
        if_tok = self._advance() # 'neu'
        
        # Condition can be wrapped in () or plain
        has_paren = self._match(TokenType.LPAREN)
        cond = self._normalize_condition(self._parse_expression())
        if has_paren:
            self._consume(TokenType.RPAREN, "Cần ')' sau biểu thức điều kiện")
            
        self._skip_newlines()
        then_branch = self._parse_block() if self._check(TokenType.LBRACE) else self._parse_statement()

        elif_branches = []
        else_branch = None

        while True:
            self._skip_newlines()
            if self._check(TokenType.KHONG_THI_NEU):
                elif_tok = self._advance()
                has_p = self._match(TokenType.LPAREN)
                elif_cond = self._normalize_condition(self._parse_expression())
                if has_p:
                    self._consume(TokenType.RPAREN, "Cần ')' sau điều kiện 'không_thì_nếu'")
                self._skip_newlines()
                elif_body = self._parse_block() if self._check(TokenType.LBRACE) else self._parse_statement()
                elif_branches.append((elif_cond, elif_body))
            elif self._check(TokenType.KHONG_THI):
                self._advance() # 'khong_thi' / 'nguoc_lai'
                self._skip_newlines()
                # Check if followed immediately by 'neu' (i.e. 'khong_thi neu')
                if self._check(TokenType.NEU):
                    self._advance() # 'neu'
                    has_p = self._match(TokenType.LPAREN)
                    elif_cond = self._normalize_condition(self._parse_expression())
                    if has_p:
                        self._consume(TokenType.RPAREN, "Cần ')' sau điều kiện 'không_thì nếu'")
                    self._skip_newlines()
                    elif_body = self._parse_block() if self._check(TokenType.LBRACE) else self._parse_statement()
                    elif_branches.append((elif_cond, elif_body))
                else:
                    else_branch = self._parse_block() if self._check(TokenType.LBRACE) else self._parse_statement()
                    break
            else:
                break

        return IfStmt(
            condition=cond,
            then_branch=then_branch,
            elif_branches=elif_branches,
            else_branch=else_branch,
            line=if_tok.line,
            column=if_tok.column
        )

    def _parse_while_stmt(self) -> WhileStmt:
        while_tok = self._advance() # 'khi'
        has_paren = self._match(TokenType.LPAREN)
        cond = self._normalize_condition(self._parse_expression())
        if has_paren:
            self._consume(TokenType.RPAREN, "Cần ')' sau điều kiện 'khi'")
        self._skip_newlines()
        body = self._parse_block() if self._check(TokenType.LBRACE) else self._parse_statement()
        return WhileStmt(condition=cond, body=body, line=while_tok.line, column=while_tok.column)

    def _parse_for_in_stmt(self) -> ForInStmt:
        for_tok = self._advance() # 'lap'
        has_paren = self._match(TokenType.LPAREN)
        
        # Case 1: `lap 5 lan { ... }`
        if self._check(TokenType.INT) or (self._check(TokenType.IDENTIFIER) and self._peek(1).type == TokenType.LAN):
            count_expr = self._parse_expression()
            self._consume(TokenType.LAN, "Cần từ khóa 'lần' sau số lần lặp")
            var_name = "_i"
            iterable = CallExpr(callee=Identifier(name="pham_vi", line=for_tok.line, column=for_tok.column), args=[count_expr], line=for_tok.line, column=for_tok.column)
        else:
            var_tok = self._consume(TokenType.IDENTIFIER, "Cần tên biến chạy hoặc số lần lặp sau 'lặp'")
            var_name = str(var_tok.value)
            
            # Case 2: `lap i tu 1 den 10 { ... }`
            if self._match(TokenType.TU):
                start_expr = self._parse_expression()
                self._consume(TokenType.DEN, "Cần từ khóa 'đến' sau điểm bắt đầu lặp")
                end_expr = self._parse_expression()
                end_plus_1 = BinaryOp(left=end_expr, op="+", right=NumberLiteral(value=1, line=for_tok.line, column=for_tok.column), line=for_tok.line, column=for_tok.column)
                iterable = CallExpr(callee=Identifier(name="pham_vi", line=for_tok.line, column=for_tok.column), args=[start_expr, end_plus_1], line=for_tok.line, column=for_tok.column)
            else:
                # Case 3: `lap i trong ...`
                self._consume(TokenType.TRONG, "Cần từ khóa 'trong' hoặc 'từ' sau tên biến lặp")
                iterable = self._parse_expression()
        
        if has_paren:
            self._consume(TokenType.RPAREN, "Cần ')' đóng vòng lặp 'lặp'")
            
        self._skip_newlines()
        body = self._parse_block() if self._check(TokenType.LBRACE) else self._parse_statement()
        return ForInStmt(var_name=var_name, iterable=iterable, body=body, line=for_tok.line, column=for_tok.column)

    def _parse_break_stmt(self) -> BreakStmt:
        tok = self._advance()
        self._match(TokenType.SEMICOLON)
        return BreakStmt(line=tok.line, column=tok.column)

    def _parse_continue_stmt(self) -> ContinueStmt:
        tok = self._advance()
        self._match(TokenType.SEMICOLON)
        return ContinueStmt(line=tok.line, column=tok.column)

    def _parse_return_stmt(self) -> ReturnStmt:
        tok = self._advance() # 'tra_ve'
        val = None
        if not self._check(TokenType.SEMICOLON) and not self._check(TokenType.NEWLINE) and not self._check(TokenType.RBRACE) and not self._is_at_end():
            val = self._parse_expression()
        self._match(TokenType.SEMICOLON)
        return ReturnStmt(value=val, line=tok.line, column=tok.column)

    def _parse_function_decl(self) -> FunctionDecl:
        fn_tok = self._advance() # 'ham'
        if self._check(TokenType.KHOI_TAO):
            name_tok = self._advance()
            name = "khoi_tao"
        else:
            name_tok = self._consume(TokenType.IDENTIFIER, "Can ten ham sau tu khoa 'ham'")
            name = str(name_tok.value)

        self._consume(TokenType.LPAREN, "Can '(' sau ten ham")
        params = []
        if not self._check(TokenType.RPAREN):
            while True:
                p_tok = self._consume(TokenType.IDENTIFIER, "Can ten tham so")
                params.append(str(p_tok.value))
                if not self._match(TokenType.COMMA):
                    break
        self._consume(TokenType.RPAREN, "Can ')' sau danh sach tham so")

        self._skip_newlines()
        body = self._parse_block()
        return FunctionDecl(name=name, params=params, body=body, line=fn_tok.line, column=fn_tok.column)

    def _parse_class_decl(self) -> ClassDecl:
        cls_tok = self._advance() # 'lop'
        name_tok = self._consume(TokenType.IDENTIFIER, "Can ten lop sau tu khoa 'lop'")
        name = str(name_tok.value)

        parent_name = None
        if self._match(TokenType.KE_THUA):
            p_tok = self._consume(TokenType.IDENTIFIER, "Can ten lop cha sau tu khoa 'ke_thua'")
            parent_name = str(p_tok.value)

        self._skip_newlines()
        self._consume(TokenType.LBRACE, "Can '{' bat dau than lop")

        methods = []
        self._skip_newlines()
        while not self._check(TokenType.RBRACE) and not self._is_at_end():
            self._skip_newlines()
            if self._check(TokenType.KHOI_TAO):
                # Constructor method
                init_tok = self._advance()
                self._consume(TokenType.LPAREN, "Can '(' sau 'khoi_tao'")
                params = []
                if not self._check(TokenType.RPAREN):
                    while True:
                        p_tok = self._consume(TokenType.IDENTIFIER, "Can ten tham so")
                        params.append(str(p_tok.value))
                        if not self._match(TokenType.COMMA):
                            break
                self._consume(TokenType.RPAREN, "Can ')' sau danh sach tham so")
                self._skip_newlines()
                body = self._parse_block()
                methods.append(FunctionDecl(name="khoi_tao", params=params, body=body, line=init_tok.line, column=init_tok.column))
            elif self._check(TokenType.HAM):
                methods.append(self._parse_function_decl())
            else:
                tok = self._peek()
                raise ParserError(f"Phan tu khong hop le trong lop: '{tok.value}'. Chi cho phep khai bao 'ham' hoac 'khoi_tao'", tok)
            self._skip_newlines()

        self._consume(TokenType.RBRACE, "Can '}' ket thuc lop")
        return ClassDecl(name=name, parent_name=parent_name, methods=methods, line=cls_tok.line, column=cls_tok.column)

    def _parse_try_catch_stmt(self) -> TryCatchStmt:
        try_tok = self._advance() # 'thu'
        self._skip_newlines()
        try_block = self._parse_block()

        error_var = None
        catch_block = None
        finally_block = None

        self._skip_newlines()
        if self._match(TokenType.BAT_LOI):
            if self._match(TokenType.LPAREN):
                e_tok = self._consume(TokenType.IDENTIFIER, "Can ten bien luu loi")
                error_var = str(e_tok.value)
                self._consume(TokenType.RPAREN, "Can ')' sau ten bien loi")
            self._skip_newlines()
            catch_block = self._parse_block()

        self._skip_newlines()
        if self._match(TokenType.CUOI_CUNG):
            self._skip_newlines()
            finally_block = self._parse_block()

        if catch_block is None and finally_block is None:
            raise ParserError("Khoi 'thu' bat buoc phai co it nhat 'bat_loi' hoac 'cuoi_cung'", try_tok)

        return TryCatchStmt(
            try_block=try_block,
            error_var=error_var,
            catch_block=catch_block,
            finally_block=finally_block,
            line=try_tok.line,
            column=try_tok.column
        )

    def _parse_throw_stmt(self) -> ThrowStmt:
        tok = self._advance() # 'nem_loi'
        expr = self._parse_expression()
        self._match(TokenType.SEMICOLON)
        return ThrowStmt(expr=expr, line=tok.line, column=tok.column)

    def _parse_import_stmt(self) -> ImportStmt:
        tok = self._advance() # 'dung_thu_vien' / 'tai'
        path_tok = self._consume(TokenType.STRING, "Can duong dan tep chuoi sau 'dung_thu_vien'")
        path = str(path_tok.value)
        alias = None
        if self._match(TokenType.IDENTIFIER): # e.g. nhu / as
            a_tok = self._consume(TokenType.IDENTIFIER, "Can ten dinh danh alias")
            alias = str(a_tok.value)
        self._match(TokenType.SEMICOLON)
        return ImportStmt(module_path=path, alias=alias, line=tok.line, column=tok.column)

    def _parse_expr_stmt(self) -> ExprStmt:
        tok = self._peek()
        expr = self._parse_expression()
        self._match(TokenType.SEMICOLON)
        return ExprStmt(expr=expr, line=tok.line, column=tok.column)

    # --- Expression Parsers ---

    def _parse_expression(self) -> ASTNode:
        return self._parse_assignment()

    def _parse_assignment(self) -> ASTNode:
        expr = self._parse_logical_or()

        if self._check(TokenType.ASSIGN) or \
           self._check(TokenType.PLUS_ASSIGN) or \
           self._check(TokenType.MINUS_ASSIGN) or \
           self._check(TokenType.STAR_ASSIGN) or \
           self._check(TokenType.SLASH_ASSIGN) or \
           self._check(TokenType.PERCENT_ASSIGN):
            op_tok = self._advance()
            val = self._parse_assignment()

            if isinstance(expr, (Identifier, IndexExpr, MemberExpr)):
                return Assign(target=expr, op=str(op_tok.value), value=val, line=op_tok.line, column=op_tok.column)
            if op_tok.type == TokenType.ASSIGN:
                return BinaryOp(left=expr, op="==", right=val, line=op_tok.line, column=op_tok.column)
            raise ParserError("Đích đến của phép gán phải là một biến, phần tử mảng hoặc thuộc tính", op_tok)

        return expr

    def _parse_logical_or(self) -> ASTNode:
        expr = self._parse_logical_and()
        while self._check(TokenType.OR) or self._check(TokenType.HOAC):
            op_tok = self._advance()
            right = self._parse_logical_and()
            expr = BinaryOp(left=expr, op="hoac", right=right, line=op_tok.line, column=op_tok.column)
        return expr

    def _parse_logical_and(self) -> ASTNode:
        expr = self._parse_equality()
        while self._check(TokenType.AND) or self._check(TokenType.VA):
            op_tok = self._advance()
            right = self._parse_equality()
            expr = BinaryOp(left=expr, op="va", right=right, line=op_tok.line, column=op_tok.column)
        return expr

    def _parse_equality(self) -> ASTNode:
        expr = self._parse_comparison()
        while self._check(TokenType.EQ) or self._check(TokenType.NOT_EQ):
            op_tok = self._advance()
            right = self._parse_comparison()
            expr = BinaryOp(left=expr, op=str(op_tok.value), right=right, line=op_tok.line, column=op_tok.column)
        return expr

    def _parse_comparison(self) -> ASTNode:
        expr = self._parse_addition()
        while self._check(TokenType.LT) or self._check(TokenType.LTE) or \
              self._check(TokenType.GT) or self._check(TokenType.GTE):
            op_tok = self._advance()
            right = self._parse_addition()
            expr = BinaryOp(left=expr, op=str(op_tok.value), right=right, line=op_tok.line, column=op_tok.column)
        return expr

    def _parse_addition(self) -> ASTNode:
        expr = self._parse_multiplication()
        while self._check(TokenType.PLUS) or self._check(TokenType.MINUS):
            op_tok = self._advance()
            right = self._parse_multiplication()
            expr = BinaryOp(left=expr, op=str(op_tok.value), right=right, line=op_tok.line, column=op_tok.column)
        return expr

    def _parse_multiplication(self) -> ASTNode:
        expr = self._parse_power()
        while self._check(TokenType.STAR) or self._check(TokenType.SLASH) or self._check(TokenType.PERCENT):
            op_tok = self._advance()
            right = self._parse_power()
            expr = BinaryOp(left=expr, op=str(op_tok.value), right=right, line=op_tok.line, column=op_tok.column)
        return expr

    def _parse_power(self) -> ASTNode:
        expr = self._parse_unary()
        while self._check(TokenType.POWER):
            op_tok = self._advance()
            right = self._parse_unary() # right-associative power can be parsed
            expr = BinaryOp(left=expr, op="^", right=right, line=op_tok.line, column=op_tok.column)
        return expr

    def _parse_unary(self) -> ASTNode:
        if self._check(TokenType.NOT) or self._check(TokenType.PHU_DINH) or \
           self._check(TokenType.MINUS) or self._check(TokenType.PLUS) or \
           self._check(TokenType.PLUS_PLUS) or self._check(TokenType.MINUS_MINUS):
            op_tok = self._advance()
            operand = self._parse_unary()
            op_name = "!" if op_tok.type in (TokenType.NOT, TokenType.PHU_DINH) else str(op_tok.value)
            return UnaryOp(op=op_name, operand=operand, is_postfix=False, line=op_tok.line, column=op_tok.column)
        return self._parse_call_and_member()

    def _parse_call_and_member(self) -> ASTNode:
        expr = self._parse_primary()

        while True:
            if self._match(TokenType.LPAREN):
                # Function call
                args = []
                if not self._check(TokenType.RPAREN):
                    while True:
                        self._skip_newlines()
                        args.append(self._parse_expression())
                        self._skip_newlines()
                        if not self._match(TokenType.COMMA):
                            break
                rparen = self._consume(TokenType.RPAREN, "Can ')' sau danh sach doi so")
                expr = CallExpr(callee=expr, args=args, line=rparen.line, column=rparen.column)
            elif self._match(TokenType.LBRACKET):
                # Indexing or slicing: arr[i] or arr[start:end]
                self._skip_newlines()
                is_slice = False
                end_index = None
                index = None
                
                if self._match(TokenType.COLON):
                    # [:end]
                    is_slice = True
                    if not self._check(TokenType.RBRACKET):
                        end_index = self._parse_expression()
                else:
                    index = self._parse_expression()
                    if self._match(TokenType.COLON):
                        is_slice = True
                        if not self._check(TokenType.RBRACKET):
                            end_index = self._parse_expression()
                            
                self._skip_newlines()
                rbrack = self._consume(TokenType.RBRACKET, "Can ']' de dong chi muc")
                expr = IndexExpr(target=expr, index=index, end_index=end_index, is_slice=is_slice, line=rbrack.line, column=rbrack.column)
            elif self._match(TokenType.DOT):
                # Member access: obj.prop (allows identifiers and keywords as property/method names)
                tok = self._peek()
                if tok.type in (TokenType.EOF, TokenType.NEWLINE, TokenType.SEMICOLON, TokenType.RPAREN, TokenType.RBRACKET, TokenType.RBRACE):
                    raise SyntaxError(f"Cần tên thuộc tính sau '.' tại dòng {tok.line}")
                if tok.value is True:
                    m_name = "dung"
                elif tok.value is False:
                    m_name = "sai"
                elif tok.type == TokenType.RONG:
                    m_name = "rong"
                else:
                    m_name = str(tok.value)
                self._advance()
                expr = MemberExpr(target=expr, member=m_name, line=tok.line, column=tok.column)
            elif self._match(TokenType.PLUS_PLUS):
                # Postfix ++
                expr = UnaryOp(op="++", operand=expr, is_postfix=True, line=self._peek().line, column=self._peek().column)
            elif self._match(TokenType.MINUS_MINUS):
                # Postfix --
                expr = UnaryOp(op="--", operand=expr, is_postfix=True, line=self._peek().line, column=self._peek().column)
            else:
                break

        return expr

    def _parse_primary(self) -> ASTNode:
        tok = self._peek()

        if tok.type == TokenType.INT:
            self._advance()
            return NumberLiteral(value=tok.value, line=tok.line, column=tok.column)
        elif tok.type == TokenType.FLOAT:
            self._advance()
            return NumberLiteral(value=tok.value, line=tok.line, column=tok.column)
        elif tok.type == TokenType.STRING:
            self._advance()
            return StringLiteral(value=tok.value, line=tok.line, column=tok.column)
        elif tok.type == TokenType.DUNG:
            self._advance()
            return BooleanLiteral(value=True, line=tok.line, column=tok.column)
        elif tok.type == TokenType.SAI:
            self._advance()
            return BooleanLiteral(value=False, line=tok.line, column=tok.column)
        elif tok.type == TokenType.RONG:
            self._advance()
            return NullLiteral(line=tok.line, column=tok.column)
        elif tok.type == TokenType.BAN_THAN:
            self._advance()
            return SelfExpr(line=tok.line, column=tok.column)
        elif tok.type == TokenType.IDENTIFIER:
            self._advance()
            return Identifier(name=str(tok.value), line=tok.line, column=tok.column)
        elif tok.type == TokenType.HAM:
            # Anonymous function: ham(x, y) { tra_ve x + y }
            fn_tok = self._advance()
            self._consume(TokenType.LPAREN, "Can '(' sau tu khoa 'ham'")
            params = []
            if not self._check(TokenType.RPAREN):
                while True:
                    p_tok = self._consume(TokenType.IDENTIFIER, "Can ten tham so")
                    params.append(str(p_tok.value))
                    if not self._match(TokenType.COMMA):
                        break
            self._consume(TokenType.RPAREN, "Can ')' sau tham so ham an danh")
            self._skip_newlines()
            body = self._parse_block()
            return AnonymousFunction(params=params, body=body, line=fn_tok.line, column=fn_tok.column)
        elif tok.type == TokenType.LPAREN:
            self._advance()
            self._skip_newlines()
            expr = self._parse_expression()
            self._skip_newlines()
            self._consume(TokenType.RPAREN, "Can ')' de dong bieu thuc")
            return expr
        elif tok.type == TokenType.LBRACKET:
            # List literal: [1, 2, 3]
            self._advance()
            elements = []
            self._skip_newlines()
            if not self._check(TokenType.RBRACKET):
                while True:
                    self._skip_newlines()
                    elements.append(self._parse_expression())
                    self._skip_newlines()
                    if not self._match(TokenType.COMMA):
                        break
            self._skip_newlines()
            rbrack = self._consume(TokenType.RBRACKET, "Can ']' de dong danh sach")
            return ListLiteral(elements=elements, line=tok.line, column=tok.column)
        elif tok.type == TokenType.LBRACE:
            # Dict literal: { "a": 1, "b": 2 } or empty { }
            self._advance()
            pairs = []
            self._skip_newlines()
            if not self._check(TokenType.RBRACE):
                while True:
                    self._skip_newlines()
                    # Key can be string or identifier or expression
                    key = self._parse_expression()
                    self._consume(TokenType.COLON, "Can ':' giua khoa va gia tri trong tu dien")
                    val = self._parse_expression()
                    pairs.append((key, val))
                    self._skip_newlines()
                    if not self._match(TokenType.COMMA):
                        break
            self._skip_newlines()
            self._consume(TokenType.RBRACE, "Can '}' de dong tu dien")
            return DictLiteral(pairs=pairs, line=tok.line, column=tok.column)
        else:
            raise ParserError(f"Bieu thuc khong hop le: '{tok.value}' (TokenType: {tok.type.name})", tok)
