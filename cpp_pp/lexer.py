import re
from locale import currency
from sre_parse import WHITESPACE

from sklearn.metrics import classification_report
from cpp_pp.include_handler import IncludeHandler
from cpp_pp import cpp_pp_exceptions as exceptions


class Token:
    def __init__(self, text: str, token_type: str = 'UND') -> None:
        self.text = text
        self.type = token_type
    @property
    def is_whitespace(self) -> bool:
        return self.text[0] in [' ', '\n', '\t']
    def __repr__(self) -> str:
        return f'<Token {repr(self.text)} {self.type}>'


class Lexer:
    DERECTIVES = {'SD': [':', ';', '=', '-', '+', '*', '/', '%', '++', '--', '==', '!=',
                         '>', '>=', '<', '<=', '!', '&&', '||', '~', '&', '|', '^', '<<', '>>',
                         '(', ')', '[', ']', '{', '}', '+=', '-=', '*=', '/=', '%=', '|=', '^=',
                         '<<=', '>>=', ' ', '\n', '\\', '\t', '\r', '#', ',', '/*', '*/'],
                  'PPD': ['define', 'undefine', 'ifdef', 'ifndef'],
                  'CPPD': ['char', 'char8_t', 'char16_t', 'char32_t', 
                           'alignas', 'and', 'and_eq', 'asm', 'auto', 'bitand', 'bitor', 'bool', 'break', 'case', 'catch', 'class',
                           'compl', 'concept', 'const', 'const_cast', 'consteval', 'constexpr', 'constinit', 'continiue', 'co_await',
                           'co_return', 'co_yield', 'decltype', 'default', 'delete', 'do', 'double', 'dynamic_cast', 'else', 'enum',
                           'explicit', 'export', 'extern', 'false', 'float', 'for', 'friend', 'goto', 'if', 'inline', 'int', 'long',
                           'mutable', 'namespace', 'namespace', 'new', 'noexcept', 'not', 'not_eq', 'nullptr', 'operator', 'or', 'or_eq',
                           'private', 'protected', 'public', 'requires', 'return', 'short', 'signed', 'sizeof', 'static', 'static_assert',
                           'static_cast', 'struct', 'switch', 'template', 'this', 'thread_local', 'throw', 'true', 'try', 'typedef', 
                           'typeid', 'typename', 'union', 'unsigned', 'using', 'virtual', 'void', 'volatile', 'wchar_t', 'while', 'xor', 'xor_eq']}
    IS_FLOAT_RE = re.compile('^([+-]?[0-9]*\.?[0-9]*)$')
    IS_INT_RE = re.compile('^([+-]?[0-9]\.?0?)$')
    IS_STRING_RE = re.compile(r"""([bruf]*)(\"""|'''|"|')(?:(?!\2)(?:\\.|[^\\]))*\2""")
    def __init__(self, 
                 file_path: str,
                 include_handler: 'IncludeHandler') -> None:
        self.root_file_path = file_path
        self.include_handler = include_handler

    def process(self, text = None) -> 'Token':
        if text is None:
            with open(self.root_file_path, 'r', encoding='utf8') as file:
                text = file.read()
        
        current_token = ''
        in_string = False; in_comment = False

        for char in text:
            if current_token == '':
                current_token += char
                continue

            if current_token == '"' or current_token == "'":
                in_string = True
            
            if in_comment:
                if current_token + char == '*/':
                    in_comment = False
                    current_token = ''
                    continue
                current_token = char
                continue

            if in_string:
                if char == '"' or char == "'":
                    in_string = False
                    current_token += char
                    continue
                current_token += char
                continue

            if char == ' ' and current_token == ' ':
                continue
            
            if current_token + char == '/*':
                in_comment = True
                continue

            if current_token + char in self.DERECTIVES['SD']:
                yield Token(current_token + char, 'SD'); current_token = ''
                continue
            elif current_token in self.DERECTIVES['SD']:
                yield Token(current_token, 'SD'); current_token = ''

            for code in self.DERECTIVES:
                if current_token in self.DERECTIVES[code]:
                    if code != 'SD':
                        yield Token(current_token, code); current_token = ''
            
            if char in self.DERECTIVES['SD']:
                _is_num, _num_value = self.is_num(current_token)
                if _is_num:
                    yield Token(_num_value, 'NUM_CONST'); current_token = ''
                
                _is_str, _str_value = self.is_str(current_token)
                if _is_str:
                    yield Token(_str_value, 'STR_CONST'); current_token = ''
                
                if not _is_num and not _is_str:
                    yield Token(current_token, 'ID'); current_token = ''
            
            current_token += char

    def is_num(self, string: str) -> bool or str:
        if string == '':
            return False, None
        if len(re.findall(self.IS_INT_RE, string)) > 0:
            return True, int(string)
        elif len(re.findall(self.IS_FLOAT_RE, string)) > 0:
            return True, float(string)
        return False, None
    
    def is_str(self, string: str) -> bool or str:
        if string == '':
            return False, None
        if len(re.findall(self.IS_STRING_RE, string)) > 0:
            string = string.strip('"')
            string = string.strip("'")
            return True, string
        return False, None