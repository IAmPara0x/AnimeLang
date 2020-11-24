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
    Info_type,
    Print,
    Print_stack,
    Error_type,
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
        self.print_stack = Print_stack()

    def parse(self):
        # @self.pg.production('program : expression LINE_END')
        # TODO: replace this line with above one
        @self.pg.production('program : expression')
        @self.pg.production('program : f_expression')
        def program(p):
            return Print(p[0])

        #### file parsing start ####
        @self.pg.production('f_expression : ENTRY')
        def f_parsing_start(p):
            return p[0]

        #### file end parsing ####
        @self.pg.production('f_expression : f_expression EXIT')
        @self.pg.production('f_expression : EXIT')
        def f_parsing_end(p):
            return self.print_stack

        #### GRAMMAR FOR PRINTING STUFF ####
        @self.pg.production('f_expression : f_expression PRINT expression LINE_END')
        @self.pg.production('expression : PRINT expression LINE_END')
        def print_expression(p):
            if len(p) == 4:
                self.print_stack.append(p[2])
                return p[2]
            return p[1]

        @self.pg.production('line_expression : CONDITIONAL_IF_R PRINT expression LINE_END')
        def conditional_print_expression(p):
            if p[0].eval() == "baaka":
                return p[0]
            else:
                self.print_stack.append(p[2])
                return p[0]


        ######## GRAMMAR FOR BASIC ARITHMETIC CALCULATIONS ########

        @self.pg.production('expression : OPEN_PAREN expression CLOSE_PAREN')
        def expression_parens(p):
            return p[1]

        @self.pg.production('expression : expression SUBSTRACT expression')
        @self.pg.production('expression : expression ADD expression')
        @self.pg.production('expression : expression MULTIPLY expression')
        @self.pg.production('expression : expression DIVIDE expression')
        def expression_binayop(p):
            if isinstance(p[0], Error_type):
                return p[0]
            if isinstance(p[1], Error_type):
                return p[1]
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
                return Error_type("OPERATOR NOT VALID meow", f"Ba-aaaka {p[1].value} is not a valid operator.")

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
        @self.pg.production('list_expression : list_expression expression S_CLOSE_PAREN')
        def list_end(p):
            p[0].value.append(p[1].eval())
            return p[0]

        # parses all the elements insides the list
        @self.pg.production('list_expression : list_expression expression COMMA')
        def list_parse(p):
            p[0].value.append(p[1].eval())
            return p[0]

        # parsing of the created list begins here
        @self.pg.production('list_expression : S_OPEN_PAREN')
        def list_begin(p):
            new_list = List_type()
            return new_list

        # gets the element from the list given index number
        @self.pg.production('expression : INDEX_W BAR expression BAR val_expression')
        @self.pg.production('expression : INDEX_W BAR expression BAR list_expression')
        def get_list_index(p):
            if isinstance(p[-1], Error_type):
                return p[-1]
            p[4].is_index = True
            p[4].index = p[2].eval()
            return p[4]

        @self.pg.production('line_expression : APPEND expression TO val_expression LINE_END')
        @self.pg.production('line_expression : CONDITIONAL_IF_R APPEND expression TO val_expression LINE_END')
        def add_to_list(p):
            if isinstance(p[-2], Error_type):
                return p[-2]

            if len(p) == 6:
                if p[0].eval() == "baaka":
                    return p[0]
                else:
                    if p[-2].type == "LIST":
                        p[-2].value.append(p[2].eval())
                    return p[0]

            elif len(p) == 5:
                if p[-2].type == "LIST":
                    p[-2].value.append(p[2].eval())
                return p[-2]


        @self.pg.production('line_expression : REMOVE INDEX_W FROM val_expression LINE_END')
        @self.pg.production('line_expression : CONDITIONAL_IF_R REMOVE INDEX_W FROM val_expression LINE_END')
        def remove_from_list(p):
            if isinstance(p[-2], Error_type):
                return p[-2]

            if len(p) == 6:
                if p[0].eval() == "baaka":
                    return p[0]
                else:
                    if p[-2].type == "LIST":
                        p[-2].value.pop()
                    return p[0]
            elif len(p) == 5:
                if p[-1].type == "LIST":
                    p[-1].value.pop()
                return p[-1]


        @self.pg.production('expression : C_LIST SIZE val_expression')
        def get_length_of_list(p):
            if isinstance(p[-1], Error_type):
                return p[-1]
            if p[-1].type == "LIST":
                length = len(p[-1].value)
                return Integer(length)

       #### GRAMMAR FOR VARIABLES ####

        @self.pg.production('expression : val_expression')
        def val_expression(p):
           return p[0]

        # return the value of the variable
        @self.pg.production('val_expression : n_expression')
        def return_variable(p):
            name = p[0].value
            try:
                return self.variables_dict.dict[name]
            except KeyError:
                return Error_type("WAIFU DOES NOT EXISTS", f"Baaaka you haven't created a waifu with name '{name}-chan'")

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
        @self.pg.production('line_expression : CONDITIONAL_IF_R INDEX_W BAR expression BAR n_expression v_expression')
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

            elif len(p) == 7:
                if p[0].eval() == "baaka":
                    return p[0]
                name = p[5].value
                index = p[3].eval()
                value = p[-1].eval()
                var = self.variables_dict.get_variable(name)
                var.value[index] = value
                return p[0]

        @self.pg.production('expression : INDEX_W TYPE val_expression')
        def get_variable_type(p):
            if isinstance(p[-1], Error_type):
                return p[-1]
            msg = None
            if p[-1].type == "INTEGER":
                msg = f"waifu {p[-1].name}-chan is a tsundere"
            elif p[-1].type == "FLOAT":
                msg = f"waifu {p[-1].name}-chan is a yandere"
            elif p[-1].type == "LIST":
                msg = f"{p[-1].name} is a harem with lots of waifus"
            elif p[-1].type == "BOOL":
                msg = f"{p[-1].name} is of type ship"
            return Info_type(msg)

        @self.pg.production('expression : line_expression')
        @self.pg.production('f_expression : f_expression line_expression')
        def line_expression(p):
            if len(p) == 2:
                return p[1]
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
                    check_else = Check_else(p[0].val1, p[0].val2)
                    check_else.eval_val = "baaka" if p[0].eval_val == "kawai" else "kawai"
                    return check_else
                else:
                    check_else = Check_else(p[0].val1, p[0].val2)
                    check_else.eval_val = "baaka" if p[0].eval_val == "kawai" else "kawai"
                    return check_else
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
        @self.pg.production('e_expression : CONDITIONAL_IF_R')
        @self.pg.production('e_expression : e_expression line_expression')
        def get_e_expression(p):
            if len(p) == 2:
                return p[0]
            return p[0]


        @self.pg.production('f_expression : f_expression e_expression')
        def cvt_e_expression_to_f_expression(p):
            return p[1]

        ######## GRAMMAR FOR EXIT ########

        @self.pg.production('expression : CLOSE')
        def expression_close(p):
            return Exit()

        ######## ERROR Handling ########

        @self.pg.error
        def error_handler(token):
            raise ValueError(
                "Ran into a %s where it wasn't expected" % token.gettokentype())

    def get_parser(self):
        return self.pg.build()
