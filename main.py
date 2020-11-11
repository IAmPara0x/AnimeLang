from lexer import Lexer
from tokens import TOKENS_DICT
from parser import Parser


lexer = Lexer()
lexer.add_tokens(TOKENS_DICT)
lexer.add_ignore('\s+')

pg = Parser()
pg.parse()
parser = pg.get_parser()

# Main loop for getting input

while True:
    code = input("animeLang > ")
    all_tokens = lexer.get_lexer().lex(code)
    parser.parse(all_tokens).eval()
    # for i in all_tokens:
    #     print(i)
    # print(parser.parse(all_tokens).eval())
