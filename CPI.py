from cpp import lexer, parser
from general import preprocessor

def main(directory: str, file_path: str,
         from_lang: str, to_lang: str,
         keep_comments: bool,
         preprocess: bool) -> None:
    FUNCTIONS = {'preprocess_python': preprocess_python,
             'preprocess_cpp': preprocess_cpp,
             'preprocess_cpi': preprocess_cpi,
             'from_python': from_python,
             'from_cpp': from_cpp,
             'from_cpi': from_cpi,
             'to_python': to_python,
             'to_cpp': to_cpp,
             'to_cpi': to_cpi}

    if preprocess:
        ast = FUNCTIONS['preprocess_' + from_lang](keep_comments)
    else:
        ast = FUNCTIONS['from_' + from_lang](keep_comments)
    
    FUNCTIONS['to_' + to_lang](ast)
        

def preprocess_python():
    pass


def preprocess_cpp():
    pass


def preprocess_cpi():
    pass


def preprocess():
    pass

    
def from_python():
    pass


def from_cpp():
    pass


def from_cpi():
    pass


def to_python():
    pass


def to_cpp():
    pass


def to_cpi():
    pass