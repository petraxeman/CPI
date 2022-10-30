import re
from cpp.include_handler import IncludeHandler
from cpp import cpp_pp_exceptions as exceptions
from general.base_lexer import BaseLexer

class Token:
    def __init__(self,
                 text: str,
                 position: tuple[int, int],
                 token_type: str = 'UND') -> None:
        self.text:     str   = text
        self.type:     str   = token_type
        self.position: tuple = position
    @property
    def is_whitespace(self) -> bool:
        return self.text[0] in [' ', '\n', '\t']
    def __repr__(self) -> str:
        return f'<Token {repr(self.text)} {self.type} at l{self.position[0]}:c{self.position[1]}>'


class Lexer(BaseLexer):
    DERECTIVES = {'SD': [':', ';', '=', '-', '+', '*', '/', '%', '++', '--', '==', '!=',
                         '>', '>=', '<', '<=', '!', '&&', '||', '~', '&', '|', '^', '<<', '>>',
                         '(', ')', '[', ']', '{', '}', '+=', '-=', '*=', '/=', '%=', '|=', '^=',
                         '<<=', '>>=', ' ', '\n', '\\', '\t', '\r', '#', ',', '/*', '*/'],
                  'PPD': ['define', 'undef', 'ifdef', 'ifndef', 'error', 'import', 'pragma', 'if', 'elif', 'include', 'else', 'line', 'using'],
                  'CPPD': ['char', 'char8_t', 'char16_t', 'char32_t', 
                           'alignas', 'and', 'and_eq', 'asm', 'auto', 'bitand', 'bitor', 'bool', 'break', 'case', 'catch', 'class',
                           'compl', 'concept', 'const', 'const_cast', 'consteval', 'constexpr', 'constinit', 'continiue', 'co_await',
                           'co_return', 'co_yield', 'decltype', 'default', 'delete', 'do', 'double', 'dynamic_cast', 'else', 'enum',
                           'explicit', 'export', 'extern', 'false', 'float', 'for', 'friend', 'goto', 'if', 'inline', 'int', 'long',
                           'mutable', 'namespace', 'namespace', 'new', 'noexcept', 'not', 'not_eq', 'nullptr', 'operator', 'or', 'or_eq',
                           'private', 'protected', 'public', 'requires', 'return', 'short', 'signed', 'sizeof', 'static', 'static_assert',
                           'static_cast', 'struct', 'switch', 'template', 'this', 'thread_local', 'throw', 'true', 'try', 'typedef', 
                           'typeid', 'typename', 'union', 'unsigned', 'using', 'virtual', 'void', 'volatile', 'wchar_t', 'while', 'xor', 'xor_eq']}
    def __init__(self, 
                 file_path:       str,
                 keep_comments:   bool) -> None:
        self.file_path: str                    = file_path
        self.keep_comments: bool               = keep_comments
    
    def process(self, text = None) -> 'Token':
        with open(self.file_path, 'r', encoding='utf8') as file:
            text = file.read()

        current_token: str      = ''
        position:      tuple    = (1, 1)
        skip_symbols:  int      = 0
        in_string:     bool     = False
        in_comment:    bool     = False

        for char_index in range(len(text)):

            char:        str       = text[char_index]
            triple_char: list[str] = text[char_index:char_index+3]
            double_char: list[str] = text[char_index:char_index+2]

            if char == '\n': position = (position[1]+1, 0)
            position = (position[1], position[0]+1)

            if skip_symbols > 0:
                skip_symbols -= 1
                continue
            
            if triple_char in ['"""', "'''"] or char in ['"', "'"]:
                if current_token != '':
                    yield self.token_from_string(current_token, position); current_token = ''
                if triple_char in ['"""', "'''"]:
                    current_token = triple_char
                    expect = triple_char
                elif char in ["'", '"']:
                    current_token = char
                    expect = char
                in_string = True
            
            if in_string:
                if triple_char == expect or char == expect:
                    current_token += expect
                    expect = ''
                    yield self.token_from_string(current_token, position); current_token = ''
                    in_string = False
                else:
                    current_token += char
                
            if triple_char in self.DERECTIVES['SD']:
                if current_token != '':
                    yield self.token_from_string(current_token, position); current_token = ''
                yield self.token_from_string(triple_char, position)
                skip_symbols = 2
                continue
            
            if double_char in self.DERECTIVES['SD']:
                if current_token != '':
                    yield self.token_from_string(current_token, position); current_token = ''
                yield self.token_from_string(double_char, position)
                skip_symbols = 1
                continue

            if char in self.DERECTIVES['SD']:
                if current_token != '':
                    yield self.token_from_string(current_token, position); current_token = ''
                yield self.token_from_string(char, position)
                continue
                
            current_token += char

    def token_from_string(self, string: str, position: tuple) -> 'Token':
        result, value = self.is_keyword(string)
        if result:
            for category in self.DERECTIVES:
                if value in self.DERECTIVES[category]:
                    return Token(value, position, token_type=category)
            
        result, value = self.is_string(string)
        if result:
            return Token(value, position, token_type='STR_CONST')
        
        result, value = self.is_number(string)
        if result:
            if type(value) == type(int()):
                return Token(value, position, token_type='INT_CONST')
            elif type(value) == type(float()):
                return Token(value, position, token_type='FLT_CONST')



        











'''
            if in_comment:
                if text[char_index:char_index+2] == '*/':
                    in_comment = False
                    current_token += char
                    continue
                current_token += char
                continue

            if in_string:
                if char == '"' or char == "'":
                    in_string = False
                    current_token += char
                    continue
                current_token += char
                continue

        for char in text:
            position = (position[0]+1, position[1])
            if char == '\n':
                position = (0, position[1]+1)
            pass
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
                
                if not _is_num and not _is_str and current_token != '':
                    yield Token(current_token, 'ID'); current_token = ''
            
            current_token += char
            '''