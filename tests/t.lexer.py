from sys import path
path.append('/'.join((path[0].split("/")[:-1])))
########################################

from src.toolchain.Lexer import *
from src.toolchain.Parser import *
from src.toolchain.Cli import *
import json


setup()
lexer = Lexer(open("./examples/main.brick", "r").read())
tokens = lexer.tokenize()
parser = Parser(tokens)
parser.parse()
print(json.dumps(parser.ast, indent=4))