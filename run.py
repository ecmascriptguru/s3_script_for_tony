import os, argparse
from src.gluefile import gluefile
from src.clean import clean


class Processor:
    gluefile = 'gluefile'
    clean = 'clean'

    @classmethod
    def run(cls, option):
        if option == cls.gluefile:
            gluefile()
        elif option == cls.clean:
            clean()


if __name__ == "__main__":
    args = os.sys.argv
    if len(args) < 2:
        raise Exception("Insufficient args. Please check readme.")
    
    Processor.run(args[1])
