from fileinput import filename
from lib2to3.pgen2 import token
import re
from general.datatypes import FileOrigin
from general.include_handler import IncludeHandler



class Token:
    def __init__(self,
                 filename: str,
                 text: str,
                 position: tuple[int, int],
                 token_type: str = 'UND') -> None:
        self.filename: str   = filename
        self.text:     str   = text
        self.type:     str   = token_type
        self.position: tuple = position

    @property
    def is_whitespace(self) -> bool:
        return self.text[0] in [' ', '\n', '\t']
    def __repr__(self) -> str:
        return f'<Token {repr(self.text)} {self.type} at {self.position[0]}:{self.position[1]}>'


class Position:
    def __init__(self, line: int = 1, column: int = 1):
        self.line:          int = line
        self.column:        int = column
        self.marked_line:   int = line
        self.marked_column: int = column
        self._base_column:  int = column

    def increment_line(self):
        self.column = self._base_column
        self.line += 1
    def increment_column(self):
        self.column += 1

    def mark_current(self):
        self.marked_line = self.line
        self.marked_column = self.column
    
    def get_current(self):
        return (self.line, self.column)
    def get_marked(self):
        return (self.marked_line, self.marked_column)
    def get_and_mark(self):
        _ = (self.marked_line, self.marked_column)
        self.mark_current()
        return _


class BaseTokenizer:
    DERECTIVES = {}
    IS_FLOAT_RE = re.compile('^([+-]?[0-9]*\.[0-9]*)$')
    IS_INT_RE = re.compile('^([+-]?[0-9]*\.?0?)$')
    IS_STRING_RE = re.compile(r"""([bruf]*)(\"""|'''|"|')(?:(?!\2)(?:\\.|[^\\]))*\2""")
    IS_KEYWORD_RE = re.compile(r'^[a-zA-Z_][0-9a-zA-Z_]*$')
    IS_COMMENT_RE = re.compile(r'^(\/\*(.*)\*\/)$', re.S)
    filename = None

    def build_token(self, string: str, position: tuple) -> 'Token':
        if self.is_comment(string):
            return Token(self.filename, string, position, token_type='COMMENT')
        
        if self.is_keyword(string):
            finded, token = self.build_reserved_token(string, position)
            if finded:
                return token
            return Token(self.filename, string, position, token_type='ID')

        if self.is_string(string):
            return Token(self.filename, string, position, token_type='STR_CONST')
        
        if self.is_int(string):
            return Token(self.filename, int(string), position, token_type='INT_CONST')

        if self.is_float(string):
            return Token(self.filename, float(string), position, token_type='FLT_CONST')


    def build_specific_token(self, string: str, position: tuple, token_type: str) -> 'Token':
        return Token(self.filename, string, position, token_type=token_type)

    def build_reserved_token(self, string: str, position: tuple) -> 'Token':
        for category in self.DERECTIVES:
            if string in self.DERECTIVES[category]:
                return True, Token(self.filename, string, position, token_type=category)
        return False, None

    def is_keyword(self, string: str) -> bool:
        if re.search(self.IS_KEYWORD_RE, string):
            return True
        return False

    def is_int(self, string: str) -> bool:
        if re.search(self.IS_INT_RE, string):
            return True
        return False
    
    def is_float(self, string: str) -> bool:
        if re.search(self.IS_FLOAT_RE, string):
            return True
        return False

    def is_string(self, string: str) -> tuple[bool, str]:
        if re.search(self.IS_STRING_RE, string):
            string = string.strip('"')
            string = string.strip("'")
            return True, string
        return False, None
    
    def is_comment(self, string: str) -> bool:
        if re.search(self.IS_COMMENT_RE, string):
            return True
        return False