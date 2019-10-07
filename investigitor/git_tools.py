from pathlib import Path
from typing import List, TextIO, Iterator, Optional
from subprocess import Popen, PIPE
from datetime import datetime, tzinfo
from io import TextIOWrapper

from investigitor.blame_provider import BlameProvider, BlameRecord


class CommitInfo():
    def __init__(self, author: str, timestamp: datetime):
        self.author = author
        self.timestamp = timestamp


class GitBlameProvider(BlameProvider):
    def blame(self, file: Path) -> List[BlameRecord]:
        with Popen(
            ['git', '--no-pager', 'blame',  '--porcelain', str(file)],
            stdout=PIPE,
            stderr=PIPE,
        ) as p:
            error_lines = p.stderr.readlines()
            if not error_lines:
                return [x for x in self._records(TextIOWrapper(p.stdout))]
            else:
                print('Error:\n' + '\n'.join(error_lines))

    def _records(self, s: TextIO) -> Iterator[BlameRecord]:
        commits = {}

        while s:
            line = s.readline().split(maxsplit=1)
            if not line:
                break
            [commit, _] = line
            if commit not in commits:
                while True:
                    line = list(map(str.strip, s.readline().split(' ', 1)))
                    if line[0] != 'boundary':
                        [key, value] = line
                        if key == 'author':
                            author = value
                        elif key == 'author-time':
                            timestamp = int(value)
                        elif key == 'author-tz':
                            tz = value
                    else:
                        s.readline() # skip filename
                        commits[commit] = CommitInfo(author, datetime.fromtimestamp(timestamp))
                        break

            line = s.readline().lstrip('\t').rstrip('\n')

            yield BlameRecord(
                commit=commit,
                author=commits[commit].author,
                timestamp=commits[commit].timestamp,
                line=line
            )
