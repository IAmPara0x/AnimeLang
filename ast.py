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
        self.variables_dict = {}

    def add_variable(self, name: str, variable):
        self.variables_dict[name] = variable

    def get_variable(self, name: str):
        return self.variables_dict[name]

# class for conditionals
class Booleans():
    def __init__(self, value):
        self.value = value

    def eval(self):
        return self.value

class Check():
    def __init__(self, val1, val2):
        self.val1 = val1
        self.val2 = val2

    def eval(self):
        if self.val1.eval() == self.val2.eval():
            return "kawai"
        else:
            return "baaka"


class Eval_expressions():
    def __init__(self):
        self.expressions = []

    def add_expression(self,expression):
        self.expressions.append(expression)

    def eval(self):
        for i in self.expressions:
            i.eval()


class Exit:
    def eval(self):
        print("What did you thought that i would get upset? It's not that i like you b-baaka. *Hmph*")
        quit()
