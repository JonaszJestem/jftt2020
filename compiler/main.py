from parser import JFTTParser
from lexer import JFTTLexer
import sys


def parse(code):
    lexer = JFTTLexer()
    parser = JFTTParser()

    tokens = lexer.tokenize(code)
    program = parser.parse(tokens)
    result = program.generate_code()

    return result


file_name = sys.argv[1]
output = sys.argv[2]

with open(file_name) as f:
    code = f.read()
    with open(output, 'w+') as out:
        out.write(parse(code))
