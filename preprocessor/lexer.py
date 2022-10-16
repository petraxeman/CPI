from msilib.schema import File
import typing, exceptions

from include_handler import IncludeHandler, FileIncludeStack
from macro_environment import MacroEnv



class Token:
    def __init__(self, symbol: str = '', token_type: str = None) -> None:
        self.text = symbol
        self.is_whitespace = symbol in [' ', '\n', '\t']
        self.type = token_type
    def add(self, symbol: str) -> None:
        self.text = self.text + symbol
    def set_type(self, token_type: str) -> None:
        self.type = token_type
    def __repr__(self) -> str:
        return f'<Token {self.text} {self.type}>'


class Lexer:
    MAX_INCLUDE_DEPTH = 100

    def __init__(self, file_path: str, include_handler: 'IncludeHandler') -> None:
        self._file_path = file_path
        self._include_handler = include_handler or IncludeHandler()
        self._macro_env = MacroEnv()
        self._include_file_stack = FileIncludeStack()
        self._keyword_despatch = {
            'if'        : self.__if,
            'ifdef'     : self.__ifdef,
            'ifndef'    : self.__ifndef,
            'elif'      : self.__elif,
            'else'      : self.__else,
            'endif'     : self.__endif,
            'include'   : self.__include,
            'define'    : self.__define,
            'undef'     : self.__undef,
            'line'      : self.__line,
            'error'     : self.__error,
            'pragma'    : self.__pragma,
            'warning'   : self.__warning,
        }

        self._is_generating = False
    
    def get_tokens(self, generaotr: bool = True, minimize_ws: bool = True) -> 'PPToken':
        current_tu = self._include_handler.init_tu(self._file_path)
        if current_tu is None:
            raise exceptions.NotFoundFileError(f'Not found file: {self._file_path}')
        current_tu.file_object.seek(0)

        if generaotr:
            if self._is_generating:
                raise exceptions.AllreadyGeneratingLexerError('Generating allredy started')
            
            self._is_generating = True
            #

            #
            self._is_generating = False
        else:
            return [token for token in self._tokens_generator()]

    def _tokens_generator(self) -> 'PPToken':
        for i in range(10):
            yield PPToken()

    def get_all_tokens(self) -> list['PPToken']:
        return [PPToken()]
    
    def _next_token(self) -> 'PPToken':
        return PPToken()


class Tokeniser:
    _keywords = (
            'if', 'ifdef', 'ifndef', 'elif', 'else', 'endif', 'include', 
            'define', 'undef', 'line', 'error', 'pragma', 'warning'
        )
    def __init__(self, file_object: typing.TextIO) -> None:
        self._file = file_object
    
    def get_token(self) -> Token:
        self._file.seek(0)
        self._file_text = self._file.read()
        current_token = None

        for sym in self._file_text:
            if current_token is None:
                current_token = Token(sym, token_type = 'UD')
                continue
            
            if current_token.is_whitespace and self._is_whitespace(sym):
                pass
            elif current_token.is_whitespace and not self._is_whitespace(sym):
                yield current_token
                current_token = Token(sym)
            elif not current_token.is_whitespace and self._is_whitespace(sym):
                if current_token.text.lower() in self._keywords:
                    current_token.set_type('PPD')
                    yield current_token
                else:
                    current_token.set_type('AD')
                    yield current_token
                yield Token(' ', token_type='WS')
            
            if sym == '#':
                yield current_token
                yield Token('#', token_type = '#')
            elif current_token.text == '#':
                current_token.set_type('#')
                yield current_token
            current_token.add(sym)
    def _is_whitespace(self, sym: str) -> bool:
        return sym in [' ', '\n', '\t']
if __name__ == '__main__':
    t = Tokeniser(open('./example.cpp', 'r'))
    for tok in t.get_token():
        print(tok)