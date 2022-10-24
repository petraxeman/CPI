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
    def __init__(self, file_path: str,
                 include_handler: 'IncludeHandler',
                 tokenizer: 'Tokenizer' = None) -> None:
        self.root_file_path = file_path
        self.include_handler = include_handler
        self.tokenizer = tokenizer or Tokenizer()

    def token_generator(self) -> 'Token':
        for token in self.tokenizer.process(text):
            yield token


class Tokenizer:
    DELIMITER = list(r'#:(){}, ;"\'')
    DELIMITER.append('\n')
    ALPHABET = {'PPD': ['if', 'define', 'undefine', 'ifndef', 'ifdef'],
                'CPPD': ['int', 'char', 'float', '<<', 'cout']}
    WHITESPACE = [' ', '\t', '\n']
    def __init__(self,
                 delimiter: list[str] = None,
                 alphabet: dict[str: list[str]] = None,
                 whitespaces: list[str] = None) -> None:
        self.DELIMITER = delimiter or self.DELIMITER
        self.ALPHABET = alphabet or self.ALPHABET
        self.WHITESPACE = whitespaces or self.WHITESPACE

    def process(self, text: str) -> 'Token':
        if text is None and self.text is None:
            raise exceptions.TokenizerExpectsText('Tokenizer expects text. Got None.')

        current_token = ''

        for char in text:
            if char in self.WHITESPACE and current_token == char:
                continue
            elif current_token in self.WHITESPACE and current_token != char:
                yield Token(current_token); current_token = ''

            if current_token in self.DELIMITER and current_token not in self.WHITESPACE:
                yield Token(current_token); current_token = ''

            if char in self.DELIMITER:
                if len(current_token) > 0:
                    yield Token(current_token); current_token = ''
            
            

            current_token += char