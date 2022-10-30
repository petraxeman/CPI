import re
if __name__ == '__main__':
    from datatypes import FileOrigin
    from include_handler import IncludeHandler
else:
    from general.datatypes import FileOrigin
    from general.include_handler import IncludeHandler

class RawToken:
    pass

class BaseLexer:
    IS_FLOAT_RE = re.compile('^([+-]?[0-9]*\.?[0-9]*)$')
    IS_INT_RE = re.compile('^([+-]?[0-9]\.?0?)$')
    IS_STRING_RE = re.compile(r"""([bruf]*)(\"""|'''|"|')(?:(?!\2)(?:\\.|[^\\]))*\2""")
    IS_KEYWORD_RE = re.compile(r'^[a-zA-Z_][0-9a-zA-Z_]*$')
    

    def is_keyword(self, string: str) -> bool:
        if string == '':
            return False, None
        
        if len(re.findall(self.IS_KEYWORD_RE, string)) > 0:
            return True, string
        
        return False, None


    def is_number(self, string: str) -> tuple[bool, str]:
        if string == '':
            return False, None
        
        if len(re.findall(self.IS_INT_RE, string)) > 0:
            return True, int(string)
        elif len(re.findall(self.IS_FLOAT_RE, string)) > 0:
            return True, float(string)

        return False, None
    

    def is_string(self, string: str) -> bool or str:
        if string == '':
            return False, None

        if len(re.findall(self.IS_STRING_RE, string)) > 0:
            string = string.strip('"')
            string = string.strip("'")
            return True, string

        return False, None