import argparse

import general.exceptions as exceptions
import CPI



def is_available_translation(langs: tuple[str]) -> bool:
    if langs[0] == 'python':
        if langs[1] == 'cpp' or langs[1] == 'c' or langs[1] == 'cpi':
            return False
    return True



if __name__ == '__main__':
    available_langs = ['python', 'cpp', 'cpi']

    parser = argparse.ArgumentParser('CPI Command Line Interface.')
    parser.add_argument('-P', '--preprocess', type=bool, default=True,
                        action=argparse.BooleanOptionalAction,
                        help = 'Use preprocessor when translating')
    parser.add_argument('-C', '--keep-comments', type=bool, default=False,
                        action=argparse.BooleanOptionalAction,
                        help = 'Keep or remove comments after translate')
    parser.add_argument('from_lang', metavar='From-language', type=str,
                        help = "Language from translating (can be 'python', 'cpp', 'cpi')")
    parser.add_argument('to_lang', metavar='To-language', type=str,
                        help = "Language to translating (can be 'python', 'cpp', 'cpi')")
    parser.add_argument('dir', metavar='Directory', type=str,
                        help = 'Directory with source files')
    parser.add_argument('file', metavar='File', type=str,
                        help='Path to root file')
    
    args = parser.parse_args()

    if args.from_lang not in available_langs or args.to_lang not in available_langs:
        raise exceptions.UndefinedLanguage(f'Language "{args.from_lang}" or "{args.to_lang}" is not supported')
    if not is_available_translation((args.from_lang, args.to_lang)):
        raise exceptions.ArgumentError(f'Translation not available from:{args.from_lang} to:{args.to_lang}')
    
    CPI.main(args.dir, args.file, args.from_lang, args.to_lang, args.keep_comments, args.preprocess)
