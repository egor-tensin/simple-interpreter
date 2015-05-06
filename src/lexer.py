# Copyright 2015 Egor Tensin <Egor.Tensin@gmail.com>
# This file is licensed under the terms of the MIT License.
# See LICENSE.txt for details.

import re

from tokens import *

class LexerError(RuntimeError):
    pass 

class Lexer:
    def __init__(self, src_file):
        self._line_buf = ''
        self._tok_buf = []
        self._src_file = src_file
        self._ws_re = re.compile(r'^\s+')
        self._identifier_re = re.compile(r'^[^\W\d]\w*')
        self._const_toks = {
            '+': AdditionOpToken,
            '-': SubtractionOpToken,
            '*': MultiplicationOpToken,
            '/': DivisionOpToken,
            ':=': AssignmentOpToken,
            ';': SemicolonToken,
            '(': OpeningParenToken,
            ')': ClosingParenToken,
            '{': OpeningBraceToken,
            '}': ClosingBraceToken,
            '&&': AndOpToken,
            '||': OrOpToken,
            '==': EqualsOpToken,
            '!=': NotEqualsOpToken,
        }
        self._const_toks_sorted = list(self._const_toks.keys())
        self._const_toks_sorted.sort()
        self._make_sure_const_tokens_dont_match_identifier_re()
        self._keywords = {
            'if': IfToken,
            'print': PrintToken,
            'True': TrueToken,
            'False': FalseToken,
        }
        self._make_sure_keywords_match_identifier_re()

    def _make_sure_keywords_match_identifier_re(self):
        for kw in self._keywords:
            if not re.match(self._identifier_re, kw):
                raise LexerError("keyword '%s' is not an identifier" % (kw))

    def _make_sure_const_tokens_dont_match_identifier_re(self):
        for t in self._const_toks_sorted:
            if re.match(self._identifier_re, t):
                raise LexerError("const token '%s' is an identifier" % (t))

    def _try_require_line_buf(self):
        if self._line_buf:
            return True
        if self._src_file is None:
            return False
        self._line_buf = self._src_file.readline()
        if not self._line_buf:
            self._src_file = None
            return False
        return True

    def _eat_number_after_e_sign(self, acc):
        m_after_e_sign = re.match(r'^[\-+]?\d+', self._line_buf)
        if m_after_e_sign:
            after_e_sign = m_after_e_sign.group(0)
            self._line_buf = self._line_buf[len(after_e_sign):]
            return FloatingPointNumberToken('%s%s' % (acc, after_e_sign))
        raise LexerError("'%c' unexpected" % (self._line_buf[0]))

    def _eat_number_after_dec_mark(self, acc):
        if not self._line_buf:
            return FloatingPointNumberToken(acc)
        m_digits = re.match(r'^\d+', self._line_buf)
        if m_digits:
            digits = m_digits.group(0)
            self._line_buf = self._line_buf[len(digits):]
            return self._eat_number_after_dec_mark('%s%s' % (acc, digits))
        m_e_sign = re.match(r'^[eE]', self._line_buf)
        if m_e_sign:
            e_sign = m_e_sign.group(0)
            self._line_buf = self._line_buf[len(e_sign):]
            return self._eat_number_after_e_sign('%s%s' % (acc, e_sign))
        return FloatingPointNumberToken(acc)

    def _eat_number_after_first_digit(self, acc):
        if not self._line_buf:
            return IntegerNumberToken(acc)
        m_digits = re.match(r'^\d+', self._line_buf)
        if m_digits:
            digits = m_digits.group(0)
            self._line_buf = self._line_buf[len(digits):]
            return self._eat_number_after_first_digit('%s%s' % (acc, digits))
        m_e_sign = re.match(r'^[eE]', self._line_buf)
        if m_e_sign:
            e_sign = m_e_sign.group(0)
            self._line_buf = self._line_buf[len(e_sign):]
            return self._eat_number_after_e_sign('%s%s' % (acc, e_sign))
        m_dec_mark = re.match(r'^\.', self._line_buf)
        if m_dec_mark:
            dec_mark = m_dec_mark.group(0)
            self._line_buf = self._line_buf[len(dec_mark):]
            return self._eat_number_after_dec_mark('%s%s' % (acc, dec_mark))
        return IntegerNumberToken(acc)

    def _try_eat_number(self):
        m_first_digit = re.match(r'^\d', self._line_buf)
        if m_first_digit:
            first_digit = m_first_digit.group(0)
            self._line_buf = self._line_buf[len(first_digit):]
            return self._eat_number_after_first_digit(first_digit)
        m_dec_mark = re.match(r'^\.\d', self._line_buf)
        if m_dec_mark:
            dec_mark = m_dec_mark.group(0)
            self._line_buf = self._line_buf[len(dec_mark):]
            return self._eat_number_after_dec_mark(dec_mark)
        return False

    def _try_eat_ws(self):
        while True:
            if not self._try_require_line_buf():
                return False
            m_ws = re.match(self._ws_re, self._line_buf)
            if not m_ws:
                return True
            self._line_buf = self._line_buf[len(m_ws.group(0)):]
        return True

    def _try_eat_identifier_or_keyword(self):
        m_identifier = re.match(self._identifier_re, self._line_buf)
        if m_identifier:
            identifier = m_identifier.group(0)
            self._line_buf = self._line_buf[len(identifier):]
            if identifier in self._keywords:
                return self._keywords[identifier]()
            else:
                return IdentifierToken(identifier)
        return False

    def _try_eat_const_token(self):
        for t in self._const_toks_sorted:
            if self._line_buf.startswith(t):
                self._line_buf = self._line_buf[len(t):]
                return self._const_toks[t]()
        return False

    def _try_eat_token(self):
        if not self._try_eat_ws():
            return False
        const_tok = self._try_eat_const_token()
        if const_tok:
            self._tok_buf.append(const_tok)
            return const_tok
        identifier_or_keyword = self._try_eat_identifier_or_keyword()
        if identifier_or_keyword:
            self._tok_buf.append(identifier_or_keyword)
            return identifier_or_keyword
        number = self._try_eat_number()
        if number:
            self._tok_buf.append(number)
            return number
        raise LexerError("'%c' unexpected" % (self._line_buf[0]))

    def _try_require_tok_buf(self, n = 1):
        if n < 1:
            raise LexerError("unable to require %d tokens" % (n))
        while len(self._tok_buf) < n:
            if not self._try_eat_token():
                return False
        return True

    def has_next_token(self, n = 1):
        return self._try_require_tok_buf(n)

    def preview_next_token(self, n = 0):
        if not self.has_next_token(n + 1):
            raise LexerError("not enough tokens")
        return self._tok_buf[n]

    def drop_next_token(self, n = 1):
        if not self.has_next_token(n):
            raise LexerError("not enough tokens")
        if n == 1:
            return self._tok_buf.pop(0)
        else:
            xs = self._tok_buf[:n]
            self._tok_buf = self._tok_buf[n:]
            return xs

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('src_path', help='set soure file path')
    args = parser.parse_args()
    with open(args.src_path, 'r') as src_file:
        lexer = Lexer(src_file)
        while lexer.has_next_token():
            print(lexer.drop_next_token().__class__.__name__)
