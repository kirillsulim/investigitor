from investigitor.git_tools import GitBlameProvider

from  pprint import pprint

class InvestigitorApp():

    def __init__(self):
        pass

    @staticmethod
    def _init_parser():
        pass

    def run(self, args):
        g = GitBlameProvider()

        res = g.blame(args[1])

        for x in res:
            pprint(x)

