import unittest
from tests.cases import PRINT_TESTCASE_DICT
from lexer import Lexer
from tokens import TOKENS_DICT
from parser import Parser


lexer = Lexer()
lexer.add_tokens(TOKENS_DICT)
lexer.add_ignore('\s+')

pg = Parser()
pg.parse()
parser = pg.get_parser()


class TestAnimeLang(unittest.TestCase):

    def test_print(self):
        for i in PRINT_TESTCASE_DICT.keys():
            all_tokens = lexer.get_lexer().lex(PRINT_TESTCASE_DICT[i][0])
            ans = parser.parse(all_tokens).eval()
            self.assertEqual(ans, PRINT_TESTCASE_DICT[i][1])