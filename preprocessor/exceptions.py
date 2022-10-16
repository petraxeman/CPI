class ExceptionCPI(Exception):
    # Простое исключение
    pass

###################### 
# Исключения Лексера #
######################

class AllreadyGeneratingLexerError(ExceptionCPI):
    # Выдается если производится попытка запустить генератор токенов
    # когда генерация уже запущена
    pass

class NotFoundFileError(ExceptionCPI):
    # Выдается когда была попытка открыть файл
    # Но файл не был найден
    pass

##############################
# Исключения Инклюд Хендлера #
##############################

class IncludeFileStackLengthError(ExceptionCPI):
    # Список включаемых файлов пуст
    pass
