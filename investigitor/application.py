from dataclasses import dataclass, field
from pathlib import Path
from itertools import groupby

from typing import List

from investigitor.blame_provider import BlameRecord
from investigitor.git_tools import GitBlameProvider

from  pprint import pprint
from json import dumps

import json
import dataclasses


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        if isinstance(o, Path):
            return str(o)
        return super().default(o)


@dataclass
class Share:
    author: str = None
    lines: int = 0


@dataclass
class ShareNode:
    path: Path = None
    shares: List[Share] = None
    subnodes: List['ShareNode'] = None


class InvestigitorApp():

    def __init__(self):
        self.blame = GitBlameProvider()

    @staticmethod
    def _init_parser():
        pass

    def run(self, args):

        path = Path(args[1]).expanduser()
        sh = self.print_share(path)

        with open('out.json', 'w+') as out:
            out.write(dumps(sh, cls=EnhancedJSONEncoder, indent=4, sort_keys=True))

    def print_share(self, path: Path) -> ShareNode:
        if path.is_file():
            blame = self.blame.blame(path)

            shares_map = {}
            for b in blame:
                if b.author not in shares_map:
                    shares_map[b.author] = 0
                shares_map[b.author] += 1

            return ShareNode(
                path=path,
                shares=[Share(author, lines) for author, lines in shares_map.items()],
            )
        else:
            shares_map = {}
            subnodes = []
            for child in path.iterdir():
                if child.parts[-1] == '.git':
                    continue

                subnode = self.print_share(child)

                subnodes.append(subnode)
                for s in subnode.shares:
                    if s.author not in shares_map:
                        shares_map[s.author] = 0
                    shares_map[s.author] += s.lines

            return ShareNode(
                path=path,
                shares=[Share(author, lines) for author, lines in shares_map.items()],
                subnodes=subnodes,
            )
