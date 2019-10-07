from typing import List
from pathlib import Path
from datetime import datetime


class BlameRecord:
    def __init__(self, commit: str, author: str, timestamp: datetime, line: str):
        self.commit = commit
        self.author = author
        self.timestamp = timestamp
        self.line = line

    def __repr__(self):
        return f'{self.commit} <{self.author}> {self.timestamp} {self.line}'


class BlameProvider():

    def __init__(self):
        pass

    def blame(self, file: Path) -> List[BlameRecord]:
        raise NotImplementedError()
