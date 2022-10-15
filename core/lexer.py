import typing
from include_handler import IncludeHandler
from macro_environment import MacroEnv
from preprocessor_token import PPToken



class Lexer:
    def __init__(self, file_path: str, include_handler: 'IncludeHandler') -> None:
        self._file_path = file_path
        self._include_handler = include_handler or IncludeHandler()
        self._macro_env = MacroEnv()
    
    def token_generator(self) -> 'PPToken':
        yield _next_token()
    
    def get_all_tokens(self) -> list['PPToken']:
        return [PPToken()]
    
    def _next_token(self) -> 'PPToken':
        return PPToken()