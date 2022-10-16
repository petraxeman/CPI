import typing, os, exceptions
from dataclasses import dataclass


class FilePathOrigin:
    file_object: typing.TextIO
    file_path: str
    current_place: str
    origin: str
    
class IncludeHandler:
    def __init__(self, user_dirs: list[str] = [], sys_dirs: list[str] = []) -> None:
        self.user_dirs = user_dirs
        self.sys_dirs = sys_dirs

        self._current_places = None
    
    def add_place(self, file_path_origin: 'FilePathOrigin') -> None:
        if file_path_origin is None:
            self._current_places.append(file_path_origin)
        else:
            self._current_places.append(file_path_origin.current_place)
    
    def init_tu(self, file_path: str, encoding: str = 'utf8') -> 'FilePathOrigin':
        _ = FilePathOrigin(
                open(file_path, 'rw', encoding=encoding),
                file_path,
                self._get_abspath_from_path(file_path),
                'TU'
            )
        self.add_place()
        return _
    
    def _get_abspath_from_path(self, path: str) -> str:
        return os.path.dirname(os.path.abspath(path))

class FileIncludeStack:
    def __init__(self) -> None:
        self._file_include_stack = []
    
    def start_include(self, file: 'FilePathOrigin', line: int) -> None:
        self._file_include_stack.append()

    @property
    def depth(self) -> int:
        return len(self._file_include_stack)

    @property
    def current_file(self) -> str:
        if len(self._file_include_stack) < 1:
            raise exceptions.IncludeFileStackLengthError('Include file stack is empty')
        return self._file_include_stack[-1].file_name

class FileInclude:
    def __init__(self, file_path_origin: 'FilePathOrigin') -> None:
        self.file_path = file_path_origin.file_path
        self.tokiniser = None