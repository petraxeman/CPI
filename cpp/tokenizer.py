import re, copy
from cpp.include_handler import IncludeHandler
from general import exceptions
from general.base_tokenizer import BaseTokenizer, Token, Position


class Tokenizer(BaseTokenizer):
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
                 text:          str,
                 keep_comments: bool,
                 filename:      str = None) -> None:
        if filename == None:
            self.filename = 'Undefined'
        else:
            self.filename = filename
        self.text:          str  = text
        self.keep_comments: bool = keep_comments
    
    def process(self) -> 'Token':
        current_token:          str        = ''
        position:               'Position' = Position(1, 0)
        skip_symbols:           int        = 0
        in_string:              bool       = False
        in_comment:             bool       = False

        for char_index in range(len(self.text)):

            char:        str       = self.text[char_index]
            triple_char: list[str] = self.text[char_index:char_index+3]
            double_char: list[str] = self.text[char_index:char_index+2]

            if char == '\n': position.increment_line()
            else: position.increment_column()

            if skip_symbols > 0:
                skip_symbols -= 1
                continue
            
            if double_char == '/*':
                if current_token != '':
                    yield self.build_token(current_token, position.get_and_mark()); current_token = ''
                if self.keep_comments:
                    current_token = '/*'
                expect     = '*/'  
                in_comment = True
            
            if in_comment:
                if double_char == '*/':
                    skip_symbols = 1
                    expect = ''
                    in_comment = False
                    if self.keep_comments:
                        yield self.build_token(current_token + '*/', position.get_and_mark()); current_token = ''
                elif self.keep_comments:
                    current_token += char
                continue
            
            if triple_char in ['"""', "'''"] and not in_string:
                if current_token != '':
                    yield self.build_token(current_token, position.get_and_mark()); current_token = ''
                current_token = triple_char
                expect = triple_char
                skip_symbols = 2
                in_string = True
                continue
            elif char in ['"', "'"] and not in_string:
                if current_token != '':
                    yield self.build_token(current_token, position.get_and_mark()); current_token = ''
                current_token = char
                expect = char
                in_string = True
                continue
            
            if in_string:
                if triple_char == expect or char == expect:
                    current_token += expect
                    skip_symbols = 2 if len(expect) > 1 else 0
                    expect = ''
                    yield self.build_token(current_token, position.get_and_mark()); current_token = ''
                    in_string = False
                else:
                    current_token += char
                continue
                
            if triple_char in self.DERECTIVES['SD']:
                if current_token != '':
                    yield self.build_token(current_token, position.get_and_mark()); current_token = ''
                yield self.build_specific_token(triple_char, position.get_and_mark(), 'SD')
                skip_symbols = 2
                continue
            
            if double_char in self.DERECTIVES['SD']:
                if current_token != '':
                    yield self.build_token(current_token, position.get_and_mark()); current_token = ''
                yield self.build_specific_token(double_char, position.get_and_mark(), 'SD')
                skip_symbols = 1
                continue

            if char in self.DERECTIVES['SD']:
                if current_token != '':
                    yield self.build_token(current_token, position.get_and_mark()); current_token = ''
                yield self.build_specific_token(char, position.get_and_mark(), 'SD')
                continue
                
            current_token += char