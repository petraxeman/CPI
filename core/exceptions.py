class ExceptionCPI(Exception):
    # Простое исключение
    pass

###################### 
# Исключения Лексера #
######################

class ExceptionGeneratingLexer(ExceptionCPI):
    # Выдается если производится попытка запустить генератор токенов
    # когда генерация уже запущена
    pass