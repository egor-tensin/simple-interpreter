# Copyright (c) 2015 Egor Tensin <Egor.Tensin@gmail.com>
# This file is part of the "Simple interpreter" project.
# For details, see https://github.com/egor-tensin/simple-interpreter.
# Distributed under the MIT License.

class Token:
    pass

class AdditionOpToken(Token):
    def __str__(self):
        return '+'

class SubtractionOpToken(Token):
    def __str__(self):
        return '-'

class MultiplicationOpToken(Token):
    def __str__(self):
        return '*'

class DivisionOpToken(Token):
    def __str__(self):
        return '/'

class AssignmentOpToken(Token):
    def __str__(self):
        return ':='

class SemicolonToken(Token):
    def __str__(self):
        return ';'

class PrintToken(Token):
    def __str__(self):
        return 'print'

class OpeningParenToken(Token):
    def __str__(self):
        return '('

class ClosingParenToken(Token):
    def __str__(self):
        return ')'

class OpeningBraceToken(Token):
    def __str__(self):
        return '{'

class ClosingBraceToken(Token):
    def __str__(self):
        return '}'

class IdentifierToken(Token):
    def __init__(self, i):
        self._i = i

    def __str__(self):
        return str(self._i)

class FloatingPointNumberToken(Token):
    def __init__(self, n):
        self._n = n

    def __float__(self):
        return float(self._n)

    def __str__(self):
        return str(self._n)

class IntegerNumberToken(Token):
    def __init__(self, n):
        self._n = n

    def __int__(self):
        return int(self._n)

    def __str__(self):
        return str(self._n)

class TrueToken(Token):
    def __str__(self):
        return 'True'

class FalseToken(Token):
    def __str__(self):
        return 'False'

class AndOpToken(Token):
    def __str__(self):
        return '&&'

class OrOpToken(Token):
    def __str__(self):
        return '||'

class IfToken(Token):
    def __str__(self):
        return 'if'

class EqualsOpToken(Token):
    def __str__(self):
        return '=='

class NotEqualsOpToken(Token):
    def __str__(self):
        return '!='
