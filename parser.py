from rply import ParserGenerator
from ast import Integer, Float, Add, Substract, Multiply, Divide, List_type, Print, Exit
from tokens import TOKENS_DICT


class Parser():
    def __init__(self):
        self.pg = ParserGenerator([token_name for token_name in TOKENS_DICT.keys()],
                                  precedence=[('left', ['ADD', 'SUBSTRACT']),
                                              ('left', ['MULTIPLY', 'DIVIDE'])])

    def parse(self):

        ####### GRAMMAR FOR PRINTING STUFF ########
        @self.pg.production('program : PRINT expression LINE_END')
        def program(p):
            return Print(p[1])

        # @self.pg.production('program : expression LINE_END')
        # TODO: replace this line with above one
        @self.pg.production('program : expression')
        def program(p):
            return Print(p[0])

        ######## GRAMMAR FOR BASIC ARITHMETIC CALCULATIONS ########
        @self.pg.production('expression : OPEN_PAREN expression CLOSE_PAREN')
        def expression_parens(p):
            return p[1]

        @self.pg.production('expression : expression SUBSTRACT expression')
        @self.pg.production('expression : expression ADD expression')
        @self.pg.production('expression : expression MULTIPLY expression')
        @self.pg.production('expression : expression DIVIDE expression')
        def expression_binayop(p):
            left = p[0]
            right = p[2]

            if p[1].gettokentype() == 'ADD':
                return Add(left, right)
            elif p[1].gettokentype() == 'SUBSTRACT':
                return Substract(left, right)
            elif p[1].gettokentype() == 'MULTIPLY':
                return Multiply(left, right)
            elif p[1].gettokentype() == 'DIVIDE':
                return Divide(left, right)
            else:
                raise AssertionError(
                    'B-Baakaa Baaaaaaaaaaaaaaka you made a mistake Baaaaka.')

        ########  GRAMMA FOR BASIC DATATYPES ########
        @self.pg.production('expression : INTEGER')
        @self.pg.production('expression : FLOAT')
        def expression_number(p):
            if p[0].gettokentype() == 'FLOAT':
                return Float(p[0].value)
            elif p[0].gettokentype() == 'INTEGER':
                return Integer(p[0].value)

        ######## GRAMMAR FOR LISTS ########

        @self.pg.production('expression : s_expression')
        def new_list_type(p):
            return p[0]

        @self.pg.production('s_expression : S_OPEN_PAREN expression')
        def list_end(p):
            return p[1]

        @self.pg.production('expression : expression  expression')
        def list_parse(p):
            p[1].value.insert(0, p[0].eval())
            return p[1]

        @self.pg.production('expression : expression  S_CLOSE_PAREN')
        def list_begin(p):
            new_list = List_type()
            new_list.value.insert(0, p[0].eval())
            return new_list

        @self.pg.production('expression : INDEX_W C_OPEN_PAREN expression C_CLOSE_PAREN s_expression')
        def get_list_index(p):
            p[4].is_index = True
            p[4].index = p[2].eval()
            return p[4]

        ######## GRAMMAR FOR EXIT ########
        @self.pg.production('expression : CLOSE')
        def expression_number(p):
            return Exit()

        ######## ERROR Handling - UwU ########

        @self.pg.error
        def error_handler(token):
            raise ValueError(
                "Ran into a %s where it wasn't expected" % token.gettokentype())

    def get_parser(self):
        return self.pg.build()
