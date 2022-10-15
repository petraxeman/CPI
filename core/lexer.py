import typing, exceptions

from include_handler import IncludeHandler
from macro_environment import MacroEnv
from preprocessor_token import PPToken



class Lexer:
    MAX_INCLUDE_DEPTH = 100

    def __init__(self, file_path: str, include_handler: 'IncludeHandler') -> None:
        self._file_path = file_path
        self._include_handler = include_handler or IncludeHandler()
        self._macro_env = MacroEnv()

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
        if generaotr:
            if self._is_generating:
                raise exceptions.ExceptionGeneratingLexer()
            self._is_generating = True
            for token in _tokens_generator():
                yield token
            self._is_generating = False
        else:
            return [token for token in _tokens_generator()]

    def _tokens_generator(self) -> 'PPToken':
        for i in range(10):
            yield PPToken()

    def get_all_tokens(self) -> list['PPToken']:
        return [PPToken()]
    
    def _next_token(self) -> 'PPToken':
        return PPToken()