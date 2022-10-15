import typing
from dataclasses import dataclass


class FilePathOrigin:
    file_object: typing.TextIO
    file_path: str
    current_place: str
    origin: str
    
class IncludeHandler:
    pass