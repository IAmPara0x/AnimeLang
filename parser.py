from rply import ParserGenerator
from ast import Integer, Float, Add, Substract, Multiply, Divide, S_expression, Print, Exit
from tokens import TOKENS_DICT


class Parser():
    def __init__(self):
        self.new_list = S_expression()  # TODO: need to add a proper way to store list and to reduce time complexity
        self.pg = ParserGenerator([token_name for token_name in TOKENS_DICT.keys()],
                                  precedence=[('left', ['ADD', 'SUBSTRACT']),
                                              ('left', ['MULTIPLY', 'DIVIDE'])])

    def parse(self):

        ####### GRAMMAR FOR PRINTING STUFF ########
        @self.pg.production('program : PRINT expression LINE_END')
        def program(p):
            return Print(p[1])

        # @self.pg.production('program : expression LINE_END')
        @self.pg.production('program : expression')  # TODO: replace this line with above one
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
            self.new_list = S_expression()
            return p[0]

        @self.pg.production('s_expression : S_OPEN_PAREN expression')
        def list_begin(p):
            return p[1]

        @self.pg.production('expression : expression  expression')
        def list_parse(p):
            self.new_list.value.insert(0, p[0].eval())
            return p[1]

        @self.pg.production('expression : expression  S_CLOSE_PAREN')
        def list_end(p):
            self.new_list.value.insert(0, p[0].eval())
            return self.new_list


        ######## GRAMMAR FOR EXIT ########
        @self.pg.production('expression : CLOSE')
        def expression_number(p):
            return Exit()

        ######## ERROR Handling - UwU ########

        @self.pg.error
        def error_handler(token):
            raise ValueError("Ran into a %s where it wasn't expected" % token.gettokentype())

    def get_parser(self):
        return self.pg.build()
