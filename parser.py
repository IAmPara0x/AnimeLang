from rply import ParserGenerator
from utils import *
from ast import (
  Integer,
  Float,
  Add,
  Substract,
  Multiply,
  Divide,
  List_type,
  Variable_type,
  Variables_dict,
  Info_type,
  String_type,
  Conditional_level,
  If_type,
  Func_type,
  Func_dict,
  Print,
  Print_stack,
  Error_type,
  Exit,
)
from tokens import TOKENS_DICT


class Parser:
  def __init__(self):
    self.pg = ParserGenerator(
      [token_name for token_name in TOKENS_DICT.keys()],
      precedence=[
        ("left", ["ADD", "SUBSTRACT"]),
        ("left", ["MULTIPLY", "DIVIDE"]),
      ],
    )

    self.variables_dict = Variables_dict()  # stores all the variables
    self.print_stack = Print_stack()
    self.global_conditional_state = Conditional_level()
    self.functions_dict = Func_dict()

  def parse(self):
    @self.pg.production("program : expression")
    @self.pg.production("program : f_expression")
    def program(p):
      return Print(p[0])

    #### file parsing start ####
    @self.pg.production("f_expression : ENTRY")
    def f_parsing_start(p):
      return p[0]

    #### file end parsing ####
    @self.pg.production("f_expression : f_expression EXIT")
    @self.pg.production("f_expression : EXIT")
    def f_parsing_end(p):
      return self.print_stack

    #### GRAMMAR FOR PRINTING STUFF ####

    @self.pg.production("line_expression : PRINT expression LINE_END")
    def print_expression(p):
      if (self.global_conditional_state.state == True
          or self.global_conditional_state.state is None):
        if self.functions_dict.in_function:
          exp = p[1]
          func = self.functions_dict.curr_function
          func.exec_print_exp(exp)
        else:
          self.print_stack.append(p[1])
      return p[1]

    ######## GRAMMAR FOR BASIC ARITHMETIC CALCULATIONS ########

    @self.pg.production("expression : OPEN_PAREN expression CLOSE_PAREN")
    def expression_parens(p):
      return p[1]

    @self.pg.production("expression : expression SUBSTRACT expression")
    @self.pg.production("expression : expression ADD expression")
    @self.pg.production("expression : expression MULTIPLY expression")
    @self.pg.production("expression : expression DIVIDE expression")
    def expression_binaryop(p):
      left = p[0]
      right = p[2]

      if isinstance(left, Variable_type) and isinstance(right, Variable_type):
        if left.type == right.type:
          if p[1].gettokentype() == "ADD":
            return Add(left, right)
          elif p[1].gettokentype() == "SUBSTRACT":
            return Substract(left, right)
          elif p[1].gettokentype() == "MULTIPLY":
            return Multiply(left, right)
          elif p[1].gettokentype() == "DIVIDE":
            return Divide(left, right)
          else:
            err = Error_type(
                "OPERATOR NOT VALID meow",
                f"Ba-aaaka {p[1].value} is not a valid operator.",
            )
            self.print_stack.append(err)
            raise ValueError()
            return err
        else:
          left_type = get_var_type(left)
          right_type = get_var_type(right)

          err = Error_type(
              "Can't operate with different type of waifus",
              f"you tried to {p[1].gettokentype()} waifu '{left.name}-chan' which is of type {left_type} and "
              + f"'{right.name}-chan' which is of type {right_type}",
          )
          self.print_stack.append(err)
          raise ValueError()

      if p[1].gettokentype() == "ADD":
        return Add(left, right)
      elif p[1].gettokentype() == "SUBSTRACT":
        return Substract(left, right)
      elif p[1].gettokentype() == "MULTIPLY":
        return Multiply(left, right)
      elif p[1].gettokentype() == "DIVIDE":
        return Divide(left, right)
      else:
        err = Error_type(
            "OPERATOR NOT VALID meow",
            f"Ba-aaaka {p[1].value} is not a valid operator.",
        )
        self.print_stack.append(err)
        raise ValueError()
        return err

    ########  GRAMMA FOR BASIC DATATYPES ########

    @self.pg.production("expression : INTEGER")
    @self.pg.production("expression : FLOAT")
    def expression_number(p):
      if p[0].gettokentype() == "FLOAT":
        return Float(p[0].value)
      elif p[0].gettokentype() == "INTEGER":
        return Integer(p[0].value)

    ######## GRAMMAR FOR LISTS ########

    # returns the list created
    @self.pg.production("expression : list_expression")
    def new_list_type(p):
      return p[0]

    # parsing of the list ends here
    @self.pg.production(
        "list_expression : list_expression expression S_CLOSE_PAREN"
    )
    def list_end(p):
      p[0].value.append(p[1].eval())
      return p[0]

    # parses all the elements insides the list
    @self.pg.production("list_expression : list_expression expression COMMA")
    def list_parse(p):
      p[0].value.append(p[1].eval())
      return p[0]

    # parsing of the created list begins here
    @self.pg.production("list_expression : S_OPEN_PAREN")
    def list_begin(p):
      new_list = List_type()
      return new_list

    # gets the element from the list given index number
    @self.pg.production("expression : INDEX_W BAR expression BAR val_expression")
    @self.pg.production("expression : INDEX_W BAR expression BAR list_expression")
    def get_list_index(p):
      #FIXME : prints the list when wants an index but works fine with vars
      if (self.global_conditional_state.state == True
          or self.global_conditional_state.state is None):
        p[4].is_index = True
        p[4].index = p[2].eval()
        return p[4]

    @self.pg.production(
        "line_expression : APPEND expression TO val_expression LINE_END"
    )
    def add_to_list(p):
      if (self.global_conditional_state.state == True
          or self.global_conditional_state.state is None):
        if p[-2].type == "LIST":
          p[-2].value.append(p[1].eval())
        else:
          err = Error_type(
              "Waifu not suitable",
              f"you can add waifu only to your harem but '{p[-2].name}-chan' is not of harem type.",
          )
          self.print_stack.append(err)
          raise ValueError()
        return p[-2]

    @self.pg.production(
        "line_expression : REMOVE INDEX_W FROM val_expression LINE_END"
    )
    def remove_from_list(p):
      if (self.global_conditional_state.state == True
        or self.global_conditional_state.state is None):
        if p[-2].type == "LIST":
          p[-2].value.pop()
        else:
          err = Error_type(
              "Waifu not suitable",
              f"you can remove waifu only from your harem but '{p[-2].name}-chan' is not of harem type.",
          )
          self.print_stack.append(err)
          raise ValueError()
          return p[-2]

    @self.pg.production("expression : C_LIST SIZE val_expression")
    def get_length_of_list(p):
      if (self.global_conditional_state.state == True
          or self.global_conditional_state.state is None):
        if p[-1].type == "LIST":
          length = len(p[-1].value)
          return Integer(length)
        else:
          err = Error_type(
              "Waifu not suitable",
              f"waifu does not have size baa-aaka only harem has it's size but '{p[-1].name}-chan' is not harem type",
          )
          self.print_stack.append(err)
          raise ValueError()

    #### GRAMMAR FOR VARIABLES ####

    @self.pg.production("expression : val_expression")
    def val_expression(p):
      return p[0]

    # return the value of the variable
    @self.pg.production("val_expression : n_expression")
    def return_variable(p):
      if (self.global_conditional_state.state == True
          or self.global_conditional_state.state is None):
        name = p[0].value
        try:
          return self.variables_dict.dict[name]
        except Exception as e:
          self.print_stack.append(
              Error_type(
                  "WAIFU DOES NOT EXISTS",
                  f"Baaaka you haven't created a waifu with name '{name}-chan'",
              )
          )
          raise ValueError()

    # returns the name of the variable
    @self.pg.production("n_expression : VARIABLE")
    def variable_name(p):
      return p[0]

    # returns the calculated value of the variable
    @self.pg.production("v_expression : EQUALS expression LINE_END")
    def variable_value(p):
      return p[1]

    @self.pg.production("line_expression : NEW C_INTEGER n_expression v_expression")
    def variable_int(p):
      if (self.global_conditional_state.state == True
          or self.global_conditional_state.state is None):
        name = p[2].value
        value = p[-1].eval()
        type = "INTEGER"
        try:
          variable = Variable_type(name, type, value)
        except ValueError:
          err = Error_type(
              "waifu not suitable",
              f"Tsundere waifus can only have integers but {p[-1].eval()} is not an integer.",
          )
          self.print_stack.append(err)
          raise ValueError()
        self.variables_dict.add_variable(name, variable)
        return variable

    @self.pg.production("line_expression : NEW C_FLOAT n_expression v_expression")
    def variable_float(p):
      if (self.global_conditional_state.state == True
          or self.global_conditional_state.state is None):
        name = p[2].value
        value = p[-1].eval()
        type = "FLOAT"
        try:
          variable = Variable_type(name, type, value)
        except ValueError:
          err = Error_type(
              "waifu not suitable",
              f"Yandere waifus can only have floats but {p[-1].eval()} is not an float.",
          )
          self.print_stack.append(err)
          raise ValueError()
          return err
        self.variables_dict.add_variable(name, variable)
        return variable

    @self.pg.production("line_expression : NEW C_LIST n_expression v_expression")
    def variable_list(p):
      if (self.global_conditional_state.state == True
          or self.global_conditional_state.state is None):
        name = p[2].value
        value = p[-1].eval()
        type = "LIST"
        try:
          variable = Variable_type(name, type, value)
        except ValueError:
          err = Error_type(
              "Harem not suitable",
              f"Harem can have only group of waifus, integers, floats, strings but "
              f"{value} doesn't satisfies any one of the group.",
          )
          self.print_stack.append(err)
          raise ValueError()

        self.variables_dict.add_variable(name, variable)
        return variable

    @self.pg.production("line_expression : NEW C_BOOL n_expression v_expression")
    def variable_bool(p):
      if (self.global_conditional_state.state == True
          or self.global_conditional_state.state is None):
          name = p[2].value
          value = p[-1].eval()
          type = "BOOL"
          try:
            variable = Variable_type(name, type, value)
          except ValueError:
            err = Error_type(
                "Ship not suitable",
                f"A Ship can only be kawai or baaka but {value} is none of them.",
            )
            self.print_stack.append(err)
            raise ValueError()
          self.variables_dict.add_variable(name, variable)
          return variable

    # parses string

    @self.pg.production("expression : STRING")
    def cvt_string_to_expression(p):
      return String_type(p[0].value)

    # creates string
    @self.pg.production("line_expression : NEW C_STRING n_expression v_expression")
    def variables_string(p):
      if (self.global_conditional_state.state == True
          or self.global_conditional_state.state is None):
        name = p[2].value
        value = p[-1].eval()
        type = "STRING"
        try:
          variable = Variable_type(name, type, value)
        except ValueError:
          err = Error_type(
              "waifu not suitable",
              f"Kuudere waifus can only have strings but {p[-1].eval()} is not a string.",
          )
          self.print_stack.append(err)
          raise ValueError()
        self.variables_dict.add_variable(name, variable)
        return variable

    @self.pg.production("line_expression : INDEX_W val_expression v_expression")
    @self.pg.production(
        "line_expression : INDEX_W BAR expression BAR val_expression v_expression"
    )
    def change_variable_value(p):
        if (
            self.global_conditional_state.state == True
            or self.global_conditional_state.state is None
        ):
          if len(p) == 3:
            var = p[1]
            value = p[-1].eval()
            var.value = value
            var.type = get_exp_type(value)
            if var.type == "LIST":
              var.is_index = False
              var.index = None
            return var

          elif len(p) == 6:
            var = p[4]
            index = p[2].eval()
            value = p[-1].eval()
            var.value[index] = value
            return var

    @self.pg.production("expression : INDEX_W TYPE val_expression")
    def get_variable_type(p):
      if (
          self.global_conditional_state.state == True
          or self.global_conditional_state.state is None
      ):
        msg = None
        if p[-1].type == "INTEGER":
          msg = f"waifu {p[-1].name}-chan is a tsundere"
        elif p[-1].type == "FLOAT":
          msg = f"waifu {p[-1].name}-chan is a yandere"
        elif p[-1].type == "LIST":
          msg = f"{p[-1].name} is a harem with lots of waifus"
        elif p[-1].type == "BOOL":
          msg = f"{p[-1].name} is of type ship"
        elif p[-1].type == "STRING":
          msg = f"waifu {p[-1].name}-chan is a kuudere"
        return Info_type(msg)

    @self.pg.production("expression : line_expression")
    def line_expression(p):
      if len(p) == 2:
        return p[1]
      return p[0]

    #### GRAMMAR FOR CONDITIONALS ####

    @self.pg.production(
        "conditionals_expression : CHECK OPEN_PAREN expression BAR IS_EQUALS BAR expression CLOSE_PAREN C_OPEN_PAREN"
    )
    def conditional_if_begin(p):
      if p[2] is None:
        val1 = None
      else:
        val1 = p[2].eval()
      if p[6] is None:
        val2 = None
      else:
        val2 = p[6].eval()

      if self.global_conditional_state.if_conditional is None:
        conditional = If_type(val1, val2)
        self.global_conditional_state.if_conditional = conditional
        self.global_conditional_state.state = conditional.state
        self.global_conditional_state.current_nested_level += 1

      elif self.global_conditional_state.if_conditional is not None:
        conditional_state = Conditional_level()
        conditional = If_type(val1, val2)
        conditional_state.if_conditional = conditional
        if (
            self.global_conditional_state.state is True
            and conditional.state is True
        ):
          conditional_state.state = True
        else:
          conditional_state.state = False
        temp = self.global_conditional_state
        self.global_conditional_state = conditional_state
        self.global_conditional_state.parent_conditional = temp
        self.global_conditional_state.current_nested_level = (
            temp.current_nested_level + 1
        )

      return conditional

    @self.pg.production("conditionals_expression : ELSE C_OPEN_PAREN")
    def conditional_else_begin(p):
      if (
          self.global_conditional_state.parent_conditional is not None
          and self.global_conditional_state.parent_conditional.state is False
      ):
        self.global_conditional_state.state = False
        return self.global_conditional_state

      if (
          self.global_conditional_state.if_conditional is not None
          and self.global_conditional_state.state == False
      ):
        self.global_conditional_state.state = True
      elif (
          self.global_conditional_state.if_conditional is not None
          and self.global_conditional_state.state == True
      ):
        self.global_conditional_state.state = False
      elif self.global_conditional_state.parent_conditional.state is False:
        self.global_conditional_state.state = False
      return self.global_conditional_state

    @self.pg.production("line_expression : e_expression C_CLOSE_PAREN")
    @self.pg.production("line_expression : e_expression C_CLOSE_PAREN LINE_END")
    def conditional_end(p):
      if len(p) == 3:
          if self.global_conditional_state.parent_conditional is not None:
              self.global_conditional_state = (
                  self.global_conditional_state.parent_conditional
              )
          else:
              self.global_conditional_state = Conditional_level()
      return self.global_conditional_state

    #### GRAMMAR for e_expressions ####

    @self.pg.production("e_expression : line_expression")
    @self.pg.production("e_expression : conditionals_expression")
    @self.pg.production("e_expression : e_expression line_expression")
    def get_e_expression(p):
      if len(p) == 2:
          return p[0]
      return p[0]

    @self.pg.production("f_expression : f_expression e_expression")
    def cvt_e_expression_to_f_expression(p):
      return p[1]

    #### GRAMMAR for functions ####

    @self.pg.production("func_expression : NEW C_FUNC n_expression C_FUNC_START")
    def start_parsing_function(p):
      new_func = Func_type(p[2].value, self.print_stack, self.variables_dict)
      self.functions_dict.add_func(p[2].value, new_func)
      return new_func

    @self.pg.production(
        "line_expression : func_expression e_expression C_FUNC_CLOSE LINE_END"
    )
    def end_parsing_function(p):
      self.functions_dict.end_func()
      return p[0]

    @self.pg.production("line_expression : FUNC_EXEC C_FUNC n_expression LINE_END")
    def exec_function(p):
      func = self.functions_dict.get_func(p[2].value)
      func.eval()
      return p[2]

    ######## GRAMMAR FOR EXIT ########

    @self.pg.production("expression : CLOSE")
    def expression_close(p):
      return Exit()

    ######## ERROR Handling ########

    @self.pg.error
    def error_handler(token):
      raise ValueError(
          "Ran into a %s where it wasn't expected" % token.gettokentype()
      )

  def get_parser(self):
      return self.pg.build()
