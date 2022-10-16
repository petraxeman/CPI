import typing


class Tokeniser:
    def __init__(self, file_object: typing.TextIO, file_path: str) -> None:
        self._file = file_object

        if self._file is not None and hasattr(self._file, 'name'):
            self._file_name = self._file.name
        else:
            self._file_name = file_path