import os


def _mkdir(name:str)->None:
    if not (os.path.exists(name)):
        os.mkdir(name)

def _touch(name:str)->None:
    if not (os.path.exists(name)):
        open(name, "w").write("")

def setup()->None:
    _mkdir("build/")
    _mkdir("build/types")
    _touch("build/types/functions.types")