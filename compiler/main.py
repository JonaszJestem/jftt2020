from .parser import JFTTParser
from .lexer import JFTTLexer

def parse(code):
    lexer = JFTTLexer()
    parser = JFTTParser()

    tokens = lexer.tokenize(code)
    program = parser.parse(tokens)
    result = program.generate_code()

    return result
