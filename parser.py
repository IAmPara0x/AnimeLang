from rply import ParserGenerator
from ast import (
    Integer,
    Float,
    Add,
    Substract,
    Multiply,
    Divide,
    Variable_buffer,
    Eval_expressions_buffer,
    E_expressions_list,
    List_type,
    Variable_type,
    Variables_dict,
    Booleans,
    Check,
    Print,
    Exit
)
from tokens import TOKENS_DICT


class Parser():
    def __init__(self):
        self.pg = ParserGenerator([token_name for token_name in TOKENS_DICT.keys()],
                                  precedence=[('left', ['ADD', 'SUBSTRACT']),
                                              ('left', ['MULTIPLY', 'DIVIDE'])])

        self.variables_dict = Variables_dict()  # stores all the variables
        self.local_scope = None
        self.local_scope_expressions_buffer = None

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

        # returns the list created
        @self.pg.production('expression : l_expression')
        def new_list_type(p):
            return p[0]

        # parsing of the list ends here
        @self.pg.production('l_expression : S_OPEN_PAREN expression')
        def list_end(p):
            return p[1]

        # parses all the elements insides the list
        @self.pg.production('expression : expression COMMA expression')
        def list_parse(p):
            p[2].value.insert(0, p[0].eval())
            return p[2]

        # parsing of the created list begins here
        @self.pg.production('expression : expression S_CLOSE_PAREN')
        def list_begin(p):
            new_list = List_type()
            new_list.value.insert(0, p[0].eval())
            return new_list

        # gets the element from the list given index number
        @self.pg.production('expression : INDEX_W BAR expression BAR expression')
        def get_list_index(p):
            p[4].is_index = True
            p[4].index = p[2].eval()
            return p[4]

       #### GRAMMAR FOR VARIABLES ####

        # return the value of the variable
        @self.pg.production('expression : n_expression')
        def return_variable(p):
            name = p[0].value
            return self.variables_dict.get_variable(name)

        # returns the name of the variable
        @self.pg.production('n_expression : VARIABLE')
        def variable_name(p):
            return p[0]

        # returns the calculated value of the variable
        @self.pg.production('v_expression : EQUALS expression LINE_END')
        def variable_value(p):
            return p[1]

        @self.pg.production('l_expression : NEW C_INTEGER n_expression v_expression')
        def variable_int(p):
            name = p[2].value
            value = Integer(p[-1].eval()).eval()
            type = "INTEGER"
            variable = Variable_type(name, type, value)
            self.variables_dict.add_variable(name, variable)
            return variable

        @self.pg.production('l_expression : NEW C_FLOAT n_expression v_expression')
        def variable_float(p):
            name = p[2].value
            value = Float(p[-1].eval()).eval()
            type = "FLOAT"
            variable = Variable_type(name, type, value)
            self.variables_dict.add_variable(name, variable)
            return variable

        @self.pg.production('l_expression : NEW C_LIST n_expression v_expression')
        def variable_list(p):
            name = p[2].value
            value = p[-1].eval()
            type = "LIST"
            variable = Variable_type(name, type, value)
            self.variables_dict.add_variable(name, variable)
            return variable

        @self.pg.production('l_expression : NEW C_BOOL n_expression v_expression')
        def variable_bool(p):
            name = p[2].value
            value = p[-1].eval()
            type = "BOOL"
            variable = Variable_type(name, type, value)
            self.variables_dict.add_variable(name, variable)
            return variable

        @self.pg.production('l_expression : INDEX_W n_expression v_expression')
        def change_variable_value(p):
            name = p[1].value
            value = p[-1].eval()
            var = self.variables_dict.get_variable(name)
            var.value = value
            return var


        #### GRAMMAR FOR CONDITIONALS ####

        @self.pg.production('expression : b_expression')
        def booleans_expression(p):
            return p[0]

        @self.pg.production('b_expression : TRUE')
        @self.pg.production('b_expression : FALSE')
        def booleans(p):
            return Booleans(p[0].value)

        @self.pg.production('expression : CHECK OPEN_PAREN expression COMMA expression CLOSE_PAREN')
        @self.pg.production('expression : CHECK OPEN_PAREN expression COMMA expression CLOSE_PAREN local_scope_end')
        @self.pg.production('expression : CHECK OPEN_PAREN expression COMMA expression CLOSE_PAREN scope_end ELSE local_scope_end')
        def conditional_check(p):
            if len(p) == 6:
                return Check(p[2], p[4])
            elif len(p) == 7:
                cond = Check(p[2], p[4])
                val = cond.eval()
                if val == "kawai":
                    e_expression = self.local_scope.get_e_expression()
                    self.variables_dict.dict = e_expression.eval(self.variables_dict.dict)
                    if self.local_scope.len == 0:
                        self.local_scope = None
                else:
                    self.local_scope.get_e_expression()
                    if self.local_scope.len == 0:
                        self.local_scope = None
                return cond
            elif len(p) == 9:
                cond = Check(p[2], p[4])
                val = cond.eval()
                if val == "kawai":
                    e_expression = self.local_scope.get_e_expression()
                    self.variables_dict.dict = e_expression.eval(self.variables_dict.dict)
                    self.local_scope.get_e_expression()
                    if self.local_scope.len == 0:
                        self.local_scope = None
                else:
                    self.local_scope.get_e_expression()
                    e_expression = self.local_scope.get_e_expression()
                    self.variables_dict.dict = e_expression.eval(self.variables_dict.dict)
                    if self.local_scope.len == 0:
                        self.local_scope = None

                return Check(p[2], p[4])

        #### GRAMMAR for e_expressions ####

        @self.pg.production('local_scope_l_expression : local_scope NEW C_INTEGER n_expression v_expression')
        @self.pg.production('local_scope_l_expression : local_scope_l_expression NEW C_INTEGER n_expression v_expression')
        def local_scope_variable_int(p):
            name = p[3].value
            value = p[-1]
            type = "INTEGER"
            buffer = Variable_buffer(name, value, type)
            self.local_scope_expressions_buffer.add_expression(buffer)
            return buffer

        @self.pg.production('local_scope : C_OPEN_PAREN')
        def local_scope_expressions_begin(p):
            if self.local_scope is None:
                self.local_scope = E_expressions_list()
            self.local_scope_expressions_buffer = Eval_expressions_buffer()
            return p[0]

        @self.pg.production('scope_end : local_scope_l_expression C_CLOSE_PAREN')
        def scope_end(p):
            self.local_scope.add_e_expression(self.local_scope_expressions_buffer)
            return p[0]

        @self.pg.production('local_scope_end : local_scope_l_expression C_CLOSE_PAREN LINE_END')
        def local_scope_expressions_end(p):
            self.local_scope.add_e_expression(self.local_scope_expressions_buffer)
            return p[0]

        ######## GRAMMAR FOR EXIT ########

        @self.pg.production('expression : CLOSE')
        def expression_close(p):
            return Exit()

        ######## ERROR Handling - UwU ########

        @self.pg.error
        def error_handler(token):
            raise ValueError(
                "Ran into a %s where it wasn't expected" % token.gettokentype())

    def get_parser(self):
        return self.pg.build()
