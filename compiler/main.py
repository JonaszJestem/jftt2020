from .parser import JFTTParser
from .lexer import JFTTLexer
import sys


def parse(code):
    lexer = JFTTLexer()
    parser = JFTTParser()

    tokens = lexer.tokenize(code)
    program = parser.parse(tokens)
    result = program.generate_code()

    return result


if __name__ == "__main__":
    file_name = sys.argv[1]

    with open('workfile') as f:
        code = f.read()
        print(parse(code))
