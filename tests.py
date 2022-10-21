from cpp_pp import lexer

text = '''
#define BLOB 1
#ifdef BLOB

int simple_function (int x, int y) {
    cout << "Hello world!";
    cout << BLOB;
    return 0;
}

#endif
'''

t = lexer.Tokenizer()
for i in t.process(text):
    if i.type == 'WS':
        continue
    print(i)