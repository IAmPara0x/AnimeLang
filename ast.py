from colorama import Fore, Back, Style


class Integer:
    def __init__(self, value):
        self.value = value

    def eval(self):
        return int(self.value)


class Float:
    def __init__(self, value):
        self.value = value

    def eval(self):
        return float(self.value)


class String_type:
    def __init__(self, value):
        self.value = value

    def eval(self):
        return self.value


class BinaryOp:
    def __init__(self, left, right):
        self.left = left
        self.right = right


class Add(BinaryOp):
    def eval(self):
        return self.left.eval() + self.right.eval()


class Substract(BinaryOp):
    def eval(self):
        return self.left.eval() - self.right.eval()


class Multiply(BinaryOp):
    def eval(self):
        return self.left.eval() * self.right.eval()


class Divide(BinaryOp):
    def eval(self):
        if self.right.eval() == 0:
            print(
                "Naaani? you were trying to divide by 0."
                "B-Baaaaaaka that's not possible"
            )
        return self.left.eval() / self.right.eval()


# class for lists
class List_type:
    def __init__(self):
        self.value = []
        self.is_index = False
        self.index = None

    def eval(self):
        if self.is_index:
            return self.get_index()
        return self.value

    def get_index(self):
        self.is_index = False
        return self.value[self.index]


class Print:
    def __init__(self, value):
        self.value = value

    def eval(self):
        return self.value.eval()


class Print_stack:
    def __init__(self):
        self.stack = []
        self.info_terms = []
        self.error_terms = []

    def eval(self):
        for i, obj in enumerate(self.stack):
            if i in self.info_terms:
                print(Fore.GREEN + obj)
                print(Style.RESET_ALL)
            elif i in self.error_terms:
                print(Fore.RED + obj)
                print(Style.RESET_ALL)
            else:
                print(obj)

    def append(self, val) -> None:
        if val == None:
            return
        elif isinstance(val.eval(), list):
            obj = val.eval().copy()
        elif isinstance(val, Info_type):
            obj = val.eval()
            self.info_terms.append(len(self.stack))
        elif isinstance(val, Error_type):
            obj = val.eval()
            self.error_terms.append(len(self.stack))
        else:
            obj = val.eval()
        self.stack.append(obj)


# class for variable
class Variable_type:
    def __init__(self, name, type, value):
        self.name = name
        self.value = value
        self.type = type
        if self.type == "LIST":
            if not isinstance(self.value, list):
                raise ValueError()
            self.is_index = False
            self.index = None
        if self.type == "BOOL":
            if self.value != "kawai" and self.value != "baaka":
                raise ValueError()
        if self.type == "INTEGER":
            if not isinstance(self.value, int):
                raise ValueError()
        if self.type == "FLOAT":
            if not isinstance(self.value, float):
                raise ValueError()
        if self.type == "STRING":
            if not isinstance(self.value, str):
                raise ValueError()

    def eval(self):
        if self.type == "LIST":
            return self.leval()
        return self.value

    def leval(self):
        if self.is_index:
            self.is_index = False
            return self.value[self.index]
        return self.value


# class to store all the variables
class Variables_dict:
    def __init__(self):
        self.dict = {}

    def add_variable(self, name: str, variable):
        self.dict[name] = variable

    def get_variable(self, name: str):
        return self.dict[name]


class Booleans:
    def __init__(self, value):
        self.value = value

    def eval(self):
        return self.value


# class for conditionals


class Conditional_level:
    def __init__(self):
        self.current_nested_level = 0
        self.if_conditional = None
        self.else_conditional = None
        self.state = None
        self.next_conditional = None
        self.parent_conditional = None

    @property
    def prev(self):
        return self.parent_conditional

    @property
    def next(self):
        return self.next_conditional


class If_type:
    def __init__(self, val1, val2):
        self.val1 = val1
        self.val2 = val2
        self.state = True if self.val1 == self.val2 else False

    def eval(self):
        return self.state


class Else_type:
    def __init__(self, state):
        self.state = state

    def eval(self):
        return self.state


class Info_type:
    def __init__(self, string: str):
        self.info = string

    def eval(self) -> str:
        return self.info


#### classes for functions ####


class Function_state:
    def __init__(self, print_stack, variables_dict):
        self.print_stack = print_stack
        self.variables = variables_dict
        self.expressions_buffer = []

    def exec_print_exp(self, exp):
        def exec():
            self.print_stack.append(exp)

        self.expressions_buffer.append(exec)
        return exec

    def exec_get_list_index(self, list_name, index):
        def exec():
            list_name.is_index = True
            list_name.index = index.eval()
        self.expressions_buffer.append(exec)
        return exec


class Func_type(Function_state):
    def __init__(self, name, print_stack, variables_dict):
        super().__init__(print_stack, variables_dict)
        self.name = name

    def eval(self):
        for exp in self.expressions_buffer:
            exp()


class Func_dict:
    def __init__(self):
        self.dict = {}
        self.in_function = False
        self.curr_function_name = None

    def get_func(self, name):
        return self.dict[name]

    def add_func(self, name, val: Func_type):
        self.dict[name] = val
        self.curr_function_name = name
        self.in_function = True

    def end_func(self):
        self.curr_function_name = None
        self.in_function = False

    def add_exp(self, exp):
        func = self.dict[self.curr_function_name]
        func.expressions_buffer.append(exp)

    @property
    def curr_function(self):
        return self.dict[self.curr_function_name]


#### classes for error handling ####
class Error_type:
    def __init__(self, error_type, error_value):
        self.error_type = error_type
        self.error_value = error_value

    def eval(self):
        return f"{self.error_type} : {self.error_value}"


class Exit:
    def eval(self):
        print(
            "What did you thought that i would get upset? It's not that i like you b-baaka. *Hmph*"
        )
        quit()
