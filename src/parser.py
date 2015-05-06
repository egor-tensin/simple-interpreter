# Copyright 2015 Egor Tensin <Egor.Tensin@gmail.com>
# This file is licensed under the terms of the MIT License.
# See LICENSE.txt for details.

from lexer import *
from nodes import *

class ParserError(RuntimeError):
    pass

class Parser:
    def __init__(self, src_file):
        self._lexer = Lexer(src_file)

    def parse(self):
        return self._parse_program()

    def _try_parse_token(self, cls):
        if not self._lexer.has_next_token():
            return False
        t = self._lexer.preview_next_token()
        if not isinstance(t, cls):
            return False
        self._lexer.drop_next_token()
        return t

    def _parse_token(self, cls):
        if not self._lexer.has_next_token():
            raise ParserError("%s expected" % cls.__name__)
        t = self._lexer.preview_next_token()
        if not isinstance(t, cls):
            raise ParserError("%s expected instead of %s" % (
                    cls.__name__, t.__class__.__name__))
        self._lexer.drop_next_token()
        return t

    def _parse_program(self):
        stmt_list = []
        while self._lexer.has_next_token():
            stmt = self._try_parse_stmt()
            if not stmt:
                raise ParserError("unexpected token '%s'" % (
                        self._lexer.preview_next_token()))
            stmt_list.append(stmt)
        return ProgramNode(stmt_list)

    def _try_parse_stmt(self):
        print_stmt = self._try_parse_print_stmt()
        if print_stmt:
            return print_stmt
        assignment = self._try_parse_assignment()
        if assignment:
            return assignment
        empty_stmt = self._try_parse_empty_stmt()
        if empty_stmt:
            return empty_stmt
        if_stmt = self._try_parse_if_stmt()
        if if_stmt:
            return if_stmt
        block = self._try_parse_block()
        if block:
            return block
        return False

    def _try_parse_empty_stmt(self):
        if not self._try_parse_token(SemicolonToken):
            return False
        return EmptyStatementNode()

    def _try_parse_block(self):
        if not self._try_parse_token(OpeningBraceToken):
            return False
        stmt_list = []
        while True:
            stmt = self._try_parse_stmt()
            if stmt:
                stmt_list.append(stmt)
            else:
                break
        self._parse_token(ClosingBraceToken)
        return CompoundStatementNode(stmt_list)

    def _try_parse_if_stmt(self):
        if not self._try_parse_token(IfToken):
            return False
        self._parse_token(OpeningParenToken)
        cond = self._parse_logical_expr()
        self._parse_token(ClosingParenToken)
        stmt = self._try_parse_stmt()
        if not stmt:
            raise ParserError("unexpected token '%s'" % (
                    self._lexer.preview_next_token()))
        return IfStatementNode(cond, stmt)

    def _try_parse_print_stmt(self):
        if not self._try_parse_token(PrintToken):
            return False
        arithm_expr = self._parse_arithm_expr()
        self._parse_token(SemicolonToken)
        return PrintStatementNode(arithm_expr)

    def _try_parse_assignment(self):
        if not self._lexer.has_next_token(2):
            return False
        identifier = self._lexer.preview_next_token(0)
        if not isinstance(identifier, IdentifierToken):
            return False
        op = self._lexer.preview_next_token(1)
        if not isinstance(op, AssignmentOpToken):
            return False
        self._lexer.drop_next_token(2)
        arithm_expr = self._parse_arithm_expr()
        self._parse_token(SemicolonToken)
        return AssignmentNode(identifier, arithm_expr)

    def _parse_logical_expr(self):
        left = self._parse_logical_term()
        while self._lexer.has_next_token():
            if self._try_parse_token(AndOpToken):
                left = AndOpNode(left, self._parse_logical_term())
            elif self._try_parse_token(OrOpToken):
                left = OrOpNode(left, self._parse_logical_term())
            else:
                return left
        return left

    def _parse_logical_term(self):
        left = self._parse_logical_factor()
        if self._lexer.has_next_token():
            if self._try_parse_token(EqualsOpToken):
                left = EqualsOpNode(left, self._parse_logical_factor())
            elif self._try_parse_token(NotEqualsOpToken):
                left = NotEqualsOpNode(left, self._parse_logical_factor())
            else:
                return left
        return left

    def _parse_logical_factor(self):
        if self._try_parse_token(TrueToken):
            return TrueNode()
        elif self._try_parse_token(FalseToken):
            return FalseNode()
        elif self._try_parse_token(OpeningParenToken):
            logical_expr = self._parse_logical_expr()
            self._parse_token(ClosingParenToken)
            return logical_expr
        else:
            raise ParserError('expected \'True\', \'False\' or \'(\'')

    def _parse_arithm_expr(self):
        left = self._parse_arithm_term()
        while self._lexer.has_next_token():
            if self._try_parse_token(AdditionOpToken):
                left = AdditionOpNode(left, self._parse_arithm_term())
            elif self._try_parse_token(SubtractionOpToken):
                left = SubtractionOpNode(left, self._parse_arithm_term())
            else:
                return left
        return left

    def _parse_arithm_term(self):
        left = self._parse_arithm_factor()
        while self._lexer.has_next_token():
            if self._try_parse_token(MultiplicationOpToken):
                left = MultiplicationOpNode(left, self._parse_arithm_factor())
            elif self._try_parse_token(DivisionOpToken):
                left = DivisionOpNode(left, self._parse_arithm_factor())
            else:
                return left
        return left
        
    def _parse_arithm_factor(self):
        identifier = self._try_parse_token(IdentifierToken)
        if identifier:
            return IdentifierNode(identifier)
        int_num = self._try_parse_token(IntegerNumberToken)
        if int_num:
            return IntegerNumberNode(int_num)
        float_num = self._try_parse_token(FloatingPointNumberToken)
        if float_num:
            return FloatingPointNumberNode(float_num)
        if self._try_parse_token(OpeningParenToken):
            arithm_expr = self._parse_arithm_expr()
            self._parse_token(ClosingParenToken)
            return arithm_expr
        else:
            raise ParserError('expected an identifier, a number or \'(\'')

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('src_path', help='set source file path')
    args = parser.parse_args()
    with open(args.src_path, 'r') as src_file:
        parser = Parser(src_file)
        parser.parse().execute()
