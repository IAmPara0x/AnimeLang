from rply import ParserGenerator
from ast import (
    Integer,
    Float,
    Add,
    Substract,
    Multiply,
    Divide,
    Variable_buffer, # this class will be used while making functions
    Eval_expressions_buffer, # this class will be used while making functions
    E_expressions_list, # this class will be used while making functions
    List_type,
    Variable_type,
    Variables_dict,
    Booleans,
    Check_if,
    Check_else,
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
        self.global_nested_level = 0 #TODO: improve the way to store global_nested_level

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
        @self.pg.production('expression : list_expression')
        def new_list_type(p):
            return p[0]

        # parsing of the list ends here
        @self.pg.production('list_expression : S_OPEN_PAREN expression')
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

        @self.pg.production('line_expression : NEW C_INTEGER n_expression v_expression')
        @self.pg.production('line_expression : CONDITIONAL_IF_R NEW C_INTEGER n_expression v_expression')
        @self.pg.production('line_expression : CONDITIONAL_IF_R NEW C_INTEGER n_expression v_expression')
        def variable_int(p):
            # check if condtional local scope
            if len(p) == 5:
                if p[0].eval() == "baaka":
                    return p[0]
                else:
                    name = p[3].value
                    value = Integer(p[-1].eval()).eval()
                    type = "INTEGER"
                    variable = Variable_type(name, type, value)
                    self.variables_dict.add_variable(name, variable)
                    return p[0]

            elif len(p) == 4:
                name = p[2].value
                value = Integer(p[-1].eval()).eval()
                type = "INTEGER"
                variable = Variable_type(name, type, value)
                self.variables_dict.add_variable(name, variable)
                return variable

        @self.pg.production('line_expression : NEW C_FLOAT n_expression v_expression')
        @self.pg.production('line_expression : CONDITIONAL_IF_R NEW C_FLOAT n_expression v_expression')
        def variable_float(p):
            if len(p) == 5:
                if p[0].eval() == "baaka":
                    return p[0]
                else:
                    name = p[3].value
                    value = Float(p[-1].eval()).eval()
                    type = "FLOAT"
                    variable = Variable_type(name, type, value)
                    self.variables_dict.add_variable(name, variable)
                    return p[0]
            elif len(p) == 4:
                name = p[2].value
                value = Float(p[-1].eval()).eval()
                type = "FLOAT"
                variable = Variable_type(name, type, value)
                self.variables_dict.add_variable(name, variable)
                return variable

        @self.pg.production('line_expression : NEW C_LIST n_expression v_expression')
        @self.pg.production('line_expression : CONDITIONAL_IF_R NEW C_LIST n_expression v_expression')
        def variable_list(p):
            if len(p) == 5:
                if p[0].eval() == "baaka":
                    return p[0]
                else:
                    name = p[3].value
                    value = p[-1].eval()
                    type = "LIST"
                    variable = Variable_type(name, type, value)
                    self.variables_dict.add_variable(name, variable)
                    return p[0]
            elif len(p) == 4:
                name = p[2].value
                value = p[-1].eval()
                type = "LIST"
                variable = Variable_type(name, type, value)
                self.variables_dict.add_variable(name, variable)
                return variable

        @self.pg.production('line_expression : NEW C_BOOL n_expression v_expression')
        @self.pg.production('line_expression : CONDITIONAL_IF_R NEW C_BOOL n_expression v_expression')
        def variable_bool(p):
            if len(p) == 5:
                if p[0].eval() == "baaka":
                    return p[0]
                else:
                    name = p[3].value
                    value = p[-1].eval()
                    type = "BOOL"
                    variable = Variable_type(name, type, value)
                    self.variables_dict.add_variable(name, variable)
                    return p[0]
            elif len(p) == 4:
                name = p[2].value
                value = p[-1].eval()
                type = "BOOL"
                variable = Variable_type(name, type, value)
                self.variables_dict.add_variable(name, variable)
                return variable

        @self.pg.production('line_expression : INDEX_W n_expression v_expression')
        @self.pg.production('line_expression : INDEX_W BAR expression BAR n_expression v_expression')
        @self.pg.production('line_expression : CONDITIONAL_IF_R INDEX_W n_expression v_expression')
        def change_variable_value(p):
            if len(p) == 4:
                if p[0].eval() == "baaka":
                    return p[0]
                else:
                    name = p[2].value
                    value = p[-1].eval()
                    var = self.variables_dict.get_variable(name)
                    var.value = value
                    return p[0]
            elif len(p) == 3:
                name = p[1].value
                value = p[-1].eval()
                var = self.variables_dict.get_variable(name)
                var.value = value
                return var

            elif len(p) == 6:
                name = p[4].value
                index = p[2].eval()
                value = p[-1].eval()
                var = self.variables_dict.get_variable(name)
                var.value[index] = value
                return var

        @self.pg.production('expression : line_expression')
        def line_expression(p):
            return p[0]

        #### GRAMMAR FOR CONDITIONALS ####

        @self.pg.production('expression : b_expression')
        def booleans_expression(p):
            return p[0]

        @self.pg.production('b_expression : TRUE')
        @self.pg.production('b_expression : FALSE')
        def booleans(p):
            return Booleans(p[0].value)

        @self.pg.production('CONDITIONAL_IF_R : CHECK OPEN_PAREN expression BAR IS_EQUALS BAR expression CLOSE_PAREN')
        @self.pg.production('CONDITIONAL_IF_R : e_expression CHECK OPEN_PAREN expression BAR IS_EQUALS BAR expression CLOSE_PAREN')
        @self.pg.production('CONDITIONAL_IF_R : e_expression  ELSE')
        def conditional_check(p):
            if len(p) == 8:
                return Check_if(p[2], p[6])
            elif len(p) == 2:
                if self.global_nested_level == p[0].nested_level:
                    return Check_else(p[0].val1, p[0].val2)
                else:
                    return Check_else(p[0].parent.val1, p[0].parent.val2)
            elif len(p) == 9:
                condtional = Check_if(p[3], p[7])
                condtional.parent = p[0]
                return condtional

        @self.pg.production('CONDITIONAL_IF_R : CONDITIONAL_IF_R C_OPEN_PAREN')
        def begin_conditional_scope(p):
            if not isinstance(p[0], Check_else):
                self.global_nested_level += 1
                p[0].nested_level = self.global_nested_level
            else:
                p[0].nested_level = self.global_nested_level
            return p[0]

        @self.pg.production('e_expression : e_expression C_CLOSE_PAREN LINE_END')
        @self.pg.production('e_expression : e_expression C_CLOSE_PAREN')
        def end_conditional_scope(p):
            if len(p) == 3:
                self.global_nested_level -= 1
            return p[0]

        @self.pg.production('expression : CONDITIONAL_IF_R ')
        @self.pg.production('expression : e_expression ')
        def conditional_result(p):
            return p[0]

        #### GRAMMAR for e_expressions ####

        @self.pg.production('e_expression : line_expression')
        @self.pg.production('e_expression : e_expression line_expression')
        def get_e_expression(p):
            if len(p) == 2:
                return p[0]
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
