class Integer():
    def __init__(self, value):
        self.value = value

    def eval(self):
        return int(self.value)


class Float():
    def __init__(self, value):
        self.value = value

    def eval(self):
        return float(self.value)


class BinaryOp():
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
            print("Naaani? you were trying to divide by 0."
                  "B-Baaaaaaka that's not possible")
        return self.left.eval() / self.right.eval()


# class for lists
class List_type():
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


class Print():
    def __init__(self, value):
        self.value = value

    def eval(self):
        return self.value.eval()


# class for variable
class Variable_type():
    def __init__(self, name, type, value):
        self.name = name
        self.value = value
        self.type = type
        if self.type == "LIST":
            self.is_index = False
            self.index = None

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
class Variables_dict():
    def __init__(self):
        self.dict = {}

    def add_variable(self, name: str, variable):
        self.dict[name] = variable

    def get_variable(self, name: str):
        return self.dict[name]

# class for conditionals
class Booleans():
    def __init__(self, value):
        self.value = value

    def eval(self):
        return self.value

class Check_if():
    def __init__(self, val1, val2):
        self.val1 = val1
        self.val2 = val2
        self.nested_level = 0
        self.parent = None
        self.eval_val = None
        self.is_eval = False

    def eval(self):
        if not self.is_eval:
            if self.val1.eval() == self.val2.eval():
                self.eval_val = "kawai"
                return "kawai"
            else:
                self.eval_val = "baaka"
                return "baaka"
            self.is_eval = True
        else:
            return self.eval_val


class Check_else():
    def __init__(self, val1, val2):
        self.val1 = val1
        self.val2 = val2
        self.nested_level = 0
        self.parent = None
        self.eval_val = None

    def eval(self):
        if self.eval_val is not None:
            return self.eval_val
        if self.val1.eval() == self.val2.eval():
            return "baaka"
        else:
            return "kawai"


# class for e_expression
class Variable_buffer():
    def __init__(self, variable_name, value, type=None, action="create"):
        self.action = action
        self.name = variable_name
        self.value = value
        if self.action == "create":
            self.type = type

    def eval(self, variables_dict):
        if self.action == "create":
            if self.type == "INTEGER":
                self.value = int(self.value.eval())
            if self.type == "FLOAT":
                self.value = float(self.value.eval())
            variable = Variable_type(self.name, self.type, self.value)
            variables_dict[self.name] = variable
        if self.action == "change":
            variables_dict[self.name].value = self.value.eval()
        return variables_dict


class Eval_expressions_buffer():
    def __init__(self):
        self.expressions = []

    def add_expression(self,expression):
        self.expressions.append(expression)

    def eval(self, variables_dict):
        self.variables_dict = variables_dict
        for i in self.expressions:
            self.variables_dict = i.eval(variables_dict)
        return self.variables_dict

class E_expressions_list():
    def __init__(self):
        self.e_expressions_list = []

    def add_e_expression(self, e_expression: Eval_expressions_buffer):
        self.e_expressions_list.append(e_expression)

    def get_e_expression(self):
        return self.e_expressions_list.pop(0)

    @property
    def len(self):
        return len(self.e_expressions_list)

class Error_type:
    def __init__(self, error_type, error_value):
        self.error_type = error_type
        self.error_value = error_value

    def eval(self):
        return f"{self.error_type} : {self.error_value}"


class Exit:
    def eval(self):
        print("What did you thought that i would get upset? It's not that i like you b-baaka. *Hmph*")
        quit()
