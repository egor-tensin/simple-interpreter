# Copyright (c) 2015 Egor Tensin <Egor.Tensin@gmail.com>
# This file is part of the "Simple interpreter" project.
# For details, see https://github.com/egor-tensin/simple-interpreter.
# Distributed under the MIT License.

class ProgramNode:
    def __init__(self, stmt_list):
        self._stmt_list = stmt_list

    def execute(self):
        for stmt in self._stmt_list:
            stmt.execute()

_varmap = { }

class CompoundStatementNode:
    def __init__(self, stmt_list):
        self._stmt_list = stmt_list

    def execute(self):
        for stmt in self._stmt_list:
            stmt.execute()

class EmptyStatementNode:
    def execute(self):
        pass

class AssignmentNode:
    def __init__(self, identifier, arithm_expr):
        self._identifier = identifier
        self._arithm_expr = arithm_expr

    def execute(self):
        _varmap[str(self._identifier)] = self._arithm_expr.execute()
        return None

class PrintStatementNode:
    def __init__(self, arithm_expr):
        self._arithm_expr = arithm_expr

    def execute(self):
        print(self._arithm_expr.execute())
        return None

class IdentifierNode:
    def __init__(self, identifier):
        self._identifier = identifier

    def execute(self):
        return _varmap[str(self._identifier)]

class AdditionOpNode:
    def __init__(self, left, right):
        self._left = left
        self._right = right

    def execute(self):
        return self._left.execute() + self._right.execute()

class SubtractionOpNode:
    def __init__(self, left, right):
        self._left = left
        self._right = right

    def execute(self):
        return self._left.execute() + self._right.execute()

class MultiplicationOpNode:
    def __init__(self, left, right):
        self._left = left
        self._right = right

    def execute(self):
        return self._left.execute() * self._right.execute()

class DivisionOpNode:
    def __init__(self, left, right):
        self._left = left
        self._right = right

    def execute(self):
        return self._left.execute() / self._right.execute()

class IntegerNumberNode:
    def __init__(self, n):
        self._n = n

    def execute(self):
        return int(self._n)

class FloatingPointNumberNode:
    def __init__(self, n):
        self._n = n

    def execute(self):
        return float(self._n)

class IfStatementNode:
    def __init__(self, cond, body):
        self._cond = cond
        self._body = body

    def execute(self):
        if self._cond.execute():
            return self._body.execute()

class TrueNode:
    def execute(self):
        return True

class FalseNode:
    def execute(self):
        return False

class AndOpNode:
    def __init__(self, left, right):
        self._left = left
        self._right = right

    def execute(self):
        return self._left.execute() and self._right.execute()

class OrOpNode:
    def __init__(self, left, right):
        self._left = left
        self._right = right

    def execute(self):
        return self._left.execute() or self._right.execute()

class EqualsOpNode:
    def __init__(self, left, right):
        self._left = left
        self._right = right

    def execute(self):
        return self._left.execute() == self._right.execute()

class NotEqualsOpNode:
    def __init__(self, left, right):
        self._left = left
        self._right = right

    def execute(self):
        return self._left.execute() != self._right.execute()
