from lexer import Lexer
from tokens import TOKENS_DICT
from parser import Parser
from cmd import Cmd


lexer = Lexer()
lexer.add_tokens(TOKENS_DICT)
lexer.add_ignore('\s+')

pg = Parser()
pg.parse()
parser = pg.get_parser()


# Interactive Prompt for animeLang
class AnimeLangPromt(Cmd):
    prompt = "animeLang > "
    intro = "welcowme to animeLang meow. And It's neowt that i was waitwing for you b-baaaka. *Tsun* "

    def default(self, line: str) -> bool:
        all_tokens = lexer.get_lexer().lex(line)
        print(parser.parse(all_tokens).eval())


if __name__ == "__main__":
    # Main loop for getting input
    AnimeLangPromt().cmdloop()
