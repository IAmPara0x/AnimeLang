#! /usr/bin/python3

import sys
from pathlib import Path
from lexer import Lexer
from tokens import TOKENS_DICT
from parser import Parser
from cmd import Cmd
import warnings

warnings.filterwarnings(
  "ignore"
)  ### NOTE: use this to disable all the warnings during release

lexer = Lexer()
lexer.add_tokens(TOKENS_DICT)
lexer.add_ignore("\s+")

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
  if len(sys.argv) >= 2:
    if sys.argv[1] == "--f":
      if len(sys.argv) != 3:
        print("Meow you haven't given a filwe to read. Ba-aaaka")
      else:
        filename = sys.argv[2]
        if Path(filename).suffix == ".ecchi":
          file = None
          with open(filename, "r") as f:
            file = f.read()
          all_tokens = lexer.get_lexer().lex(file)
          # NOTE: uncomment this for errors
          try:
            parser.parse(all_tokens).eval()
          except Exception as e:
            print(e)
            pg.print_stack.eval()
          # parser.parse(all_tokens).eval()

        else:
          print("Meow the filename was not of type '.ecchi'")
  else:
      AnimeLangPromt().cmdloop()
