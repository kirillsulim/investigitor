from pathlib import Path
from typing import List, TextIO, Iterator, Optional
from subprocess import Popen, PIPE
from datetime import datetime, tzinfo
from io import TextIOWrapper
from pprint import pprint


from git import Repo

from investigitor.blame_provider import BlameProvider, BlameRecord


class CommitInfo():
    def __init__(self, author: str, timestamp: datetime):
        self.author = author
        self.timestamp = timestamp


class GitBlameProvider(BlameProvider):

    def _repo_by_file(self, path: Path) -> Optional[Repo]:
        if path == Path.root:
            return None
        possible_git_dir = path / '.git'
        if possible_git_dir.exists():
            return Repo(path)
        return self._repo_by_file(path.parent)

    def blame(self, file: Path) -> List[BlameRecord]:
        repo = self._repo_by_file(file)
        blame = repo.blame('HEAD', file)

        res = []
        for (commit, lines) in blame:
            for line in lines:
                res.append(BlameRecord(commit=commit.hexsha, author=commit.author.name, timestamp=commit.authored_date, line=line))
        return res

