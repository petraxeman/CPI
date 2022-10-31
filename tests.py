from cpp.tokenizer import Tokenizer

with open('./example.cpp', 'r', encoding='utf8') as file:
    t = Tokenizer(file.read(), True)

counter = 0
for tok in t.process():
    print(tok)
    counter += 1

    if counter == 200:
        break
#input('--- PAUSE ---')