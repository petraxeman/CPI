from cpp import lexer


t = lexer.Lexer('./example.cpp', True)
for i in t.process():
    print(i)
input('--- PAUSE ---')