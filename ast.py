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
        return self.value[self.index]


class Print():
    def __init__(self, value):
        self.value = value

    def eval(self):
        return self.value.eval()


class Exit:
    def eval(self):
        print("What did you thought that i would get upset? It's not that i like you b-baaka. *Hmph*")
        quit()
