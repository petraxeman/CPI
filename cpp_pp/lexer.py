from locale import currency
from cpp_pp.include_handler import IncludeHandler
from cpp_pp import cpp_pp_exceptions as exceptions


class Token:
    def __init__(self, text: str, token_type: str = '') -> None:
        self.text = text
        self.type = token_type
    @property
    def is_whitespace(self) -> bool:
        return self.text[0] in [' ', '\n', '\t']
    def __repr__(self) -> str:
        return fr'<Token "{self.text}" {self.type}>'


class Lexer:
    def __init__(self, file_path: str, include_handler: 'IncludeHandler') -> None:
        self.root_file_path = file_path
        self.include_handler = include_handler
    
    def token_generator(self) -> 'Token':
        yield False


class Tokenizer:
    def __init__(self, text: str = None) -> None:
        self.PP_DERECTIVES = {
            'if': self.__if, 'ifdef': self.__ifdef,
            'ifndef': self.__ifndef, 'define': self.__define,
            'undef': self.__undef
        }
        self.C_DERECTIVES = [
            'int', 'char', 'float', '(', ')', '{', '}', '-', '+', '=', '*', '/'
        ]

        self.text = text
    
    def process(self, text: str) -> 'Token':
        DELIMITER = list(R':(){}, ;"\'')
        DELIMITER.extend(['\n', '\t'])
        print(self._DELIMITER)
        if text is None and self.text is None:
            raise exceptions.TokenizerExpectsText('Tokenizer expects text. Got None.')
        elif text is None and self.text is not None:
            text = self.text
        
        cuid = ''

        for char in text:
            if char not in DELIMITER:
                pass
            elif char in DELIMITER:
                if char in DELIMITER and char == cuid:
                    continue
                elif cuid in self.PP_DERECTIVES:
                    yield Token(cuid, 'PPD')
                    cuid = ''
                elif cuid in self.C_DERECTIVES:
                    yield Token(cuid, 'CPPD')
                    cuid = ''
                elif not cuid in self._DELIMITER:
                    yield Token(cuid, 'AI')
                    cuid = ''

            elif cuid == '#':
                yield Token('#', '#'); cuid = ''
            cuid += char
        '''
        for char in text:
            if char not in self._DELIMITER:
                if current_identifier == ' ':
                    yield Token(' ', 'WS')
                    current_identifier = ''
                elif current_identifier in self._DELIMITER:
                    yield Token(current_identifier, 'DL')
                    current_identifier = ''

            if char in self._DELIMITER:
                if current_identifier in self._DELIMITER and char == current_identifier:
                    continue
                if current_identifier == ' ' and char == ' ':
                    continue
                if current_identifier in self.PP_DERECTIVES:
                        yield Token(current_identifier, 'PPD')
                        current_identifier = ''
                elif current_identifier in self.C_DERECTIVES:
                    yield Token(current_identifier, 'CPPD')
                    current_identifier = ''
                elif not current_identifier in self._DELIMITER:
                    yield Token(current_identifier, 'AI')
                    current_identifier = ''
            
            if current_identifier == '#':
                
            current_identifier += char
        '''
    def __if(self):
        pass
    
    def __ifdef(self):
        pass

    def __ifndef(self):
        pass

    def __define(self):
        pass

    def __undef(self):
        pass

    def __is_whitespace(self, char) -> bool:
        return char in [' ', '\n', '\t']